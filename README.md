# Verifying the Verifier: eBPF Range Analysis Verification

### Abstract
Our paper proposes an automated method to check the
correctness of range analysis used in the Linux Kernel’s
eBPF verifier. In this artifact, we provide our software
that (a) automatically extracts the abstract semantics of
the range analysis from the C code, (b) generates the
verification conditions for the soundness of the range
analysis and checks the verifier's range analysis for
soundness, and (c) synthesizes an eBPF program that
demonstrates the mismatch between the abstract and the
concrete semantics in the case where the range analysis
fails to meet the soundness condition.

### Availability
This artifact is publicly available at zenodo. DOI: TODO

### Functionality
The entire set of experiments require roughly 6 days to
complete. To keep the evaluation short, we demonstrate how
to replicate a smaller subset of the results. We show that
our results are indeed consistent with our paper for this
subset. In practice, our artifact can be used to replicate
the full set of results from the paper.

### Reusability
Our artifact is open source with the MIT License. TODO.
While we provide a docker image with all the dependencies,
it is portable in essence to different environments. 

--------------------------------------------------------------------------------

### Prerequisites to run the artifact.

1.  Install Docker if not already installed by following the
    documentation [here](https://docs.docker.com/install/).
    You might need to follow the post installation steps for
    managing docker as a non-root user
    [here](https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user).

2.  Install Virtual Box if not already installed by
    downloading from
    [here](https://www.virtualbox.org/wiki/Downloads).

### Claims to validate/reproduce.

1. Automatically extracting the semantics of the Linux
   kernel's C code to SMT (Docker).
2.  1. Verifying the kernel's range analysis using our `gen`
       and `sro` verification conditions (Docker).
    2. Synthesizing proof-of-concept BPF programs
       demonstrate a mismatch between the concrete and
       abstract semantics (Docker).
3.  Running our synthesized proof-of-concept BPF programs to
    witness unsound behaviour in a real Linux kernel
    (Virtual Box).

`Note`. To make it feasible to run the artifact quickly and with minimal
resources, we have limited our experiments to one kernel version and a specific
subset of bpf instructions. The experiments for the paper were performed without
using any containers, and on more instructions. It should take roughly 4-5
hours to evaluate this artifact. 


## System requirements and known issues.
We have tested the Docker image and the Virtual Box
appliance on `x86_64` machines, running Linux and Windows
operating systems. We have no known issues to report.

--------------------------------------------------------------------------------

## (1.) Automatically extracting the semantics of the Linux kernel's C code to SMT (25 minutes)

Here, we demonstrate how our tool can be used to
*automatically* extract the semantics of the Linux Kernel
verifier's C code as described in our paper (§5). Our tool
produces the first-order logic formula (in
[SMT-LIB](https://smtlib.cs.uiowa.edu/papers/smt-lib-reference-v2.6-r2021-05-12.pdf)
format) for the abstract semantics defined in Linux Kernel
for each eBPF instruction. We demonstrate our tool on kernel
v5.9. Within docker, the source code for the 5.9 Linux
kernel is present in `/home/linux-stable/`

### Load and run the docker image
```
docker load < cav23-artifact-docker.tar  
docker run -it cav23-artifact
```
### Inside docker, create the output directory 
```
cd /home/cav23-artifact
mkdir bpf-encodings-5.9
```

### Run the llvm-to-smt tool 

```
cd /home/cav23-artifact/llvm-to-smt
python3 generate_encodings.py --kernver 5.9 --kernbasedir /home/linux-stable \
  --outdir /home/cav23-artifact/bpf-encodings-5.9
```

### Expected Result 
```
Log file: /home/cav23-artifact/bpf-encodings-5.9/log_21_58_27_04_2023.log
Log error file: /home/cav23-artifact/bpf-encodings-5.9/log_err_21_58_27_04_2023.log
Change to kernel directory: /home/linux-stable ... done
Checkout kernel version v5.9 ... done
Run make config and edit BPF flags ... done
Extract compile flags for current kernel version ... done
Edit tnum.c and verifier.c to add wrappers ... done
Compile verifier.c and tnum.c ... done
Link verifier.ll and tnum.ll to single verifier.ll ... done
Getting encoding for BPF_ADD ... done
Getting encoding for BPF_SUB ... done
Getting encoding for BPF_OR ... done
Getting encoding for BPF_AND ... done
Getting encoding for BPF_LSH ... done
.
.
.
Getting encoding for BPF_SYNC ... done
```

### Explanation
Our automatic encoder produces an SMT-LIB (`.smt2`) file for
each eBPF instruction in the output directory
(`/home/bpf-encodings-5.9`), that captures the Linux
Kernel's abstract semantics for the instruction.  We now
have the semantics of 36 abstract operators corresponding to
36 eBPF instructions.

```
root@847d5c0f8828:/home/cav23-artifact/llvm-to-smt# ls -1 /home/bpf-encodings-5.9/*.smt2
/home/bpf-encodings-5.9/BPF_ADD.smt2
/home/bpf-encodings-5.9/BPF_ADD_32.smt2
/home/bpf-encodings-5.9/BPF_AND.smt2
.
.
.
```

### Source code structure

```
llvm-to-smt
├── llvm-passes
│   ├── ForceFunctionEarlyExit
│   ├── InlineFunctionCalls
│   ├── LLVMToSMT
│   ├── PromoteMemcpy
│   ├── RemoveFunctionCalls
├── generate_encodings.py
├── run_llvm_passes.py
└── wrappers.py
```

The `llvm-to-smt` directory contains the top-level script
`generate_encodings.py`, which is essential for running our
tool. The `llvm-passes` subdirectory includes our LLVM
transformation passes and the required scripts for executing
the passes. Our tool performs the following steps:
- Checks out the specified kernel version 
- Edits the `verifier.c` file to add a stub function for
  each eBPF instruction that requires an SMT encoding.
- Extracts the compilation flags needed to convert the eBPF
  verifier kernel module to LLVM IR.
- Compiles `verifier.c` and `tnum.c` to `verifier.ll`.
- Applies the following LLVM passes from the `llvm-passes`
  subdirectory to transform the IR:
  `ForceFunctionEarlyExit`, `RemoveFunctionCalls`,
  `InlineFunctionCalls`, and `PromoteMemcpy`.
- Finally, runs the `LLVMToSMT` pass for each eBPF
  instruction to obtain the SMT encoding for it.

--------------------------------------------------------------------------------

## (2.1 & 2.2) Verification and POC synthesis for eBPF range analysis (3-4 hours)

We now check the correctness of the 36 abstract operators
using our verification conditions `gen` (§4.1) and `sro`
(§4.2). When our soundness checks fail, we synthesize
proof-of-concept (PoC) programs that demonstrate the
mismatch between abstract values maintained by the verifier
and the values in a concrete execution of the eBPF program.
To keep the experiment short, we will make the following
simplifications:

- We will only run the experiment for kernel v5.9
- Checking all the 36 eBPF operators for soundness take a
  long time (~12 hours) for kernel version 5.9. In this
  experiment, we provide a script which will accept a
  reduced list of eBPF instructions whose abstract semantics
  are known to be _unsound_. The experiment will then
  confirm that the reduced list of eBPF instructions are
  indeed unsound. This part addresses claim 2.1.
- The synthesized PoC programs will be for demonstrative
  purposes only. Constructing a full eBPF program from our
  generated POCs requires some manual effort. For the
  review, we will forgo this step. In part 3 of the artifact
  (later), we provide full eBPF programs constructed from
  the demonstrative examples that manifest unsound behaviors
  in an actual kernel. 

### Run the script to perform the verification and synthesis
The script uses the encodings we previously generated,
present in `/home/cav23-artifact/bpf-encodings-5.9`. The
`ver_set` argument is used to restrict our verification to a
reduced list of eBPF instructions.

```
cd /home/cav23-artifact/bpf-verification/src
python3 bpf_alu_jmp_synthesis.py --kernver 5.9 \
  --encodings_path /home/cav23-artifact/bpf-encodings-5.9 \
  --ver_set BPF_AND_32 BPF_SUB BPF_JGT BPF_JSLE BPF_JEQ BPF_JNE BPF_JSGT BPF_JSGE \
            BPF_OR_32 BPF_JLT BPF_OR BPF_AND BPF_JGE BPF_JSLT BPF_JLE 
```

### Expected result

The expected output should be similar to the one below. Note
that the order of instructions in the verification part and
the order of synthesized programs in the synthesis part
might differ. Each row in the tables however, should be the
same.

```
--------------------------------------------------------------
                2.1(a) Executing gen verification
--------------------------------------------------------------

1/15 Verifying BPF_JNE ...  Done.
2/15 Verifying BPF_JEQ ...  Done.
3/15 Verifying BPF_JLT ...  Done.
4/15 Verifying BPF_OR_32 ...  Done.
5/15 Verifying BPF_AND ...  Done.
6/15 Verifying BPF_JGE ...  Done.
7/15 Verifying BPF_JGT ...  Done.
8/15 Verifying BPF_JSGT ...  Done.
9/15 Verifying BPF_OR ...  Done.
10/15 Verifying BPF_SUB ...  Done.
11/15 Verifying BPF_AND_32 ...  Done.
12/15 Verifying BPF_JLE ...  Done.
13/15 Verifying BPF_JSGE ...  Done.
14/15 Verifying BPF_JSLE ...  Done.
15/15 Verifying BPF_JSLT ...  Done.
Gen Verification Complete
+-------------+--------+-----+-----+------+-----+-----+--------------------------+
| Instruction | Sound? | u64 | s64 | tnum | u32 | s32 | Execution time (seconds) |
+-------------+--------+-----+-----+------+-----+-----+--------------------------+
|   BPF_JNE   |   ✘    |  ✘  |  ✘  |  ✘   |  ✘  |  ✘  |          192.43          |
|   BPF_JEQ   |   ✘    |  ✘  |  ✘  |  ✘   |  ✘  |  ✘  |          89.32           |
|   BPF_JLT   |   ✘    |  ✘  |  ✘  |  ✘   |  ✘  |  ✘  |          55.04           |
|  BPF_OR_32  |   ✘    |  ✘  |  ✘  |  ✓   |  ✘  |  ✘  |           5.18           |
|   BPF_AND   |   ✘    |  ✓  |  ✘  |  ✓   |  ✘  |  ✘  |           9.53           |
|   BPF_JGE   |   ✘    |  ✘  |  ✘  |  ✘   |  ✘  |  ✘  |          33.15           |
|   BPF_JGT   |   ✘    |  ✘  |  ✘  |  ✘   |  ✘  |  ✘  |          42.89           |
|   BPF_JSGT  |   ✘    |  ✘  |  ✘  |  ✘   |  ✘  |  ✘  |           28.4           |
|    BPF_OR   |   ✘    |  ✓  |  ✘  |  ✓   |  ✘  |  ✘  |           9.21           |
|   BPF_SUB   |   ✘    |  ✘  |  ✘  |  ✘   |  ✓  |  ✓  |          116.87          |
|  BPF_AND_32 |   ✘    |  ✘  |  ✘  |  ✓   |  ✘  |  ✘  |           5.28           |
|   BPF_JLE   |   ✘    |  ✘  |  ✘  |  ✘   |  ✘  |  ✘  |          62.81           |
|   BPF_JSGE  |   ✘    |  ✘  |  ✘  |  ✘   |  ✘  |  ✘  |          38.35           |
|   BPF_JSLE  |   ✘    |  ✘  |  ✘  |  ✘   |  ✘  |  ✘  |          32.33           |
|   BPF_JSLT  |   ✘    |  ✘  |  ✘  |  ✘   |  ✘  |  ✘  |          50.91           |
+-------------+--------+-----+-----+------+-----+-----+--------------------------+

--------------------------------------------------------------
                2.1(b) Executing sro verification
--------------------------------------------------------------

1/15 Verifying BPF_JNE ...  Done.
2/15 Verifying BPF_JEQ ...  Done.
3/15 Verifying BPF_JLT ...  Done.
4/15 Verifying BPF_OR_32 ...  Done.
5/15 Verifying BPF_JGE ...  Done.
6/15 Verifying BPF_JGT ...  Done.
7/15 Verifying BPF_JSGT ...  Done.
8/15 Verifying BPF_OR ...  Done.
9/15 Verifying BPF_SUB ...  Done.
10/15 Verifying BPF_JSLE ...  Done.
11/15 Verifying BPF_AND_32 ...  Done.
12/15 Verifying BPF_JLE ...  Done.
13/15 Verifying BPF_JSGE ...  Done.
14/15 Verifying BPF_AND ...  Done.
15/15 Verifying BPF_JSLT ...  Done.
SRO Verification Complete
+-------------+--------+-----+-----+------+-----+-----+--------------------------+
| Instruction | Sound? | u64 | s64 | tnum | u32 | s32 | Execution time (seconds) |
+-------------+--------+-----+-----+------+-----+-----+--------------------------+
|   BPF_JNE   |   ✘    |  ✘  |  ✘  |  ✘   |  ✘  |  ✘  |          203.43          |
|   BPF_JEQ   |   ✘    |  ✘  |  ✘  |  ✘   |  ✘  |  ✘  |         3911.46          |
|   BPF_JLT   |   ✘    |  ✘  |  ✘  |  ✘   |  ✘  |  ✘  |          74.94           |
|  BPF_OR_32  |   ✘    |  ✘  |  ✘  |  ✓   |  ✘  |  ✘  |          17.38           |
|   BPF_JGE   |   ✘    |  ✘  |  ✘  |  ✘   |  ✘  |  ✘  |          120.62          |
|   BPF_JGT   |   ✘    |  ✘  |  ✘  |  ✘   |  ✘  |  ✘  |          225.68          |
|   BPF_JSGT  |   ✘    |  ✘  |  ✘  |  ✘   |  ✘  |  ✘  |          114.93          |
|    BPF_OR   |   ✘    |  ✓  |  ✓  |  ✓   |  ✘  |  ✘  |          26.93           |
|   BPF_SUB   |   ✘    |  ✘  |  ✘  |  ✘   |  ✓  |  ✓  |          213.83          |
|   BPF_JSLE  |   ✘    |  ✘  |  ✘  |  ✘   |  ✘  |  ✘  |          79.36           |
|  BPF_AND_32 |   ✘    |  ✘  |  ✘  |  ✓   |  ✘  |  ✘  |          22.71           |
|   BPF_JLE   |   ✘    |  ✘  |  ✘  |  ✘   |  ✘  |  ✘  |          103.7           |
|   BPF_JSGE  |   ✘    |  ✘  |  ✘  |  ✘   |  ✘  |  ✘  |          95.13           |
|   BPF_AND   |   ✘    |  ✓  |  ✓  |  ✓   |  ✘  |  ✘  |          31.16           |
|   BPF_JSLT  |   ✘    |  ✘  |  ✘  |  ✘   |  ✘  |  ✘  |          71.92           |
+-------------+--------+-----+-----+------+-----+-----+--------------------------+


--------------------------------------------------------------
                2.2 Generating POC for domain violations
--------------------------------------------------------------


Synthesized program for BPF_JLT (signed_64). Instruction sequence: BPF_JLT 
Synthesized program for BPF_JLT (Tnum). Instruction sequence: BPF_JLT 
Synthesized program for BPF_JLT (unsigned_32). Instruction sequence: BPF_JLT 
Synthesized program for BPF_JLT (signed_32). Instruction sequence: BPF_JLT 
Synthesized program for BPF_JGE (signed_64). Instruction sequence: BPF_JGE 
Synthesized program for BPF_JGE (Tnum). Instruction sequence: BPF_JGE 
Synthesized program for BPF_JGE (unsigned_32). Instruction sequence: BPF_JGE 
Synthesized program for BPF_JGE (signed_32). Instruction sequence: BPF_JGE 
Synthesized program for BPF_JGT (signed_64). Instruction sequence: BPF_JGT 
Synthesized program for BPF_JGT (Tnum). Instruction sequence: BPF_JGT 
.
.
.
Synthesized program for BPF_OR_32 (unsigned_64). Instruction sequence: BPF_JSLE BPF_OR_32 
Synthesized program for BPF_OR_32 (signed_64). Instruction sequence: BPF_JSLE BPF_OR_32 
Synthesized program for BPF_OR_32 (unsigned_32). Instruction sequence: BPF_JSLE BPF_OR_32 
Synthesized program for BPF_OR_32 (signed_32). Instruction sequence: BPF_JSLE BPF_OR_32 
Synthesized program for BPF_OR (unsigned_32). Instruction sequence: BPF_JSLE BPF_OR 
Synthesized program for BPF_OR (signed_32). Instruction sequence: BPF_JSLE BPF_OR 

========================================================================

Verification Aggregate Statistics
+---------+------------+------------+-----------+-----------+-----------------+-----------------+
| KernVer | gen Sound? | sro Sound? | gen Viol. | sro Viol. | gen Unsound Ops | sro Unsound Ops |
+---------+------------+------------+-----------+-----------+-----------------+-----------------+
|  5.9    |     ✘      |     ✘      |    67     |    65     |       15        |      15         |
+---------+------------+------------+-----------+-----------+-----------------+-----------------+

Synthesis Aggregate Statistics
+---------+--------------+-----------------------+------------+------------+------------+
| KernVer | # Tot. Viol. | All POCs Synthesized? | Prog Len 1 | Prog Len 2 | Prog Len 3 |
+---------+--------------+-----------------------+------------+------------+------------+
|  5.9    |    65        |           ✓           |    39      |     26     |     0      |
+---------+--------------+-----------------------+------------+------------+------------+
```

### Explanation
- The first part of this experiment `2.1(a) Executing gen verification`, 
corresponds to the verification on the set of
eBPF instructions using our `gen` verification condition.
The table at the end of this part denotes whether an
instruction was deemed sound (✓) or unsound (✘), and which
of the five abstract domains have been violated.
- The second part `2.1(b) EXECUTING sro VERIFICATION`
performs verification on the eBPF instructions that were
deemed unsound by the previous `gen` verification condition,
using our `sro` verification condition. It produces a
similar table as in the prior part.
- The third part `2.2 Generating POC for domain violations`
performs synthesis. It attempts to generate proof-of-concept
mini eBPF programs using instructions that were deemed
unsound by both the `gen` and `sro` verification conditions
from the previous steps. The programs manifest a mismatch
between verifier's abstract values and the concrete
execution, that is they demonstrate unsound behavior.
- Lastly, we provide two tables with aggregate statistics.
  - The first table `VERIFICATION AGGREGATE STATISTICS`
shows aggregate statistics for the verification part of the
experiment (2.1(a) and 2.1(b)). This table should match
exactly with Fig 5(a) (row kernel version 5.9) from the
paper. 
  - The second table `SYNTHESIS AGGREGATE STATISTICS`
summarizes the total number of unsound instructions + domain
pairs (i.e. the total number of violations). It also shows
whether the synthesis was successful in producing a program
for all the violations, as well as the respective program
lengths. This table should match with Fig. 5(b) from the
paper.

In general, each POC is documented in a separate log in
`/home/cav23-artifact/bpf-verification/results`. We use
these logs to manually craft a full eBPF program from the
output of the synthesis process.

### Long Version (Optional, ~13 hours)
```
cd bpf_verification/src
python3 bpf_alu_jmp_synthesis.py --kernver 5.9 \
  --encodings_path /home/cav23-artifact/bpf-encodings-5.9
```

### Expected Result for Long Version
The two aggregate tables produced by the script, one for verification and one
for synthesis, should exactly match the specific row from the table (according
to kernel version) in Fig.5(a) and Fig.5(b), respectively.


### Source code structure

```
bpf-verification/
├── lib_reg_bounds_tracking
│   └── lib_reg_bounds_tracking.py
└── src
    ├── bpf_alu_jmp_synthesis.py
    ├── sync_soundness.py
    ├── synthesize_bug_types.py
    ├── verification_synth_setup_config.toml
    └── wf_soundness.py

```

We use one script `bpf_alu_jmp_synthesis.py` to call three modules which perform
verification and synthesis; two modules are used for performing verification,
one for gen (`wf_soundness.py`) and one for sro(`sync_soundness.py`), and one
more module for synthesis(`synthesize_bug_types.py`). Each of these modules uses
the encodings produced by our llvm-to-smt procedure to verify instructions or
synthesize POCs. Our verification conditions and concrete semantics for bpf
instructions are contained within the `verification_synth_module` class included
in the shared module library called `lib_reg_bounds_tracking.py` under the
lib_reg_bounds_tracking directory. 

Our `bpf_alu_jmp_synthesis.py` script can be configured using various options
for verification and synthesis. These options can be changed in our
configuration `verification_synth_setup_config.toml` file or by passing argparse
arguments to the script which we show below; otherwise, default values will be
assumed. While our experiment gives particular instructions for testing kernel
version 5.9, any kernel version after 4.14, and any instruction of interest, can be tested
using our script `bpf_alu_jmp_synthesis.py`. For example, if we want to test one
instruction, `BPF_ADD`, in kernel version 5.10 we can use the following command:

```
python3 bpf_alu_jmp_synthesis.py --kernver 5.10 \
  --encodings_path <path to 5.10 encodings directory> \
  --ver_set BPF_ADD
```
If we want to test 2 instructions or more we add them sequentially as follows:
```
python3 bpf_alu_jmp_synthesis.py --kernver 5.10 \
  --encodings_path <path to 5.10 encodings directory> \
  --ver_set BPF_ADD BPF_OR BPF_AND 
```


## (3) Running synthesized eBPF programs in a real Linux Kernel (20 minutes)

In the previous experiment, we synthesized mini eBPF
programs. These programs are utilized to create a complete
eBPF program, which showcases a discrepancy between the
abstract values maintained by the verifier and the actual
execution of the eBPF program. Building a full eBPF program
requires some manual effort. However, to simplify the review
process, we offer pre-constructed eBPF programs that we have
created using the output from the synthesis. These programs
are available in our Virtual Box appliance named
cav23-artifact-vm.ova. This appliance contains a virtual
machine that operates on Ubuntu 20.04 and is equipped with
Linux Kernel v5.9.

### Import and start the virtual machine
- Open Virtual Box
- File > Import Appliance 
- Browse and select the path to `cav23-artifact-vm.ova`
- You should have the `cav23-artifact-vm` virtual machine imported and ready the sidebar.
- Double-click on it or press "Start" to start the VM.
- If prompted, choose "Ubuntu" in the grub boot menu. 
- The password for login is `cav23`.

### Setup

Open a terminal. The directory
`/home/cav23-reviewer/bpf_progs/` contains all the code
necessary to run our synthesized eBPF programs. These
programs are located in
`/home/cav23-reviewer/bpf_progs/pocs`. The naming convention
for these eBPF programs are
`<kernel_version>_<ebpf_isntruction>_<domain_violated>.c`.
Since our VM is installed with kernel version 5.9, we will
only work with the `5.9*` files.

```
ls /home/cav23-reviewer/bpf_progs/pocs/*.c
5.5_jne_tnum_manfred.c  5.5_jsle_umin.c     5.7rc1_arsh32_u64.c  
5.7rc1_xor32_u64.c      5.8_sub_s64.c       5.9_or_s32.c
5.5_jsgt32_tnum.c       5.7rc1_add32_u64.c  5.7rc1_jge32_u64.c   
5.8_jsgt_s32.c          5.9_jsgt_s32.c      5.9_sub_s64.c
```

### Run example eBPF program 1: a bug in 64-bit BPF_SUB

We will now run the `5.9_sub_s64.c` program. This program
causes the verifier's range tracking to reach an invalid
state. The verifier believes that the minimum possible value
in a register `smin_value` is greater than the maximum value
`smax_value`. This is clearly unsound.
```
cd /home/cav23-reviewer/bpf_progs/
cp pocs/5.9_sub_s64.c ./bpf_test.c
sudo make
./bpf_test 
```

The output should be somewhat similar to the one below.
Scroll down to the lines  named `7`. `smin_value` is indeed
greater than `smax_value`. 

!["BPF_SUB S64 Violation"](images/sub_s64.jpg "BPF_SUB S64 Violation") 

### Run example eBPF program 2: a bug in 32-bit BPF_OR

```
cd /home/cav23-reviewer/bpf_progs/
cp pocs/5.9_or_s32.c ./bpf_test.c
sudo make
./bpf_test 
```

Similar to the above program, this program demonstrates that
minimum possible value in a 32-bit sub register
`s32_min_value` is greater than the maximum 32-bit value
`s32_max_value`. This too, is clearly unsound.

!["BPF_OR S32 Violation"](images/or_s32.jpg "BPF_OR S32 Violation")

---
_Fin._