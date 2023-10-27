import sys
import lib_reg_bounds_tracking.lib_reg_bounds_tracking as lr
from z3 import And, Or
from pprint import pprint
from itertools import combinations_with_replacement
from itertools import chain, combinations
from collections import Counter
from termcolor import colored
import copy
import time
import os.path
import itertools
import argparse
import json
import toml
from multiprocessing import Pool


#function to check soundness of a bpf instruction using all wellformed
#predicate
def check_wf_soundness(usr_config):
    print("\n--------------------------------------------------------------")
    print("\t\t2.1(a) Executing gen verification")
    print("--------------------------------------------------------------\n")
    #for debugging
    #usr_config.print_settings()
    
    #keep track of verification stats
    wf_stats = lr.process_stats()
    wf_stats.total_progs = str(len(list(itertools.product(*usr_config.insn_set_list))))
    #structures specific to wf verification
    wf_ver_set = set()
    
    #enumerate product of given insn sets by taking product of all sets given
    pool = Pool()
    results = []
    i = 1
    for prog in itertools.product(*usr_config.insn_set_list):
        results.append(pool.apply_async(check_wf_soundness_insn, (i, usr_config, prog, wf_stats)))
        i += 1

    for result in results:
        prog, prog_execution_time, violated_prop_list = result.get()
        nb_violated_prop = len(violated_prop_list)
        check_output = "sat" if nb_violated_prop > 0 else "unsat"
        wf_stats.eval_dict[",".join(prog)] = list((prog_execution_time, check_output, violated_prop_list))

        if nb_violated_prop > 0:
            #we add the violated instruction to our wf_ver list
            wf_ver_set.add(prog[0])
            #aggregate gen violations
            usr_config.gen_violations += nb_violated_prop
            usr_config.gen_unsound_insn += 1

    print(colored("gen Verification Complete", "green"))
    wf_stats.print_verification_stats()
    #print("Set of sound instructions: ", usr_config.insn_set_list[0] - wf_ver_set)
    #print("Set of potential unsound instructions: ", wf_ver_set, "\n")
    wf_stats.write_dict_to_file(usr_config, "wf")
    return wf_ver_set


def check_wf_soundness_insn(iteration, usr_config, prog, wf_stats):
    #initialize construct for wf verification
    wf_module = lr.verification_synth_module(usr_config)

    wf_module.prog = prog
    wf_module.prog_size = len(prog)
    wf_stats.start_time = time.time()
    ############################################################################
    # Setup Solver, Bitvectors, and General Constraints
    ############################################################################
    #reset smt solver
    wf_module.solver = None
    lr.BitVecHelper.clear_map()
    f_gen_const = lr.FormulaBuilder()

    #create instance of smt solver, add bpf encodings to it, and make list
    #of input/output mappings from the bpf encoding to our smt formula
    wf_module.solver, wf_module.inp_json_bpf_mapping_list, wf_module.out_json_bpf_mapping_list = lr.parse_and_map(prog, usr_config.OP_to_smt_file_map)

    #create arrays of input/output registers (bpf_register class contains
    #both abstract and concrete state) based on extracted mappings
    #For ALU verification
    wf_module.create_reg_states("dst_input")
    wf_module.create_reg_states("src_input")
    wf_module.create_reg_states("dst_output")
    wf_module.create_reg_states("src_output")

    #define corresponding concrete outputs based on current bpf operation
    #immaterial for jmps in verification since prog size 1.
    wf_module.set_concrete_operation(f_gen_const)

    #assert concrete values don't change in jmps
    wf_module.set_unchanged_concrete_jmps(f_gen_const)

    #assign mappings to bitvectors based on instruction
    wf_module.assign_bitvector_mapping_to_encodings(f_gen_const)

    # Add constraints to solver
    wf_module.solver.add(And(f_gen_const.list))
    ############################################################################
    # Setup preconditions
    ############################################################################
    f_pre_cond = lr.FormulaBuilder()

    #setup preconditions for the sync verification - 32 bit concrete values
    #are extracted from the 64 bit values, and concrete values (32 and 64)
    #must be contained in abstract domain bounds (32 and 64 bit
    #respectively)
    wf_module.extract_from_64_bit("dst_input", f_pre_cond)
    wf_module.extract_from_64_bit("src_input", f_pre_cond)
    wf_module.extract_from_64_bit("dst_output", f_pre_cond)
    wf_module.extract_from_64_bit("src_output", f_pre_cond)
    wf_module.conc_is_contained_in_bounds("dst_input", f_pre_cond)
    wf_module.conc_is_contained_in_bounds("src_input", f_pre_cond)

    wf_module.solver.add(And(f_pre_cond.list))
    ############################################################################
    # Setup postconditions
    ############################################################################
    f_post_cond = lr.FormulaBuilder()
    wf_module.set_verification_condition()
    
    ############################################################################
    # Solve
    ############################################################################
    print(str(iteration) + "/" + str(wf_stats.total_progs), "Verifying " + str(prog[0]) + "...")
    #set spec in object for printing purposes
    wf_module.set_spec(f_gen_const, f_pre_cond, f_post_cond)
    #check violated bounds for current instruction
    wf_module.check_bug_violations()
    print(str(iteration) + "/" + str(wf_stats.total_progs) + " " + str(prog[0]) + " " + colored("Done.", "green"))

    wf_stats.end_time = time.time()
    wf_stats.set_execution_time()

    #wf_stats.set_elapsed_time()
    #wf_stats.print_verification_stats()
    return prog, wf_stats.prog_execution_time, copy.deepcopy(wf_module.violated_prop_list)


# test
if __name__ == "__main__":
    #parse toml config file and initialize a config_setup class for verification and synthesis procedures.
    parsed_toml = toml.load("verification_synth_setup_config.toml")
    #if argv is passed for kernel version, use that instead (for experiments)
    if len(sys.argv) == 2:
        parsed_toml["kernel_ver"] = str(sys.argv[1])
    usr_config = lr.config_setup(parsed_toml)
    usr_config.insn_set_list = [{"BPF_XOR", "BPF_XOR_32", "BPF_AND_32"}]

    check_wf_soundness(usr_config)

