import sys
import os.path
#sys.path.insert(0, os.path.abspath('..'))
from lib_reg_bounds_tracking.lib_reg_bounds_tracking import config_setup, process_stats
from wf_soundness import check_wf_soundness
from sync_soundness import check_sync_soundness
from synthesize_bug_types import synthesize_bugs
import z3
from pprint import pprint
import toml
import time
import itertools
import argparse as argp
import json


###############################################################################
# Main begins
###############################################################################
def main():

    #setup argparse and customized options
    bpf_instructions_set = ["BPF_AND", "BPF_OR", "BPF_LSH", "BPF_RSH", "BPF_JLT", "BPF_JLE", "BPF_JEQ", "BPF_JNE", "BPF_JGE", "BPF_JGT", "BPF_JSGE", "BPF_JSGT", "BPF_JSLT", "BPF_JSLE", "BPF_ADD", "BPF_SUB", "BPF_XOR", "BPF_ARSH", "BPF_OR_32", "BPF_AND_32", "BPF_LSH_32", "BPF_RSH_32", "BPF_ADD_32", "BPF_SUB_32", "BPF_XOR_32","BPF_ARSH_32", "BPF_JLT_32",  "BPF_JLE_32", "BPF_JSLT_32", "BPF_JSLE_32", "BPF_JEQ_32", "BPF_JNE_32", "BPF_JGE_32", "BPF_JGT_32", "BPF_JSGE_32", "BPF_JSGT_32"]
    parser = argp.ArgumentParser(prog="eBPF Verification and Synthesis", epilog="Possible bpf instructions: {BPF_AND,BPF_OR,BPF_LSH,BPF_RSH,BPF_JLT,BPF_JLE,BPF_JEQ,BPF_JNE,BPF_JGE,BPF_JGT,BPF_JSGE,BPF_JSGT,BPF_JSLT,BPF_JSLE,BPF_ADD,BPF_SUB,BPF_XOR,BPF_ARSH,BPF_OR_32,BPF_AND_32,BPF_LSH_32,BPF_RSH_32,BPF_ADD_32,BPF_SUB_32,BPF_XOR_32,BPF_ARSH_32,BPF_JLT_32,BPF_JLE_32,BPF_JSLT_32,BPF_JSLE_32,BPF_JEQ_32,BPF_JNE_32,BPF_JGE_32,BPF_JGT_32,BPF_JSGE_32,BPF_JSGT_32}")
    parser.add_argument('--kernver', type=str, required=True, help="kernel version")
    parser.add_argument('--json_offset', type=int, help="offset for mapping bpf_reg_states, set to 4 for 4.14 and 5 for everything else")
    parser.add_argument('--encodings_path', type=str, required=True, help="set path to bpf encodings produced by llvm-to-smt")
    parser.add_argument('--res_path', type=str, help="set path where to write results")
    parser.add_argument('--synth_iter', type=int, help="set sequence length to synthesize (1-3)")
    parser.add_argument('--synth_set', type=str, metavar='bpf instruction', help="choose instructions use as priors for synthesis (meaning they won't be the last instructions in the sequence)", nargs="*", choices=bpf_instructions_set)
    parser.add_argument('--ver_set', type=str, metavar='bpf instruction', help="choose instructions to verify", nargs="*", choices=bpf_instructions_set)
    parser.add_argument('--toml_path', type=str, required=True, help="kernel version", default="verification_synth_setup_config.toml")
    args = parser.parse_args()

    #parse toml config file and initialize a config_setup class for verification
    #and synthesis procedures.
    parsed_toml = toml.load(args.toml_path)

    #update config options based on user inputs
    parsed_toml["kernel_ver"] = args.kernver if args.kernver else parsed_toml["kernel_ver"]
    parsed_toml["json_offset"] = args.json_offset if args.json_offset else parsed_toml["json_offset"]
    parsed_toml["bpf_encodings_path"] = args.encodings_path if args.encodings_path else parsed_toml["bpf_encodings_path"]
    parsed_toml["write_dir_path"] = args.res_path if args.res_path else parsed_toml["write_dir_path"]
    parsed_toml["num_synthesis_iter"] = args.synth_iter if args.synth_iter else parsed_toml["num_synthesis_iter"]
    parsed_toml["insn_set"] = args.synth_set if args.synth_set else parsed_toml["insn_set"]
    parsed_toml["verification_set"] = args.ver_set if args.ver_set else parsed_toml["verification_set"]
    usr_config = config_setup(parsed_toml)

    print("\n--------------------------------------------------------------")
    print("\t\tEXPERIMENT SETUP")
    print("--------------------------------------------------------------\n")
    pprint(parsed_toml)

    ###################### Execute verification and synthesis
    #1) check all wellformed inputs before trying sync soundness
    wf_set = check_wf_soundness(usr_config)
    
    #2) based on the set of insn from the wellformed check that is unsound -
    #   check with wellformed SRO inputs to try and eliminate more insns
    usr_config.insn_set_list = [{"BPF_SYNC"}, {"BPF_SYNC"}, wf_set]
    last_set, usr_config.bugs_dict = check_sync_soundness(usr_config)

    #3) given insns that are not sound with wellformed SRO inputs - try to
    #   synthesize programs that become illformed (last insn must be from set
    #   returned from the SRO soundness check)
    usr_config.insn_set_list = [last_set]
    synthesize_bugs(usr_config)
    #usr_config.print_settings()

    #print aggregate stats.
    aggregate = process_stats()
    aggregate.print_verification_aggregate(usr_config)
    aggregate.print_synthesis_aggregate(usr_config)

if __name__ == "__main__":
    main()

