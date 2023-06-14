import sys
import lib_reg_bounds_tracking.lib_reg_bounds_tracking as lr
from z3 import And, Or
from pprint import pprint
import toml
import time
import copy
import os.path
import itertools
import json


#function to synthesize POC for bugs
def synthesize_bugs(usr_config):
    print("\n--------------------------------------------------------------")
    print("\t\t2.2 Generating POC for domain violations")
    print("--------------------------------------------------------------\n")
    
    #keep track of verification stats
    synth_stats = lr.process_stats()
    #initialize construct for synthesis
    synth_module = lr.verification_synth_module(usr_config)
    #for debugging
    #usr_config.print_settings()

    for k in range(usr_config.num_iter):
        #enumerate product of given insn sets by taking product of all sets
        #given
        synth_stats.total_progs = str(len(list(itertools.product(*usr_config.insn_set_list))))
        for prog in itertools.product(*usr_config.insn_set_list):

            synth_module.prog = synth_stats.prog = prog
            synth_module.prog_size = len(prog)
            #if all bugs types for specific instruction have been captured no
            #need to keep searching for them.
            if len(usr_config.bugs_dict[prog[-1]]) == 0:
                continue
                
            synth_stats.start_time = time.time()
        ########################################################################
        # Setup Solver, Bitvectors, and General Constraints
        ########################################################################    #reset smt solver
            synth_module.solver = None
            lr.BitVecHelper.clear_map()
            f_gen_const = lr.FormulaBuilder()

            #create instance of smt solver, add bpf encodings to it, and make
            #list of input/output mappings from the bpf encoding to our smt
            #formula
            synth_module.solver, synth_module.inp_json_bpf_mapping_list, synth_module.out_json_bpf_mapping_list = lr.parse_and_map(prog, usr_config.OP_to_smt_file_map)

            #create arrays of input/output registers (bpf_register class
            #contains both abstract and concrete state) based on extracted
            #mappings
            synth_module.create_reg_states("dst_input")
            synth_module.create_reg_states("src_input")
            synth_module.create_reg_states("dst_output")
            synth_module.create_reg_states("src_output")

            #define corresponding concrete outputs based on current bpf operation
            synth_module.set_concrete_operation(f_gen_const)
            #assert concrete values don't change in jmps
            synth_module.set_unchanged_concrete_jmps(f_gen_const)

            #assign mappings to bitvectors based on instruction 
            synth_module.assign_bitvector_mapping_to_encodings(f_gen_const)

            # Add constraints to solver
            synth_module.solver.add(And(f_gen_const.list))
        ########################################################################
        # Setup preconditions
        ########################################################################
            f_pre_cond = lr.FormulaBuilder()

            #32 bit concrete values are extracted from the 64 bit values
            synth_module.extract_from_64_bit("dst_input", f_pre_cond)
            synth_module.extract_from_64_bit("src_input", f_pre_cond)
            synth_module.extract_from_64_bit("dst_output", f_pre_cond)
            synth_module.extract_from_64_bit("src_output", f_pre_cond)
            synth_module.conc_is_contained_in_bounds("dst_input", f_pre_cond) 
            synth_module.conc_is_contained_in_bounds("src_input", f_pre_cond) 
            
            #update operands based on results of previous instructions if there are any
            synth_module.propagate_instructions(f_pre_cond)

            #initial states the first instruction operands can have
            f_pre_cond.append(Or(
                synth_module.input_dst_reg_list[0].singleton(),
                synth_module.input_dst_reg_list[0].fully_unknown()))
            f_pre_cond.append(Or(
                synth_module.input_src_reg_list[0].singleton(),
                synth_module.input_src_reg_list[0].fully_unknown()))

            synth_module.solver.add(And(f_pre_cond.list))
        ########################################################################
        # Setup postconditions
        ########################################################################
            f_post_cond = lr.FormulaBuilder()

            #safety property list to check with corresponding insn
            synth_module.set_verification_condition()      
        ########################################################################
        # Solve
        ########################################################################
            #set spec in object for printing purposes
            synth_module.set_spec(f_gen_const, f_pre_cond, f_post_cond)
            #check violated bounds for current instruction
            synth_module.synthesize_bug_type(usr_config)
            check_output = "sat" if len(synth_module.violated_prop_list) > 0 else "unsat"

            synth_stats.end_time = time.time()
            synth_stats.set_execution_time()
            
            if check_output == "sat":
                #add only sat programs to our eval dictionary
                synth_stats.eval_dict[",".join(synth_module.prog)] = list((synth_stats.prog_execution_time, check_output, copy.deepcopy(synth_module.violated_prop_list)))
                #aggregate synth violations 
                usr_config.synth_violations += len(synth_module.violated_prop_list)
                usr_config.synth_len1 = usr_config.synth_len1 + len(synth_module.violated_prop_list) if len(prog) == 1 else usr_config.synth_len1
                usr_config.synth_len2 = usr_config.synth_len2 + len(synth_module.violated_prop_list) if len(prog) == 2 else usr_config.synth_len2
                usr_config.synth_len3 = usr_config.synth_len3 + len(synth_module.violated_prop_list) if len(prog) == 3 else usr_config.synth_len3 
                


            synth_stats.set_elapsed_time()
            #synth_stats.print_synthesis_stats()
            synth_stats.iteration += 1

        #add another set to the synthesis for next iteration    
        usr_config.insn_set_list.insert(0, usr_config.OPS_set)
        synth_stats.iteration = 1
    #synth_stats.print_synthesis_aggregate(usr_config)
    print("\n\n========================================================================")
    synth_stats.write_dict_to_file(usr_config, "synth")






# example driver
if __name__ == "__main__":
    #parse toml config file and initialize a config_setup class for verification and synthesis procedures.
    parsed_toml = toml.load("verification_synth_setup_config.toml")
    #if argv is passed for kernel version, use that instead (for experiments)
    if len(sys.argv) == 2:
        parsed_toml["kernel_ver"] = str(sys.argv[1])
    usr_config = lr.config_setup(parsed_toml)
    usr_config.insn_set_list = [{"BPF_JLT"}]

    synthesize_bugs(usr_config)

