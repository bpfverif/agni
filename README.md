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


## Verification and POC synthesis for eBPF range analysis 
In this experiment we verify the correctness of the ebpf range analysis and
produce POCs for unsound instructions for kernel version 5.9. We give a short
version and a long version of the experiment. The short version should take a
few minutes and the long version should take roughly 5 hours. 

### Run the script
The following script invokes a python script which performs the verification 
and synthesis for any set of instructions and any kernel version

Short Version:
```
cd bpf_verification/src
python3 bpf_alu_jmp_synthesis.py --kernver 5.9 --encodings_path /home/matan/bpfverif/bpf_synthesis/bpf_encodings/5.9.auto --ver_set BPF_OR BPF_AND BPF_JSGT BPF_JSLT
```

Long Version:
```
cd bpf_verification/src
python3 bpf_alu_jmp_synthesis.py --kernver 5.9 --encodings_path /home/matan/bpfverif/bpf_synthesis/bpf_encodings/5.9.auto 
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


### Expected Result for Long Version
The two aggregate tables produced by the script (one for verification and one for synthesis) should exactly match the
specific row from the table (kernel version 5.9) in Fig.5(a) and Fig.5(b), respectively.