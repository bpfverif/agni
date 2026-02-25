# Agni: Verifying the eBPF Verifier

Agni is a tool for verifying the correctness of the Linux Kernel eBPF
verifier's static analysis. 

Agni automatically (a) extracts the abstract semantics of the
value-tracking analysis from the verifier's C code, (b) generates and
checks verification conditions to ensure the soundness of the
analysis, and (c) if unsoundness is detected, synthesizes an eBPF
program that demonstrates the mismatch between abstract and concrete
semantics. See our
[paper](https://link.springer.com/chapter/10.1007/978-3-031-37709-9_12)
for details.

This repo contains instructions on how to run Agni against a specific
kernel commit.

---


Note: The `$VAR` notation (e.g. `$KERNBASEDIR`, `$KERNCOMMIT`, etc.)
is used to denote paths to directories that you have to create
yourself before running the instructions.


### Download Linux source (e.g. `bpf-next` tree)

```
git clone -b master --depth 1 git://git.kernel.org/pub/scm/linux/kernel/git/bpf/bpf-next.git $KERNBASEDIR

```
Save the commit hash of the Linux kernel commit we are planning to
verify in `KERNCOMMIT`.

```
cd $KERNBASEDIR
KERNCOMMIT=$(git rev-parse HEAD)
cd -
```

### Clone the repository
```
git clone https://github.com/bpfverif/agni.git $AGNIDIR
```
### Install dependencies

Agni depends on llvm-14.

```
sudo apt-get install -y --no-install-recommends \
  clang-14 llvm-14-dev llvm-14-tools \
  python3 python3-pip \
  make cmake libelf-dev \
  libjsoncpp-dev \
  libz3-dev
```

#### A note on clang and llvm binaries
Agni depends on clang, clang++, opt, llvm-extract, llvm-link, and
expects these binaries to be present in one directory (`/usr` by
default). If they are not present, please use `update-alternatives`
or equivalent to establish symbolic links.

### Install Python dependencies

```
cd $AGNIDIR
pip install -r requirements.txt
cd bpf-verification
pip install .
```

## Step 1. Generate encodings 

For each operator in the eBPF instruction set, the verifier's C code
updates its internal state that tracks values in eBPF registers.
First, we use Agni to extract the semantics of the verifier's
value-tracking C code into first-order a logic formula (in SMT) for
each eBPF operator. We will save the generated encodings in
`$ENCODINGSDIR`.

To generate the encodings for a specific eBPF abstract operator, we
use the `--specific-op` flag.

To speed up the verification step, we will generate modular encodings
using the `--modular` flag

`$LLVMDIR` should point to the directory of your
llvm binaries.
```
cd $AGNIDIR
cd llvm-to-smt
python3 generate_encodings.py \
            --llvmdir $LLVMDIR
            --kernver 6.10 --commit $KERNCOMMIT \
            --kernbasedir $KERNBASEDIR \
            --outdir $ENCODINGSDIR \
            --specific-op BPF_AND
            --modular
```

Sample output:
```
Getting encoding for BPF_AND
... done
Finished generating all encodings successfully (modular).
```

Agni supports the following eBPF abstract operators, named 
after their concrete counterparts:

```
BPF_ADD, BPF_SUB, BPF_OR, BPF_AND, BPF_XOR, BPF_LSH, BPF_RSH, BPF_ARSH, BPF_JLT, BPF_JLE, BPF_JSLT, BPF_JSLE, BPF_JEQ, BPF_JNE, BPF_JGE, BPF_JGT, BPF_JSGE, BPF_JSGT, BPF_ADD_32, BPF_SUB_32, BPF_OR_32, BPF_AND_32, BPF_XOR_32, BPF_LSH_32, BPF_RSH_32, BPF_ARSH_32, BPF_JLT_32, BPF_JLE_32, BPF_JSLT_32, BPF_JSLE_32, BPF_JEQ_32, BPF_JNE_32, BPF_JGE_32, BPF_JGT_32, BPF_JSGE_32, BPF_JSGT_32, BPF_SYNC
```

The automatic encoder produces an SMT-LIB (`.smt2`) file for the
abstract operator related to each eBPF instruction in `$ENCODINGSDIR`.

```
ls -1 $ENCODINGSDIR/*.smt2
BPF_AND.smt2
```

####  A note on BPF_SYNC
Note that while `BPF_SYNC` is not a first-class eBPF abstract
operator, it corresponds to a function (`reg_bounds_sync`) in the
kernel that does refinement -- using information in one abstract
domain, to update the information in the other abstract domains, in
order the improve the precision of the value-tracking. This function
is called at the tail end of every eBPF first-class abstract operator.
To perform the complete verification step for a first-class eBPF
abstract operator, we will need to generate the encodings for
`BPF_SYNC` in addition to the operator itself. Use `--specific-op`
to also obtain the encodings for `BPF_SYNC`.

```
python3 generate_encodings.py \
            --llvmdir $LLVMDIR
            --kernver 6.10 --commit $KERNCOMMIT \
            --kernbasedir $KERNBASEDIR \
            --outdir $ENCODINGSDIR \
            --specific-op BPF_SYNC
            --modular
```

## Step 2. Verification

We can now check the correctness of the abstract operators using our
verification condition `gen` and `sro` from the paper.

```
cd $AGNIDIR
mkdir $VERIFRESULTSDIR
cd $AGNIDIR/bpf-verification
python3 src/bpf_alu_jmp_synthesis.py \
            --kernver 6.10 \
            --encodings_path $ENCODINGSDIR \
            --res_path $VERIFRESULTSDIR
            --ver_set BPF_AND
```

Sample output:
```
--------------------------------------------------------------
                2.1(a) Executing gen verification
--------------------------------------------------------------

1/1 Verifying BPF_AND...
1/1 BPF_AND Done.
Instruction: BPF_AND, Execution time: 2.068349599838257, Violated domains: []
gen Verification Complete
+-------------+--------+-----+-----+------+-----+-----+--------------------------+
| Instruction | Sound? | u64 | s64 | tnum | u32 | s32 | Execution time (seconds) |
+-------------+--------+-----+-----+------+-----+-----+--------------------------+
|   BPF_AND   |   ✓    |  ✓  |  ✓  |  ✓   |  ✓  |  ✓  |           2.07           |
+-------------+--------+-----+-----+------+-----+-----+--------------------------+

--------------------------------------------------------------
                2.1(b) Executing sro verification
--------------------------------------------------------------

sro Verification Complete
+-------------+--------+-----+-----+------+-----+-----+--------------------------+
| Instruction | Sound? | u64 | s64 | tnum | u32 | s32 | Execution time (seconds) |
+-------------+--------+-----+-----+------+-----+-----+--------------------------+
+-------------+--------+-----+-----+------+-----+-----+--------------------------+


Verification Aggregate Statistics
+---------+------------+------------+-----------+-----------+-----------------+-----------------+
| KernVer | gen Sound? | sro Sound? | gen Viol. | sro Viol. | gen Unsound Ops | sro Unsound Ops |
+---------+------------+------------+-----------+-----------+-----------------+-----------------+
|   6.10  |     ✓      |     ✓      |     0     |     0     |        0        |        0        |
+---------+------------+------------+-----------+-----------+-----------------+-----------------+
```

The output shows that first, `BPF_AND` was checked for soundncess
using the `gen` verification condition. It shows that Agni checked for
soundness in all the abstract domains `u64`, `s64`, `tnum`, `u32`,
`s32`, and found the the output produed by the abstract `BPF_AND` 
operator was sound for all the abstract domains.