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
