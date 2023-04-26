import sys
import lib_reg_bounds_tracking.lib_reg_bounds_tracking as lr
from z3 import And, Or
from pprint import pprint
from collections import Counter
from termcolor import colored
import toml
import time
import copy
import os.path
import itertools
import argparse
import json



#function to check soundness of a bpf instruction using sync wellformed
#predicate
def check_sync_soundness(usr_config):
    print("\n--------------------------------------------------------------")
    print("\t\tEXECUTING SRO VERIFICATION")
    print("--------------------------------------------------------------\n")
    #for debugging
    #usr_config.print_settings()
    
    #keep track of verification stats
    sync_stats = lr.process_stats()
    sync_stats.total_progs = str(len(list(itertools.product(*usr_config.insn_set_list))))
    #initialize construct for sync verification
    sync_module = lr.verification_synth_module(usr_config)
    
    #structures specific to sync verification
    sync_ver_set = set()
    bug_type_dict_per_insn = {}
    
    #enumerate product of given insn sets by taking product of all sets given
    for prog in itertools.product(*usr_config.insn_set_list):
        sync_module.prog = prog
        sync_module.prog_size = len(prog)
        sync_stats.start_time = time.time()
    ###############################################################################
    # Setup Solver, Bitvectors, and General Constraints
    ############################################################################
        #reset smt solver
        sync_module.solver = None
        lr.BitVecHelper.clear_map()
        f_gen_const = lr.FormulaBuilder()

        #create instance of smt solver, add bpf encodings to it, and make list
        #of input/output mappings from the bpf encoding to our smt formula
        sync_module.solver, sync_module.inp_json_bpf_mapping_list, sync_module.out_json_bpf_mapping_list = lr.parse_and_map(prog, usr_config.OP_to_smt_file_map)

        #create arrays of input/output registers (bpf_register class contains
        #both abstract and concrete state) based on extracted mappings
        sync_module.create_reg_states("dst_input")
        sync_module.create_reg_states("src_input")
        sync_module.create_reg_states("dst_output")
        sync_module.create_reg_states("src_output")


        #define corresponding concrete outputs based on current bpf operation
        sync_module.set_concrete_operation(f_gen_const)
        #assert concrete values don't change in jmps
        sync_module.set_unchanged_concrete_jmps(f_gen_const)

        #assign mappings to bitvectors based on instruction 
        sync_module.assign_bitvector_mapping_to_encodings(f_gen_const)

        # Add constraints to solver
        sync_module.solver.add(And(f_gen_const.list))
    ###############################################################################
    # Setup preconditions
    ############################################################################
        f_pre_cond = lr.FormulaBuilder()

        #32 bit concrete values are extracted from the 64 bit values
        sync_module.extract_from_64_bit("dst_input", f_pre_cond)
        sync_module.extract_from_64_bit("src_input", f_pre_cond)
        sync_module.extract_from_64_bit("dst_output", f_pre_cond)
        sync_module.extract_from_64_bit("src_output", f_pre_cond)

        #propagate two sync instructions
        sync_module.seq_discover(f_pre_cond)
        
        sync_module.solver.add(And(f_pre_cond.list))
    ############################################################################
    # Setup postconditions
    ############################################################################
        f_post_cond = lr.FormulaBuilder()

        #outputs of 1,2,3...n-1 insns are in wellformed set
        sync_module.set_wellformed_outputs(f_post_cond)

        #safety property list to check with corresponding insn
        sync_module.set_verification_condition()

        sync_module.solver.add(And(f_post_cond.list))
    ############################################################################
    # Solve
    ############################################################################
        print(str(sync_stats.iteration) + "/" + str(sync_stats.total_progs), "Verifying " + str(prog[2]) + " ... ", end =" ", flush=True)
        #set spec in object for printing purposes
        sync_module.set_spec(f_gen_const, f_pre_cond, f_post_cond)
        #check violated bounds for current instruction
        sync_module.check_bug_violations()
        check_output = "sat" if len(sync_module.violated_prop_list) > 0 else "unsat"
        print(colored("Done.", "green"))# "Bounds violated: ", sync_module.violated_prop_list)
    
        sync_stats.end_time = time.time()
        sync_stats.set_execution_time()
        sync_stats.eval_dict[",".join(sync_module.prog)] = list((sync_stats.prog_execution_time, check_output,  copy.deepcopy(sync_module.violated_prop_list)))
        if check_output == "sat":
            #we add the violated instruction to our sync_ver list
            sync_ver_set.add(prog[2])
            #copy violated bounds for the offending instruction for the dict
            #{insn: [u32, u64]..}
            bug_type_dict_per_insn[sync_module.prog[2]] = copy.deepcopy(sync_module.violated_prop_list)
        
        #print("\n--------------SRO SOUNDNESS CHECK--------------")
        sync_stats.set_elapsed_time()
        #sync_stats.print_verification_stats()
        sync_stats.iteration += 1
    print(colored("SRO Verification Complete", "green"))
    sync_stats.print_verification_stats()
    #print("Set of potential unsound instructions: ", sync_ver_set, "\n")
    sync_stats.write_dict_to_file(usr_config, "sync")
    #update our usr_config to reflect unsound ops and which bugs types they can manifest
    return sync_ver_set, bug_type_dict_per_insn



# example driver
if __name__ == "__main__":
    #parse toml config file and initialize a config_setup class for verification
    #and synthesis procedures.
    parsed_toml = toml.load("verification_synth_setup_config.toml")
    #if argv is passed for kernel version, use that instead (for experiments)
    if len(sys.argv) == 2:
        parsed_toml["kernel_ver"] = str(sys.argv[1])
    usr_config = lr.config_setup(parsed_toml)
    usr_config.insn_set_list = [{"BPF_SYNC"}, {"BPF_SYNC"}, {"BPF_OR", "BPF_OR_32"}]

    check_sync_soundness(usr_config)
