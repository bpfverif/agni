import json
from pprint import pprint
import sys

bpf_alu_ops = [
    "BPF_ADD",
    "BPF_SUB",
    "BPF_OR",
    "BPF_AND",
    "BPF_LSH",
    "BPF_RSH",
    "BPF_ARSH",  # TODO started only in ?
    "BPF_XOR"  # TODO started only in 5.10
    # "BPF_MUL", # ignore
    # "BPF_DIV", # ignore
    # "BPF_NEG", # ignore
    # "BPF_MOD", # ignore

]

bpf_jmp_ops = [
    "BPF_JEQ",
    "BPF_JNE",
    # "BPF_JSET",  # TODO started only in ? + doesn't work. comment out for now
    "BPF_JGE",
    "BPF_JGT",
    "BPF_JSGE",
    "BPF_JSGT",
    "BPF_JLE",
    "BPF_JLT",
    "BPF_JSLE",
    "BPF_JSLT"
]


def is_singleton(reg_st):
    return (
        reg_st["var_off_mask"] == 0
        and (reg_st["var_off_value"] ==
             reg_st["smin_value"] ==
             reg_st["smax_value"] ==
             reg_st["umin_value"] ==
             reg_st["umax_value"])
        and (reg_st["s32_min_value"] ==
             reg_st["s32_max_value"] ==
             reg_st["u32_min_value"] ==
             reg_st["u32_max_value"])
    )

# TODO update
# def is_completely_unknown(reg_st):
#     return (
#         reg_st["var_off_value"] == 0
#         and reg_st["var_off_mask"] == 18446744073709551615
#         and reg_st["smin_value"] == -9223372036854775808
#         and reg_st["smax_value"] == 9223372036854775807
#         and reg_st["umin_value"] == 0
#         and reg_st["umax_value"] == 18446744073709551615
#         and reg_st["s32_min_value"] == -2147483648
#         and reg_st["s32_max_value"] == 2147483647
#         and reg_st["u32_min_value"] == 0
#         and reg_st["u32_max_value"] == 4294967295
#     )


def is_completely_unknown(reg_st):
    return (
        reg_st["var_off_value"] == 0
        and reg_st["var_off_mask"] == 18446744073709551615
        and reg_st["smin_value"] == 9223372036854775808
        and reg_st["smax_value"] == 9223372036854775807
        and reg_st["umin_value"] == 0
        and reg_st["umax_value"] == 18446744073709551615
        and reg_st["s32_min_value"] == 2147483648
        and reg_st["s32_max_value"] == 2147483647
        and reg_st["u32_min_value"] == 0
        and reg_st["u32_max_value"] == 4294967295
    )


def is_equal(reg_st_1, reg_st_2):
    return (
        reg_st_1["conc64"] == reg_st_2["conc64"]
        and reg_st_1["conc32"] == reg_st_2["conc32"]
        and reg_st_1["var_off_value"] == reg_st_2["var_off_value"]
        and reg_st_1["smin_value"] == reg_st_2["smin_value"]
        and reg_st_1["smax_value"] == reg_st_2["smax_value"]
        and reg_st_1["umin_value"] == reg_st_2["umin_value"]
        and reg_st_1["umax_value"] == reg_st_2["umax_value"]
        and reg_st_1["s32_min_value"] == reg_st_2["s32_min_value"]
        and reg_st_1["s32_max_value"] == reg_st_2["s32_max_value"]
        and reg_st_1["u32_min_value"] == reg_st_2["u32_min_value"]
        and reg_st_1["u32_max_value"] == reg_st_2["u32_max_value"]

    )


def is_alu_op(op):
    op = op.strip("_32")
    return op in bpf_alu_ops


def is_jump_op(op):
    op = op.strip("_32")
    return op in bpf_jmp_ops


def jsonfile_to_array(json_filepath):
    f = open(json_filepath, "r")
    s = f.read()
    json_obj_dict = json.loads(s)

    poc = []
    i = 0
    for inst_num, vals in json_obj_dict.items():
        if int(inst_num) == i:
            poc.append(vals)
        i += 1
    return poc


def print_bpf_prog(bpf_prog):
    print("-------------------------------")
    for prog in bpf_prog.items():
        print("{}".format(prog[1]))
    print("-------------------------------")

############################################################
# main
############################################################


reg_pool = set([1, 2, 3, 4, 5, 6, 7, 8, 9])

alu_macro_template = "BPF_ALU{bitness}_REG({bpf_alu_op}, BPF_REG_{dst_reg}, BPF_REG_{src_reg}),"
jump_macro_template = "BPF_JMP{bitness}_REG({bpf_jmp_op}, BPF_REG_{dst_reg}, BPF_REG_{src_reg}, {offset}),"
reg_singleton_macro_template = "BPF_LD_IMM64(BPF_REG_{dst_reg}, {imm_value}),"
reg_unknown_macro_template_0 = "BPF_LD_IMM64(BPF_REG_{dst_reg}, {imm_value}),"
reg_unknown_macro_template_1 = "BPF_ALU64_IMM(BPF_NEG, BPF_REG_{dst_reg}, 0),"
reg_unknown_macro_template_2 = "BPF_ALU64_IMM(BPF_NEG, BPF_REG_{dst_reg}, 0),"
exit_macro_template_0 = "BPF_MOV64_IMM(BPF_REG_0, 1),"
exit_macro_template_1 = "BPF_EXIT_INSN(),"

bpf_prog = {}
bpf_prog_line_num = 0

poc_from_synthesis = jsonfile_to_array(
    "/home/harishankarv/rutgers/srinivas/bpf_synthesis/jsons/5.9_and32_s32.json")


def handle_reg_is_singleton(reg_states_dict, conc64, is_reg_dst):
    global bpf_prog_line_num
    assigned_reg = reg_pool.pop()
    if is_reg_dst:
        reg_states_dict["dst_reg_num"] = assigned_reg
    else:
        reg_states_dict["src_reg_num"] = assigned_reg
    bpf_prog[bpf_prog_line_num] = reg_singleton_macro_template.format(
        dst_reg=str(assigned_reg),
        imm_value=conc64
    )
    bpf_prog_line_num += 1


def handle_reg_is_completely_unknown(reg_states_dict, conc64, is_reg_dst):
    global bpf_prog_line_num
    assigned_reg = reg_pool.pop()
    if is_reg_dst:
        reg_states_dict["dst_reg_num"] = assigned_reg
    else:
        reg_states_dict["src_reg_num"] = assigned_reg
    bpf_prog[bpf_prog_line_num] = reg_unknown_macro_template_0.format(
        dst_reg=str(assigned_reg),
        imm_value=conc64
    )
    bpf_prog_line_num += 1
    bpf_prog[bpf_prog_line_num] = reg_unknown_macro_template_1.format(
        dst_reg=str(assigned_reg)
    )
    bpf_prog_line_num += 1
    bpf_prog[bpf_prog_line_num] = reg_unknown_macro_template_2.format(
        dst_reg=str(assigned_reg)
    )
    bpf_prog_line_num += 1


def handle_reg_is_from_prev_insn(poc_insn_num, reg_states_dict, is_reg_dst):
    if is_reg_dst:
        curr_reg_st = reg_states_dict["dst_inp"]
    else:
        curr_reg_st = reg_states_dict["src_inp"]

    for j in range(poc_insn_num-1, -1, -1):
        prev_reg_st = poc_from_synthesis[j]
        equal_to_prev_dst_out = is_equal(prev_reg_st["dst_out"], curr_reg_st)
        equal_to_prev_src_out = is_equal(prev_reg_st["src_out"], curr_reg_st)
        if equal_to_prev_dst_out and is_reg_dst:
            reg_states_dict["dst_reg_num"] = prev_reg_st["dst_reg_num"]
        elif equal_to_prev_dst_out and (not is_reg_dst):
            reg_states_dict["src_reg_num"] = prev_reg_st["dst_reg_num"]
        elif equal_to_prev_src_out and is_reg_dst:
            reg_states_dict["dst_reg_num"] = prev_reg_st["src_reg_num"]
        elif equal_to_prev_src_out and (not is_reg_dst):
            reg_states_dict["src_reg_num"] = prev_reg_st["src_reg_num"]
        return j


for i, reg_sts_dict_i in enumerate(poc_from_synthesis):
    print("----------")
    print("insn: {}".format(i))
    # pprint(dict_i)
    bitness_is_32 = "_32" in reg_sts_dict_i["insn"]
    opcode = reg_sts_dict_i["insn"].strip("_32")
    dst_inp = reg_sts_dict_i["dst_inp"]
    src_inp = reg_sts_dict_i["src_inp"]
    dst_out = reg_sts_dict_i["dst_out"]
    src_out = reg_sts_dict_i["src_out"]

    # figure out dst input
    if is_singleton(dst_inp):
        handle_reg_is_singleton(reg_sts_dict_i, dst_inp["conc64"], True)
        print("src reg is singleton")
    elif is_completely_unknown(dst_inp):
        handle_reg_is_completely_unknown(
            reg_sts_dict_i, dst_inp["conc64"], True)
        print("src reg is unknown")
    else:
        prev_insn = handle_reg_is_from_prev_insn(i, reg_sts_dict_i, True)
        print("src reg is from prev insn {}".format(prev_insn))
    if "dst_reg_num" not in reg_sts_dict_i:
        raise RuntimeError("Unable to find reg to assign to.\n"
                           "POC insn number: {}, opcode: {}, dst_inp".format(str(i), opcode))

    # figure out src input
    if is_singleton(src_inp):
        handle_reg_is_singleton(reg_sts_dict_i, src_inp["conc64"], False)
        print("dst reg is singleton")
    elif is_completely_unknown(src_inp):
        handle_reg_is_completely_unknown(
            reg_sts_dict_i, src_inp["conc64"], False)
        print("dst reg is unknown")
    else:
        prev_insn = handle_reg_is_from_prev_insn(i, reg_sts_dict_i, False)
        print("dst reg is from prev insn {}".format(prev_insn))
    if "src_reg_num" not in reg_sts_dict_i:
        raise RuntimeError("Unable to find reg to assign to.\n"
                           "POC insn number: {}, opcode: {}, src_inp".format(str(i), opcode))
        ####################################################

    if is_alu_op(opcode):
        insn_macro = alu_macro_template.format(
            bitness="32" if bitness_is_32 else "",
            bpf_alu_op=opcode,
            dst_reg=str(reg_sts_dict_i["dst_reg_num"]),
            src_reg=str(reg_sts_dict_i["src_reg_num"])
        )
        bpf_prog[bpf_prog_line_num] = insn_macro
        bpf_prog_line_num += 1
        # pprint(dict_i)

print_bpf_prog(bpf_prog)
