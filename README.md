# Verifying the Verifier: eBPF Range Analysis Verification"

## Abstract
This paper proposes an automated method to check the correctness of range analysis used in the Linux Kernel’s eBPF verifier. We provide the specification of soundness for range analysis performed by the eBPF verifier. We automatically generate verification conditions that encode the operation of eBPF verifier directly from the Linux Kernel’s C source code and check it against our specification. When we discover instances where the eBPF verifier is unsound, we propose a method to generate an eBPF program that demonstrates the mismatch between the abstract and the concrete semantics. Our prototype automatically checks the soundness of 16 versions of the eBPF verifier in the Linux Kernel versions ranging from 4.14 to 5.19. In this process, we have discovered new bugs in older versions and proved the soundness of range analysis in the latest version of the Linux kernel.

--------------------------------------------------------------------------------

## Claims to validate/reproduce.

1. Automatically extracting the semantics of the Linux kernel's C code to SMT 
2. Verification of the kernel's range analysis using our `gen` and `sro` verification conditions. 
3. Synthesizing proof-of-concept BPF programs demonstrate a mismatch between the concrete and abstract semantics

`Note`. To make it feasible to run the artifact quickly, we have reduced the sample sizes used for the experiments. The experiments for the paper were performed without using any containers, and on larger inputs sizes. It should take roughly 5 hours to evaluate this artifact.

--------------------------------------------------------------------------------

## Instructions to run the artifact.

### Downloading prebuilt Docker Image

1. Install docker if it is not installed already by following the documentation [here](https://docs.docker.com/install/). You might need to follow the post installation steps for managing docker as a non-root user [here](https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user).

2.  Run the docker image:
```
docker run -it mys35/tnums-cgo22
cd tnums-cgo22
```
### Known issues. 
We have tested the docker image on different architectures (`x86_64`, `amd64`) and have no known issues to report.

--------------------------------------------------------------------------------

## Automatically extracting the semantics of the Linux kernel's C code to SMT 

Here, we demonstrate our tool can be used to *automatically* extract the semantics of the kernel's C code. 

--------------------------------------------------------------------------------

## Verification and POC synthesis for eBPF range analysis 
In the paper, we verify the soundness of the eBPF verifier's range analysis. To do this for a given kernel version, we check the correctness of 36 abstract operators using our verification conditions gen (§4.1) and sro (§4.2). When our soundness checks fail, we synthesis a concrete proof-of-concept (PoC) program that demonstrates the mismatch between abstract values maintained by the verifier and the concrete execution of the eBPF program. To keep the experiment short, we will make the following simplifications to the experiment:

- We will only run the experiment for kernel version 5.9
- For kernel version 5.9, checking all the eBPF operators for soundness take a long time (~12 hours). In this experiment, we provide a script which will accept a reduced list of eBPF operators which are known to be unsound. The experiment will then confirm that the reduced list of eBPF operators is indeed unsound.
- The synthesies PoC programs will be for demonstrative purposes only. To go from a PoC to an actual program requires some manual effort. For the review, will will avoid this step. We directly provide the reviwers with constructed eBPF programs that manifest unsound behaviors. 


### Run the script
The script `bpf_alu_jmp_synthesis.py` performs the verification and synthesis for a specific set of instructions and a specific kernel version.
To make the verification faster, we will choose only those operators which are known to be unsound.

```
cd bpf_verification/src
python3 bpf_alu_jmp_synthesis.py --kernver 5.9 --encodings_path /home/matan/bpfverif/bpf_synthesis/bpf_encodings/5.9.auto --ver_set BPF_AND_32 BPF_SUB BPF_JGT BPF_JSLE BPF_JEQ BPF_JNE BPF_JSGT BPF_JSGE BPF_OR_32 BPF_JLT BPF_OR BPF_AND BPF_JGE BPF_JSLT BPF_JLE 
```

### Expected Result for Short Version

The results should be similar to the output given below - note that the order of
instruction verification and synthesis might differ but the tables should be the same.

```
--------------------------------------------------------------
                EXECUTING GEN VERIFICATION
--------------------------------------------------------------

1/4 Verifying BPF_OR ...  Done.
2/4 Verifying BPF_JSGT ...  Done.
3/4 Verifying BPF_JSLT ...  Done.
4/4 Verifying BPF_AND ...  Done.
Gen Verification Complete
+-------------+--------+-----+-----+------+-----+-----+--------------------------+
| Instruction | Sound? | U64 | S64 | Tnum | U32 | S32 | Execution time (seconds) |
+-------------+--------+-----+-----+------+-----+-----+--------------------------+
|    BPF_OR   |   ✘    |  ✓  |  ✘  |  ✓   |  ✘  |  ✘  |           8.2            |
|   BPF_JSGT  |   ✘    |  ✘  |  ✘  |  ✘   |  ✘  |  ✘  |          58.87           |
|   BPF_JSLT  |   ✘    |  ✘  |  ✘  |  ✘   |  ✘  |  ✘  |          37.61           |
|   BPF_AND   |   ✘    |  ✓  |  ✘  |  ✓   |  ✘  |  ✘  |           9.9            |
+-------------+--------+-----+-----+------+-----+-----+--------------------------+

--------------------------------------------------------------
                EXECUTING SRO VERIFICATION
--------------------------------------------------------------

1/4 Verifying BPF_OR ...  Done.
2/4 Verifying BPF_JSGT ...  Done.
3/4 Verifying BPF_JSLT ...  Done.
4/4 Verifying BPF_AND ...  Done.
SRO Verification Complete
+-------------+--------+-----+-----+------+-----+-----+--------------------------+
| Instruction | Sound? | U64 | S64 | Tnum | U32 | S32 | Execution time (seconds) |
+-------------+--------+-----+-----+------+-----+-----+--------------------------+
|    BPF_OR   |   ✘    |  ✓  |  ✓  |  ✓   |  ✘  |  ✘  |          15.56           |
|   BPF_JSGT  |   ✘    |  ✘  |  ✘  |  ✘   |  ✘  |  ✘  |          52.02           |
|   BPF_JSLT  |   ✘    |  ✘  |  ✘  |  ✘   |  ✘  |  ✘  |          41.98           |
|   BPF_AND   |   ✘    |  ✓  |  ✓  |  ✓   |  ✘  |  ✘  |          18.24           |
+-------------+--------+-----+-----+------+-----+-----+--------------------------+

--------------------------------------------------------------
                VERIFICATION AGGREGATE STATISTICS
--------------------------------------------------------------

+----------------+------------+------------+----------------+---------------+-----------------------+-----------------------+
| Kernel Version | Gen Sound? | Sro Sound? | Gen Violations | Sro Violation | Gen Unsound Operators | Sro Unsound Operators |
+----------------+------------+------------+----------------+---------------+-----------------------+-----------------------+
|      5.9       |     ✘      |     ✘      |       16       |       14      |           4           |           4           |
+----------------+------------+------------+----------------+---------------+-----------------------+-----------------------+

--------------------------------------------------------------
                GENERATING POC FOR DOMAIN VIOLATIONS
--------------------------------------------------------------


Synthesized program for BPF_JSGT (unsigned_64). Instruction sequence: BPF_JSGT 
Synthesized program for BPF_JSGT (signed_64). Instruction sequence: BPF_JSGT 
Synthesized program for BPF_JSGT (Tnum). Instruction sequence: BPF_JSGT 
Synthesized program for BPF_JSGT (unsigned_32). Instruction sequence: BPF_JSGT 
Synthesized program for BPF_JSGT (signed_32). Instruction sequence: BPF_JSGT 
Synthesized program for BPF_JSLT (unsigned_64). Instruction sequence: BPF_JSLT 
Synthesized program for BPF_JSLT (signed_64). Instruction sequence: BPF_JSLT 
Synthesized program for BPF_JSLT (Tnum). Instruction sequence: BPF_JSLT 
Synthesized program for BPF_JSLT (unsigned_32). Instruction sequence: BPF_JSLT 
Synthesized program for BPF_JSLT (signed_32). Instruction sequence: BPF_JSLT 
Synthesized program for BPF_OR (unsigned_32). Instruction sequence: BPF_JSLE BPF_OR 
Synthesized program for BPF_OR (signed_32). Instruction sequence: BPF_JSLE BPF_OR 
Synthesized program for BPF_AND (unsigned_32). Instruction sequence: BPF_JSLE BPF_AND 
Synthesized program for BPF_AND (signed_32). Instruction sequence: BPF_JSLE BPF_AND 

--------------------------------------------------------------
                SYNTHESIS AGGREGATE STATISTICS
--------------------------------------------------------------

+----------------+-------------------------+-----------------------+---------------+---------------+---------------+
| Kernel Version | Num of Total Violations | ALL POCs Synthesized? | Prog length 1 | Prog length 2 | Prog length 3 |
+----------------+-------------------------+-----------------------+---------------+---------------+---------------+
|      5.9       |            14           |           ✓           |       10      |       4       |       0       |
+----------------+-------------------------+-----------------------+---------------+---------------+---------------+
```

### Long Version (Optional)
```
cd bpf_verification/src
python3 bpf_alu_jmp_synthesis.py --kernver 5.9 --encodings_path /home/matan/bpfverif/bpf_synthesis/bpf_encodings/5.9.auto 
```

### Expected Result for Long Version
The two aggregate tables produced by the script (one for verification and one for synthesis) should exactly match the
specific row from the table (kernel version 5.9) in Fig.5(a) and Fig.5(b), respectively.


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
python3 bpf_alu_jmp_synthesis.py --kernver 5.10 --encodings_path <path to 5.10 encodings directory>--ver_set BPF_ADD BPF_OR BPF_AND 
```
We make a distinction between the verification set - which is used to check correctness of given instructions and produce POCs for them in case of failure - and the synthesis set which is solely used for synthesizing POCs for instructions given in the verification set. We set a default synthesis set which is able to produce POCs as described by our paper but can be changed in the following way:
```
python3 bpf_alu_jmp_synthesis.py --kernver 5.10 --ver_set BPF ADD --synth_set BPF_XOR BPF_OR
```
Changing the synthesis set in this case means that only those instructions (BPF_XOR and BPF_OR) will be used in a multi-sequence program when generating a POC for BPF_ADD. 

For more on config options, use the following command:
```
python3 bpf_alu_jmp_synthesis.py -h
```
