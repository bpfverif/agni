# Verifying the Verifier: eBPF Range Analysis Verification

## Abstract
This paper proposes an automated method to check the correctness of range analysis used in the Linux Kernel’s eBPF verifier. We provide the specification of soundness for range analysis performed by the eBPF verifier. We automatically generate verification conditions that encode the operation of eBPF verifier directly from the Linux Kernel’s C source code and check it against our specification. When we discover instances where the eBPF verifier is unsound, we propose a method to generate an eBPF program that demonstrates the mismatch between the abstract and the concrete semantics. Our prototype automatically checks the soundness of 16 versions of the eBPF verifier in the Linux Kernel versions ranging from 4.14 to 5.19. In this process, we have discovered new bugs in older versions and proved the soundness of range analysis in the latest version of the Linux kernel.

--------------------------------------------------------------------------------

### Prerequisites to run the artifact.

1.  Install Docker if not already installed by following the documentation [here](https://docs.docker.com/install/). You might need to follow the post installation steps for managing docker as a non-root user [here](https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user).

2.  Install Virtual Box if not already installed by downloading from [here](https://www.virtualbox.org/wiki/Downloads).

### Claims to validate/reproduce.

1. Automatically extracting the semantics of the Linux kernel's C code to SMT (Docker).
2.  1. Verifying the kernel's range analysis using our `gen` and `sro` verification conditions (Docker).
    2. Synthesizing proof-of-concept BPF programs demonstrate a mismatch between the concrete and abstract semantics (Docker).
3.  Running our synthesized proof-of-concept BPF programs to witness unsound behaviour in a real Linux kernel (Virtual Box).

`Note`. To make it feasible to run the artifact quickly, we have reduced the sample sizes used for the experiments. The experiments for the paper were performed without using any containers, and on larger inputs sizes. It should take roughly 4-5 hours to evaluate this artifact. 

### Known issues.
We have tested the Docker image and the Virtual Box appliance on `x86_64` machines, running Linux and Windows operating systems.  We have no known issues to report.

--------------------------------------------------------------------------------

## 1. Automatically extracting the semantics of the Linux kernel's C code to SMT (25 minutes)

Here, we demonstrate how our tool can be used to *automatically* extract the semantics of the Linux Kernel verifier's C code as described in our paper (§5). Our tool produces the first-order logic formula (in [SMT-LIB](https://smtlib.cs.uiowa.edu/papers/smt-lib-reference-v2.6-r2021-05-12.pdf) format) for the abstract semantics defined in Linux Kernel for each eBPF instruction. For this review, we will use kernel v5.9

### Run the script

```
cd llvm-to-smt
python3 generate_encodings.py --llvmdir /usr/lib/llvm-12 --kernver 5.9 --outdir ~/bpf_encodings --logdir ~/bpf_encodings --kernbasedir ~/linux-stable --scriptsdir ~/llvm-to-smt/llvm-passes
```


### Expected Result 
```
Log file: /home/matan/bpfverif/cav23-artifact/llvm-to-smt/log_dir/log_23_29_26_04_2023.log
Log error file: /home/matan/bpfverif/cav23-artifact/llvm-to-smt/log_dir/log_err_23_29_26_04_2023.log
Create output directory: /home/matan/bpfverif/cav23-artifact/llvm-to-smt/encodings ... done
Change to kernel directory: /home/matan/test/linux-stable ... done
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
Getting encoding for BPF_RSH ... done
Getting encoding for BPF_ARSH ... done
Getting encoding for BPF_XOR ... done
Getting encoding for BPF_ADD_32 ... done
Getting encoding for BPF_SUB_32 ... done
Getting encoding for BPF_OR_32 ... done
Getting encoding for BPF_AND_32 ... done
Getting encoding for BPF_LSH_32 ... done
Getting encoding for BPF_RSH_32 ... done
Getting encoding for BPF_ARSH_32 ... done
Getting encoding for BPF_XOR_32 ... done
Getting encoding for BPF_JEQ ... done
Getting encoding for BPF_JNE ... done
Getting encoding for BPF_JGE ... done
Getting encoding for BPF_JGT ... done
Getting encoding for BPF_JSGE ... done
Getting encoding for BPF_JSGT ... done
Getting encoding for BPF_JLE ... done
Getting encoding for BPF_JLT ... done
Getting encoding for BPF_JSLE ... done
Getting encoding for BPF_JSLT ... done
Getting encoding for BPF_JEQ_32 ... done
Getting encoding for BPF_JNE_32 ... done
Getting encoding for BPF_JGE_32 ... done
Getting encoding for BPF_JGT_32 ... done
Getting encoding for BPF_JSGE_32 ... done
Getting encoding for BPF_JSGT_32 ... done
Getting encoding for BPF_JLE_32 ... done
Getting encoding for BPF_JLT_32 ... done
Getting encoding for BPF_JSLE_32 ... done
Getting encoding for BPF_JSLT_32 ... done
Getting encoding for BPF_SYNC ... done
```


### Explanation
Our automatic encoder produces an SMT-LIB (`.smt2`) file for each eBPF instruction which captures the Linux Kernel's abstract semantics that instruction. The encodings should be present in the directory specified by `--outdir`, in our case `~/bpf_encodings`.

```
ls bpf_encodings
...
```

### Source code structure





--------------------------------------------------------------------------------

## Verification and POC synthesis for eBPF range analysis (3-4 hours)
In the paper, we verify the soundness of the eBPF verifier's range analysis. To do this for a given kernel version, we check the correctness of 36 abstract operators using our verification conditions gen (§4.1) and sro (§4.2). When our soundness checks fail, we synthesis a concrete proof-of-concept (PoC) program that demonstrates the mismatch between abstract values maintained by the verifier and the concrete execution of the eBPF program. To keep the experiment short, we will make the following simplifications to the experiment:

- We will only run the experiment for kernel version 5.9
- For kernel version 5.9, checking all the eBPF operators for soundness take a long time (~12 hours). In this experiment, we provide a script which will accept a reduced list of eBPF operators which are known to be unsound. The experiment will then confirm that the reduced list of eBPF operators is indeed unsound.
- The synthesized PoC programs will be for demonstrative purposes since constructing a full BPF program from our generated POCs requires some manual effort. For the review, we will forgo this step. We directly provide the reviewers with constructed eBPF programs that manifest unsound behaviors. 


### Run the script
The script `bpf_alu_jmp_synthesis.py` performs the verification and synthesis for a specific set of instructions and a specific kernel version.
To make the verification faster, we will choose only those operators which are known to be unsound.

```
cd bpf_verification/src
python3 bpf_alu_jmp_synthesis.py --kernver 5.9 --encodings_path /home/cav23-artifact/bpf-encodings --ver_set BPF_AND_32 BPF_SUB BPF_JGT BPF_JSLE BPF_JEQ BPF_JNE BPF_JSGT BPF_JSGE BPF_OR_32 BPF_JLT BPF_OR BPF_AND BPF_JGE BPF_JSLT BPF_JLE 
```

### Expected Result for Short Version

The results should be similar to the output given below - note that the order of
instruction verification and synthesis might differ but the tables should be the same.

```
--------------------------------------------------------------
                EXECUTING GEN VERIFICATION
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
| Instruction | Sound? | U64 | S64 | Tnum | U32 | S32 | Execution time (seconds) |
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
                EXECUTING SRO VERIFICATION
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
| Instruction | Sound? | U64 | S64 | Tnum | U32 | S32 | Execution time (seconds) |
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
                VERIFICATION AGGREGATE STATISTICS
--------------------------------------------------------------

+----------------+------------+------------+----------------+---------------+-----------------------+-----------------------+
| Kernel Version | Gen Sound? | Sro Sound? | Gen Violations | Sro Violation | Gen Unsound Operators | Sro Unsound Operators |
+----------------+------------+------------+----------------+---------------+-----------------------+-----------------------+
|      5.9       |     ✘      |     ✘      |       67       |       65      |           15          |           15          |
+----------------+------------+------------+----------------+---------------+-----------------------+-----------------------+

--------------------------------------------------------------
                GENERATING POC FOR DOMAIN VIOLATIONS
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
Synthesized program for BPF_JGT (unsigned_32). Instruction sequence: BPF_JGT 
Synthesized program for BPF_JGT (signed_32). Instruction sequence: BPF_JGT 
Synthesized program for BPF_JSGT (unsigned_64). Instruction sequence: BPF_JSGT 
Synthesized program for BPF_JSGT (signed_64). Instruction sequence: BPF_JSGT 
Synthesized program for BPF_JSGT (Tnum). Instruction sequence: BPF_JSGT 
Synthesized program for BPF_JSGT (unsigned_32). Instruction sequence: BPF_JSGT 
Synthesized program for BPF_JSGT (signed_32). Instruction sequence: BPF_JSGT 
Synthesized program for BPF_SUB (unsigned_64). Instruction sequence: BPF_SUB 
Synthesized program for BPF_SUB (signed_64). Instruction sequence: BPF_SUB 
Synthesized program for BPF_SUB (Tnum). Instruction sequence: BPF_SUB 
Synthesized program for BPF_JLE (signed_64). Instruction sequence: BPF_JLE 
Synthesized program for BPF_JLE (Tnum). Instruction sequence: BPF_JLE 
Synthesized program for BPF_JLE (unsigned_32). Instruction sequence: BPF_JLE 
Synthesized program for BPF_JLE (signed_32). Instruction sequence: BPF_JLE 
Synthesized program for BPF_JSGE (unsigned_64). Instruction sequence: BPF_JSGE 
Synthesized program for BPF_JSGE (signed_64). Instruction sequence: BPF_JSGE 
Synthesized program for BPF_JSGE (Tnum). Instruction sequence: BPF_JSGE 
Synthesized program for BPF_JSGE (unsigned_32). Instruction sequence: BPF_JSGE 
Synthesized program for BPF_JSGE (signed_32). Instruction sequence: BPF_JSGE 
Synthesized program for BPF_JSLE (unsigned_64). Instruction sequence: BPF_JSLE 
Synthesized program for BPF_JSLE (signed_64). Instruction sequence: BPF_JSLE 
Synthesized program for BPF_JSLE (Tnum). Instruction sequence: BPF_JSLE 
Synthesized program for BPF_JSLE (unsigned_32). Instruction sequence: BPF_JSLE 
Synthesized program for BPF_JSLE (signed_32). Instruction sequence: BPF_JSLE 
Synthesized program for BPF_JSLT (unsigned_64). Instruction sequence: BPF_JSLT 
Synthesized program for BPF_JSLT (signed_64). Instruction sequence: BPF_JSLT 
Synthesized program for BPF_JSLT (Tnum). Instruction sequence: BPF_JSLT 
Synthesized program for BPF_JSLT (unsigned_32). Instruction sequence: BPF_JSLT 
Synthesized program for BPF_JSLT (signed_32). Instruction sequence: BPF_JSLT 
Synthesized program for BPF_JNE (unsigned_64). Instruction sequence: BPF_JGE BPF_JNE 
Synthesized program for BPF_JNE (signed_64). Instruction sequence: BPF_JGE BPF_JNE 
Synthesized program for BPF_JNE (Tnum). Instruction sequence: BPF_JGE BPF_JNE 
Synthesized program for BPF_JNE (unsigned_32). Instruction sequence: BPF_JGE BPF_JNE 
Synthesized program for BPF_JNE (signed_32). Instruction sequence: BPF_JGE BPF_JNE 
Synthesized program for BPF_JEQ (unsigned_64). Instruction sequence: BPF_JGE BPF_JEQ 
Synthesized program for BPF_JEQ (signed_64). Instruction sequence: BPF_JGE BPF_JEQ 
Synthesized program for BPF_JEQ (Tnum). Instruction sequence: BPF_JGE BPF_JEQ 
Synthesized program for BPF_JEQ (unsigned_32). Instruction sequence: BPF_JGE BPF_JEQ 
Synthesized program for BPF_JEQ (signed_32). Instruction sequence: BPF_JGE BPF_JEQ 
Synthesized program for BPF_JLT (unsigned_64). Instruction sequence: BPF_JGE BPF_JLT 
Synthesized program for BPF_JGE (unsigned_64). Instruction sequence: BPF_JGE BPF_JGE 
Synthesized program for BPF_AND (unsigned_32). Instruction sequence: BPF_JGE BPF_AND 
Synthesized program for BPF_AND (signed_32). Instruction sequence: BPF_JGE BPF_AND 
Synthesized program for BPF_JGT (unsigned_64). Instruction sequence: BPF_JGE BPF_JGT 
Synthesized program for BPF_AND_32 (unsigned_64). Instruction sequence: BPF_JGE BPF_AND_32 
Synthesized program for BPF_AND_32 (signed_64). Instruction sequence: BPF_JGE BPF_AND_32 
Synthesized program for BPF_AND_32 (unsigned_32). Instruction sequence: BPF_JGE BPF_AND_32 
Synthesized program for BPF_AND_32 (signed_32). Instruction sequence: BPF_JGE BPF_AND_32 
Synthesized program for BPF_JLE (unsigned_64). Instruction sequence: BPF_JGE BPF_JLE 
Synthesized program for BPF_OR_32 (unsigned_64). Instruction sequence: BPF_JSLE BPF_OR_32 
Synthesized program for BPF_OR_32 (signed_64). Instruction sequence: BPF_JSLE BPF_OR_32 
Synthesized program for BPF_OR_32 (unsigned_32). Instruction sequence: BPF_JSLE BPF_OR_32 
Synthesized program for BPF_OR_32 (signed_32). Instruction sequence: BPF_JSLE BPF_OR_32 
Synthesized program for BPF_OR (unsigned_32). Instruction sequence: BPF_JSLE BPF_OR 
Synthesized program for BPF_OR (signed_32). Instruction sequence: BPF_JSLE BPF_OR 

--------------------------------------------------------------
                SYNTHESIS AGGREGATE STATISTICS
--------------------------------------------------------------

+----------------+-------------------------+-----------------------+---------------+---------------+---------------+
| Kernel Version | Num of Total Violations | ALL POCs Synthesized? | Prog length 1 | Prog length 2 | Prog length 3 |
+----------------+-------------------------+-----------------------+---------------+---------------+---------------+
|      5.9       |            65           |           ✓           |       39      |       26      |       0       |
+----------------+-------------------------+-----------------------+---------------+---------------+---------------+

```

### Long Version (Optional)
```
cd bpf_verification/src
python3 bpf_alu_jmp_synthesis.py --kernver 5.9 --encodings_path /home/cav23-artifact/bpf-encodings 
```

### Expected Result for Long Version
The two aggregate tables produced by the script, one for verification and one
for synthesis, should exactly match the specific row from the table (kernel
version 5.9) in Fig.5(a) and Fig.5(b), respectively.


### Explanation
The automated verification and synthesis is done using
[z3py](https://ericpony.github.io/z3py-tutorial/guide-examples.htm). Our
procedure first attempts to verify given instructions and notes which abstract
domains are being violated for each instruction. As described by our paper, we
first perform GEN verification and then in SRO verification. Any instruction
that fails SRO verification will then be included in the synthesis procedure
where POCs will be generated for unsound instructions based on the domain
violations discovered in the SRO verification.

### Source code structure
We use one script `bpf_alu_jmp_synthesis.py` to call three modules which perform
verification and synthesis. Two modules are used for performing verification,
one for gen (`wf_soundness.py`) and one for sro(`sync_soundness.py`), and one
more module for synthesis(`synthesize_bug_types.py`) - these can be found in the
src directory under bpf_verification. Each of these modules uses the encodings
produced by our llvm-to-smt procedure to verify instructions or synthesize POCs.
Our verification conditions and concrete semantics for bpf instructions are
contained within the `verification_synth_module` class included in the shared
module library called `lib_reg_bounds_tracking.py` under the
lib_reg_bounds_tracking directory. We perform verification using z3 (by checking
if the solver returns `unsat`) and if verification fails we use z3 to produce a
counterexample program which serves as a POC. 

Our `bpf_alu_jmp_synthesis.py` script can be configured using various options
for verification and synthesis. These options can be changed by changing our
configuration `verification_synth_setup_config.toml` file or by passing argparse
arguments to the script which we show below, otherwise default values will be
assumed. While our experiment gives particular instructions for testing kernel
version 5.9, any kernel version, and any instruction of interest, can be tested
using our script `bpf_alu_jmp_synthesis.py`. For example, if we want to test one
instruction, `BPF_ADD`, in kernel version 5.10 we can use the following command:

```
python3 bpf_alu_jmp_synthesis.py --kernver 5.10 --encodings_path <path to 5.10 encodings directory> --ver_set BPF ADD
```
If we want to test 2 instructions or more we add them sequentially as follows:
```
python3 bpf_alu_jmp_synthesis.py --kernver 5.10 --encodings_path <path to 5.10 encodings directory> --ver_set BPF_ADD BPF_OR BPF_AND 
```
We make a distinction between the verification set - which is the set of instructions used for verification and POC generation in case of failure - and the synthesis set which is solely used for synthesizing POCs for instructions given in the verification set. We set a default synthesis set which is able to produce POCs as described by our paper but can be changed in the following way:
```
python3 bpf_alu_jmp_synthesis.py --kernver 5.11 --encodings_path <path to 5.11 encodings directory> --ver_set BPF ADD --synth_set BPF_XOR BPF_OR
```
Changing the synthesis set in this case means that only those instructions (BPF_XOR and BPF_OR) will be used in a multi-sequence program when generating a POC for BPF_ADD. 

For more on config options, use the following command:
```
python3 bpf_alu_jmp_synthesis.py -h
```


sub 264
```#2
6: (1f) r1 -= r2
7: R1(id=0,smin_value=3550221988887957680,smax_value=3550221988887957679,umin_value=3550221988887957680,umax_value=3550221988887957679,var_off=(0x3144ec1600000000; 0xffffffff),s32_min_value=-2147483648,s32_max_value=2147483647,u32_min_value=0,u32_max_value=-1) R2(id=0,smin_value=-9223372036854775808,smax_value=9223372036854775807,umin_value=0,umax_value=18446744073709551615,var_off=(0x0; 0xffffffffffffffff),s32_min_value=-2147483648,s32_max_value=2147483647,u32_min_value=0,u32_max_value=-1) R10(id=0,smin_value=0,smax_value=0,umin_value=0,umax_value=0,var_off=(0x0; 0x0),s32_min_value=0,s32_max_value=0,u32_min_value=0,u32_max_value=0)
```

![alt text for screen readers](or_s32.jpg "Text to show on mouseover").
![alt text for screen readers](sub_s64.jpg "Text to show on mouseover").

