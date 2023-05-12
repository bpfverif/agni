import argparse
import pathlib
import subprocess
import sys

# list of instructions to be verified to be unsound
ver_set_dict = {
"4.14.214": ['BPF_OR_32', 'BPF_AND', 'BPF_SUB_32', 'BPF_ADD_32', 'BPF_LSH_32', 'BPF_LSH', 'BPF_RSH', 'BPF_RSH_32', 'BPF_OR'],
"5.5": ['BPF_JNE_32', 'BPF_JSLE_32', 'BPF_JLT_32', 'BPF_JGE_32', 'BPF_JSGE_32', 'BPF_JSLT_32', 'BPF_JEQ_32', 'BPF_JGT_32', 'BPF_JSGT_32', 'BPF_AND', 'BPF_OR', 'BPF_JLE_32'],
"5.7": ['BPF_JSGE', 'BPF_JLE', 'BPF_JSLT', 'BPF_JLT', 'BPF_JGE', 'BPF_JNE', 'BPF_OR_32', 'BPF_SUB', 'BPF_JSLE', 'BPF_JSGT', 'BPF_JGT', 'BPF_AND_32', 'BPF_JEQ', 'BPF_OR', 'BPF_AND'],
"5.7-rc1": ['BPF_JEQ', 'BPF_LSH_32', 'BPF_JLT_32', 'BPF_JLE_32', 'BPF_JGT_32', 'BPF_JSLT', 'BPF_AND_32', 'BPF_SUB', 'BPF_JSGT', 'BPF_ADD_32', 'BPF_OR', 'BPF_JGT', 'BPF_JSLT_32', 'BPF_JSLE', 'BPF_JGE_32', 'BPF_ARSH_32', 'BPF_JNE_32', 'BPF_SUB_32', 'BPF_JSGE', 'BPF_JGE', 'BPF_RSH_32', 'BPF_JLT', 'BPF_AND', 'BPF_JSGE_32', 'BPF_JSGT_32', 'BPF_JLE', 'BPF_XOR_32', 'BPF_OR_32', 'BPF_JEQ_32', 'BPF_JSLE_32', 'BPF_JNE'],
"5.8": ['BPF_JSGE', 'BPF_JLE', 'BPF_JNE', 'BPF_OR_32', 'BPF_JSLE', 'BPF_JSGT', 'BPF_JGE', 'BPF_JEQ', 'BPF_AND', 'BPF_JSLT', 'BPF_JLT', 'BPF_JGT', 'BPF_AND_32', 'BPF_SUB', 'BPF_OR'],
"5.9": ['BPF_AND_32', 'BPF_SUB', 'BPF_JLE', 'BPF_JSLE', 'BPF_JGT', 'BPF_JEQ', 'BPF_JNE', 'BPF_JSGT', 'BPF_JSGE', 'BPF_OR_32', 'BPF_JLT', 'BPF_OR', 'BPF_AND', 'BPF_JSLT', 'BPF_JGE'],
"5.10": ['BPF_JLE', 'BPF_JNE', 'BPF_JGT', 'BPF_SUB', 'BPF_XOR_32', 'BPF_JSLE', 'BPF_XOR', 'BPF_JSLT', 'BPF_AND_32', 'BPF_OR_32', 'BPF_JGE', 'BPF_JSGT', 'BPF_AND', 'BPF_JEQ', 'BPF_JSGE', 'BPF_OR', 'BPF_JLT'],
"5.10-rc1": ['BPF_JSLE', 'BPF_XOR_32', 'BPF_XOR', 'BPF_JEQ', 'BPF_SUB', 'BPF_JLE', 'BPF_JSGE', 'BPF_JSLT', 'BPF_OR_32', 'BPF_OR', 'BPF_AND_32', 'BPF_JGT', 'BPF_JGE', 'BPF_JSGT', 'BPF_JNE', 'BPF_AND', 'BPF_JLT'],
"5.11": ['BPF_JSLE', 'BPF_XOR_32', 'BPF_AND_32', 'BPF_JSLT', 'BPF_OR_32', 'BPF_OR', 'BPF_JSGE', 'BPF_AND', 'BPF_JNE', 'BPF_JGT', 'BPF_JLE', 'BPF_JEQ', 'BPF_JLT', 'BPF_JGE', 'BPF_JSGT', 'BPF_XOR'],
"5.12": ['BPF_JEQ', 'BPF_OR', 'BPF_JNE', 'BPF_JSLT', 'BPF_OR_32', 'BPF_XOR_32', 'BPF_JSGT', 'BPF_JSGE', 'BPF_AND', 'BPF_JGT', 'BPF_XOR', 'BPF_JGE', 'BPF_JSLE', 'BPF_JLE', 'BPF_AND_32', 'BPF_JLT'],
"5.13": ['BPF_AND', 'BPF_XOR_32', 'BPF_OR', 'BPF_OR_32', 'BPF_XOR', 'BPF_AND_32'],
"5.14": ['BPF_AND', 'BPF_XOR_32', 'BPF_OR', 'BPF_OR_32', 'BPF_XOR', 'BPF_AND_32'],
"5.15": ['BPF_AND', 'BPF_XOR_32', 'BPF_OR', 'BPF_OR_32', 'BPF_XOR', 'BPF_AND_32'],
"5.16": ['BPF_AND', 'BPF_XOR_32', 'BPF_OR', 'BPF_OR_32', 'BPF_XOR', 'BPF_AND_32'],
"5.17": ['BPF_AND', 'BPF_XOR_32', 'BPF_OR', 'BPF_OR_32', 'BPF_XOR', 'BPF_AND_32'],
"5.18": ['BPF_AND', 'BPF_XOR_32', 'BPF_OR', 'BPF_OR_32', 'BPF_XOR', 'BPF_AND_32'],
"5.19": ['BPF_AND', 'BPF_XOR_32', 'BPF_OR', 'BPF_OR_32', 'BPF_XOR', 'BPF_AND_32']
}

kernbase_dir = "/home/cav23-artifact/reproduce-results/linux-stable/v{}"
bpf_encodings_outdir = "/home/cav23-artifact/reproduce-results/bpf-encodings/v{}"
generate_encodings_script = "/home/cav23-artifact/llvm-to-smt/generate_encodings.py"
verif_synth_outdir = "/home/cav23-artifact/reproduce-results/verifcation-synthesis-results/v{}"
bpf_alu_jmp_synthesis_script = "/home/cav23-artifact/bpf-verification/src/bpf_alu_jmp_synthesis.py"
bpf_alu_jmp_synthesis_toml_path = "/home/cav23-artifact/bpf-verification/src/verification_synth_setup_config.toml"

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--kernver", help="kernel version", type=str,
                        required=True)

    args = parser.parse_args()
    kernbase_dir_i = kernbase_dir.format(args.kernver)

    # create linux output directory
    kernbase_outdir_fullpath_i = pathlib.Path(kernbase_dir_i).resolve()
    subprocess.run(['mkdir', '-p', '{}'.format(str(kernbase_outdir_fullpath_i))],
              check=True, text=True, bufsize=1)
    subprocess.run(['rm', '-rf', '{}/*'.format(str(kernbase_outdir_fullpath_i))],
              check=True, text=True, bufsize=1)
    
    # clone linux source
    clone_kernel_cmd_i = ["git", "clone", 
                          "--depth", "1", 
                          "--branch", "v{}".format(args.kernver), 
                          "git://git.kernel.org/pub/scm/linux/kernel/git/stable/linux-stable.git", 
                          str(kernbase_outdir_fullpath_i)]
    subprocess.run(clone_kernel_cmd_i, check=True, text=True, bufsize=1)

    # create bpf encodings output directory
    bpf_encodings_outdir_i = pathlib.Path(bpf_encodings_outdir.format(args.kernver)).resolve()
    subprocess.run(['mkdir', '-p', '{}'.format(str(bpf_encodings_outdir_i))],
              check=True, text=True, bufsize=1)
    subprocess.run(['rm', '-rf', '{}/*'.format(str(bpf_encodings_outdir_i))],
              check=True, text=True, bufsize=1)

    # run llvm to smt
    subprocess.run(['python3', generate_encodings_script, 
                    '--kernver', str(args.kernver), 
                    '--kernbasedir', str(kernbase_outdir_fullpath_i),
                    '--outdir', str(bpf_encodings_outdir_i)
                    ],
              check=True, text=True, bufsize=1)

    # create verification/synthesis results directory
    verif_synth_outdir_i = pathlib.Path(verif_synth_outdir.format(args.kernver)).resolve()
    subprocess.run(['mkdir', '-p', '{}'.format(str(verif_synth_outdir_i))],
              check=True, text=True, bufsize=1)
    subprocess.run(['rm', '-rf', '{}/*'.format(str(verif_synth_outdir_i))],
              check=True, text=True, bufsize=1)
    
    # run verification/synthesis
    verif_synth_cmd_i = ['python3', bpf_alu_jmp_synthesis_script, 
                '--kernver', str(args.kernver), 
                '--encodings_path', str(bpf_encodings_outdir_i),
                '--res_path', str(verif_synth_outdir_i),
                '--synth_iter', '1',
                '--ver_set'
                ]
    verif_synth_cmd_i += ver_set_dict[args.kernver]
    verif_synth_cmd_i += ['--toml_path', bpf_alu_jmp_synthesis_toml_path]
    
    if args.kernver == "4.14":
        verif_synth_cmd_i.append('--json_offset')
        verif_synth_cmd_i.append('4')

    subprocess.run(verif_synth_cmd_i, check=True, bufsize=1)