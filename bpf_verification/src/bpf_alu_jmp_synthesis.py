import sys
import os.path
#sys.path.insert(0, os.path.abspath('..'))
from lib_reg_bounds_tracking.lib_reg_bounds_tracking import config_setup
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

    #parse toml config file and initialize a config_setup class for verification
    #and synthesis procedures.
    parsed_toml = toml.load("verification_synth_setup_config.toml")
    #setup argparse and customized options
    parser = argp.ArgumentParser()
    parser.add_argument('--kernver', type=str, help="kernel version")
    parser.add_argument('--json_offset', type=int, help="offset for mapping bpf_reg_states, set to 4 for 4.14 and 5 for everything else")
    parser.add_argument('--encodings_path', type=str, help="set path to bpf encodings")
    parser.add_argument('--res_path', type=str, help="set path where to write results")
    parser.add_argument('--synth_iter', type=int, help="set length k of sequence to synthesize")
    parser.add_argument('--insn_set', type=str, help="choose instructions to verify", nargs="*", choices=["BPF_AND", "BPF_OR", "BPF_LSH", "BPF_RSH", "BPF_JLT", "BPF_JLE", "BPF_JEQ", "BPF_JNE", "BPF_JGE", "BPF_JGT", "BPF_JSGE", "BPF_JSGT", "BPF_JSLT", "BPF_JSLE", "BPF_ADD", "BPF_SUB", "BPF_XOR", "BPF_ARSH", "BPF_OR_32", "BPF_AND_32", "BPF_LSH_32", "BPF_RSH_32", "BPF_ADD_32", "BPF_SUB_32", "BPF_XOR_32","BPF_ARSH_32", "BPF_JLT_32",  "BPF_JLE_32", "BPF_JSLT_32", "BPF_JSLE_32", "BPF_JEQ_32", "BPF_JNE_32", "BPF_JGE_32", "BPF_JGT_32", "BPF_JSGE_32", "BPF_JSGT_32"])
    parser.add_argument('--ver_set', type=str, help="choose instructions use as priors for synthesis (meaning they won't be the last instructions in the sequence)", nargs="*", choices=["BPF_AND", "BPF_OR", "BPF_LSH", "BPF_RSH", "BPF_JLT", "BPF_JLE", "BPF_JEQ", "BPF_JNE", "BPF_JGE", "BPF_JGT", "BPF_JSGE", "BPF_JSGT", "BPF_JSLT", "BPF_JSLE", "BPF_ADD", "BPF_SUB", "BPF_XOR", "BPF_ARSH", "BPF_OR_32", "BPF_AND_32", "BPF_LSH_32", "BPF_RSH_32", "BPF_ADD_32", "BPF_SUB_32", "BPF_XOR_32","BPF_ARSH_32", "BPF_JLT_32",  "BPF_JLE_32", "BPF_JSLT_32", "BPF_JSLE_32", "BPF_JEQ_32", "BPF_JNE_32", "BPF_JGE_32", "BPF_JGT_32", "BPF_JSGE_32", "BPF_JSGT_32"])
    args = parser.parse_args()
    #print(args)

    
    #print(parser)
    #update config options based on user inputs
    parsed_toml["kernel_ver"] = args.kernver if args.kernver else parsed_toml["kernel_ver"]
    parsed_toml["json_offset"] = args.json_offset if args.json_offset else parsed_toml["json_offset"]
    parsed_toml["bpf_encodings_path"] = args.encodings_path if args.encodings_path else parsed_toml["bpf_encodings_path"]
    parsed_toml["write_dir_path"] = args.res_path if args.res_path else parsed_toml["write_dir_path"]
    parsed_toml["num_synthesis_iter"] = args.synth_iter if args.synth_iter else parsed_toml["num_synthesis_iter"]
    parsed_toml["insn_set"] = args.insn_set if args.insn_set else parsed_toml["insn_set"]
    parsed_toml["verification_set"] = args.ver_set if args.ver_set else parsed_toml["verification_set"]
    usr_config = config_setup(parsed_toml)
    pprint(parsed_toml)

    ###################### Execute verification and synthesis
    #1) check all wellformed inputs before trying sync soundness
    wf_set = check_wf_soundness(usr_config)
    
    #2) based on the set of insn from the wellformed check that is unsound -
    #   check with wellformed SRO inputs to try and eliminate more insns
    usr_config.insn_set_list = [{"BPF_SYNC"}, {"BPF_SYNC"}, wf_set]
    last_set, usr_config.bugs_dict = check_sync_soundness(usr_config)

    if (len(last_set) == 0):
        print("Kernel version is sound")
        sys.exit()
    
    
    #3) given insns that are not sound with wellformed SRO inputs - try to
    #   synthesize programs that become illformed (last insn must be from set
    #   returned from the SRO soundness check)
    usr_config.insn_set_list = [last_set]
    synthesize_bugs(usr_config)
    usr_config.print_settings()


if __name__ == "__main__":
    main()


















    

    # while(k < 3):
    #     iteration = 0
    #     #enumerate all programs with the given instruction set
    #     for prog in itertools.product(*prog_set_list):
    #         #prog = ("BPF_JLT", "BPF_JGT", "BPF_AND")
    #         #prog = ("BPF_JLT",)
    #         prog_size = len(prog)
            
    #         # if prog_size > 1:
    #         #     break
    #             #continue
    #         #print(prog)
    #         if len(prog) == 1:
    #             bpf_OP = prog[0]
    #         else:
    #             bpf_OP = prog

    #         start_time = time.time()
    #         ###############################################################################
    #         # Setup Solver, Bitvectors, and General Constraints
    #         ############################################################################
    #         ###
    #         #reset smt solver
    #         solver = None
    #         BitVecHelper.clear_map()

            
    #         #create instance of smt solver, add bpf encodings to it, and make list of input/output mappings from the bpf encoding to our smt formula
    #         solver, inp_json_bpf_mapping_list, out_json_bpf_mapping_list = parse_and_map(prog, OP_to_smt_file_map)

    #         #create arrays of input/output registers (abstract domains) based on extracted mappings
    #         dst_reg_st_input_list = create_reg_states(inp_json_bpf_mapping_list, prog, prog_size, "dst_input")
    #         src_reg_st_input_list = create_reg_states(inp_json_bpf_mapping_list, prog, prog_size, "src_input")
    #         dst_reg_st_output_list = create_reg_states(out_json_bpf_mapping_list, prog, prog_size, "dst_input")
    #         src_reg_st_output_list = create_reg_states(out_json_bpf_mapping_list, prog, prog_size, "src_output")

    #         f_gen_const = FormulaBuilder()

    #         #define bitvecs for concrete inputs and outputs in formula
    #         dst_conc_input_list, src_conc_input_list, dst32_conc_input_list, src32_conc_input_list, dst_conc_output_list, dst32_conc_output_list = create_concrete_I_O_bitvecs(prog_size)

    #         #define corresponding concrete outputs based on current bpf operation
    #         set_concrete64_operation(dst_conc_input_list, src_conc_input_list,
    #                 dst32_conc_input_list, src32_conc_input_list,
    #                 dst_conc_output_list, dst32_conc_output_list,
    #                 prog_size, bpf_OP, f_gen_const)

    #         # Add constraints to solver
    #         solver.add(And(f_gen_const.list))
    #         ###############################################################################
    #         # Setup preconditions
    #         ###############################################################################
    #         f_pre_cond = FormulaBuilder()

    #         #setup preconditions for the synthesis - 32 bit concrete values are extracted from the 64 bit values, and concrete values (32 and 64) must be contained in abstract domain bounds (32 and 64 bit respectively).
    #         extract_from_64_bit(prog_size, dst32_conc_input_list, dst_conc_input_list, f_pre_cond)
    #         extract_from_64_bit(prog_size, src32_conc_input_list, src_conc_input_list, f_pre_cond)
    #         extract_from_64_bit(prog_size, dst32_conc_output_list, dst_conc_output_list, f_pre_cond)
            
    #         #concrete inputs are contained in their respective bounds (32/64)
    #         conc_is_contained_in_64(prog_size, dst_reg_st_input_list, dst_conc_input_list, f_pre_cond)
    #         conc_is_contained_in_32(prog_size, dst_reg_st_input_list, dst32_conc_input_list, f_pre_cond)
    #         conc_is_contained_in_64(prog_size, src_reg_st_input_list, src_conc_input_list, f_pre_cond)
    #         conc_is_contained_in_32(prog_size, src_reg_st_input_list, src32_conc_input_list, f_pre_cond)

    #         #update operands based on results of previous instructions if there are any
    #         propagate_instructions(prog_size, dst_reg_st_output_list, dst_reg_st_input_list, dst_conc_input_list, dst32_conc_input_list, dst_conc_output_list, src_reg_st_input_list, src_conc_input_list, src32_conc_input_list, f_pre_cond)

    #         #initial states the first instruction operands can have
    #         f_pre_cond.append(Or(dst_reg_st_input_list[0].fully_known(None, dst32_conc_input_list[0], dst_conc_input_list[0]),  dst_reg_st_input_list[0].fully_unknown()))
    #         f_pre_cond.append(Or(src_reg_st_input_list[0].fully_known(None, src32_conc_input_list[0], src_conc_input_list[0]),  src_reg_st_input_list[0].fully_unknown()))


    #         # f_pre_cond.append(dst_reg_st_input_list[0].fully_unknown())
    #         # f_pre_cond.append(src_reg_st_input_list[0].fully_known(0x600000002))
    #         # #f_pre_cond.append(src_reg_st_input_list[0].fully_known(0x0))
    #         # f_pre_cond.append(src_reg_st_input_list[1].fully_known(0x0))
    #         # f_pre_cond.append(src_reg_st_input_list[2].fully_known(0x0))
    #         # #f_pre_cond.append(src_reg_st_input_list[1].fully_known(None, src32_conc_input_list[1], src_conc_input_list[1]))

    #         # f_pre_cond.append(dst_reg_st_input_list[0].var_off_value   == 0x1);
    #         # f_pre_cond.append(dst_reg_st_input_list[0].var_off_mask   == 0xffffffff00000000);
    #         # f_pre_cond.append(dst_reg_st_input_list[0].smin_value   == 0x8000000000000001);
    #         # f_pre_cond.append(dst_reg_st_input_list[0].smax_value   == 0x7fffffff00000001);
    #         # f_pre_cond.append(dst_reg_st_input_list[0].umin_value   == 1);
    #         # f_pre_cond.append(dst_reg_st_input_list[0].umax_value   == 0xffffffff00000001);
    #         # f_pre_cond.append(dst_reg_st_input_list[0].s32_min_value   == 1);
    #         # f_pre_cond.append(dst_reg_st_input_list[0].s32_max_value   == 1);
    #         # f_pre_cond.append(dst_reg_st_input_list[0].u32_min_value   == 1);
    #         # f_pre_cond.append(dst_reg_st_input_list[0].u32_max_value   == 1);
            
    #         solver.add(And(f_pre_cond.list))
    #         ###############################################################################
    #         # Setup postconditions
    #         ###############################################################################
    #         f_post_cond = FormulaBuilder()                

    #         #final instruction concrete output dst is within bounds - safety property
    #         f_post_cond.append(Or(
    #             Not(dst_reg_st_output_list[-1].get_contains32_predicate(dst32_conc_output_list[-1])),
    #             Not(dst_reg_st_output_list[-1].get_contains64_predicate(dst_conc_output_list[-1]))))


            
    #         # f_post_cond.append(Or(
    #         #     Not(dst_reg_st_output_list[-1].get_contains64_predicate_only_unsigned(dst_conc_output_list[-1])), 
    #         #     Not(dst_reg_st_output_list[-1].get_contains64_predicate_only_signed(dst_conc_output_list[-1])),
    #         #     Not(Tnum.contains(dst_conc_output_list[-1], dst_reg_st_output_list[-1].var_off_value, dst_reg_st_output_list[-1].var_off_mask)),
    #         #     Not(dst_reg_st_output_list[-1].get_contains32_predicate_only_unsigned(dst32_conc_output_list[-1])),
    #         #     Not(dst_reg_st_output_list[-1].get_contains32_predicate_only_signed(dst32_conc_output_list[-1]))))

    #         solver.add(f_post_cond.list)

    #         ###############################################################################
    #         # Solve
    #         ###############################################################################
    #         num_tot_progs = str(len(list(itertools.product(*prog_set_list))))
    #         #str(len(list(powerset(OPS_set)))))
    #         end_time = 0
    #         check_output = None
    #         #1.5 minute timer for each program
    #         #solver.set("timeout", 1000*90 )
            
    #         #if prog[-1] == "BPF_AND" or prog[-1] == "BPF_OR" or prog[-1] == "BPF_XOR":
    #         if 1:
    #             #print(prog)
    #             #print_register_mappings(dst_reg_st_input_list, src_reg_st_input_list, dst_reg_st_output_list, prog_size)
    #             #print_specification(f_gen_const, f_pre_cond,  f_post_cond)
    #             check_output = str(solver.check())
    #             end_time = time.time()
    #             perf_dic[prog] = (end_time-start_time, check_output)
                
    #             try:
    #                 # if check_output == "unsat":
    #                 #     #solver.pop()
    #                 #     print("--------------------")
    #                 #     print("unsat")
    #                 #     print("--------------------")
    #                 if check_output == "sat":
    #                     # if solver.model() in bad_states:
    #                     #     continue
    #                     # else:
    #                     #     bad_states.append(solver.model())
    #                     #print mappings from bpf instruction encodings to our smt formula
    #                     print_register_mappings(dst_reg_st_input_list, src_reg_st_input_list, dst_reg_st_output_list, prog_size)

    #                     print_specification(f_gen_const, f_pre_cond,  f_post_cond)

    #                     print_synthesis_model(solver, dst_reg_st_input_list, src_reg_st_input_list, dst_reg_st_output_list, prog_size)

    #                     print_synthesized_program(solver, dst_conc_input_list, src_conc_input_list, dst_conc_output_list, bpf_OP, prog_size)
    #                     #break
    #                 elif check_output == "unknown":  
    #                     failed_unknown_prog_list.append(prog)
    #                     # print("--------------------")
    #                     # print("unknown")
    #                     # print("--------------------")
    #                     timeout_counter += 1
    #             except Exception as e:
    #                 print(e)
    #                 failed_exception_prog_list.append(prog)
    #                 print("--------------------")
    #                 print("z3 exception")
    #                 print("--------------------")
    #                 exception_counter += 1
    #             debug_stats(prog, num_tot_progs, iteration, timeout_counter, exception_counter, invalid_counter, failed_unknown_prog_list, failed_exception_prog_list, perf_dic, end_time-start_time, end_time - elapsed_time)
    #         # else:
    #         #     invalid_counter += 1
    #         #     end_time = time.time()

    #         iteration += 1
    #     #add set of instructions for the next iteration
    #     prog_set_list.insert(0, OPS_set)
    #     k += 1