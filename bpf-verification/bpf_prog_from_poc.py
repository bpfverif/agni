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
def is_completely_unknown(reg_st):
    return (
        reg_st["var_off_value"] == 0
        and reg_st["var_off_mask"] == 18446744073709551615
        and reg_st["smin_value"] == -9223372036854775808
        and reg_st["smax_value"] == 9223372036854775807
        and reg_st["umin_value"] == 0
        and reg_st["umax_value"] == 18446744073709551615
        and reg_st["s32_min_value"] == -2147483648
        and reg_st["s32_max_value"] == 2147483647
        and reg_st["u32_min_value"] == 0
        and reg_st["u32_max_value"] == 4294967295
    )


def is_equal(reg_st_1, reg_st_2):
    return (
        reg_st_1["var_off_value"] == reg_st_2["var_off_value"]
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
    # print("-------------------------------")
    for line_num, prog in bpf_prog.items():
        print("{}.".format(line_num), prog)
    # print("-------------------------------")


reg_pool = set([1, 2, 3, 4, 5, 6, 7, 8, 9])

alu_template = "BPF_ALU{bitness}_REG({bpf_alu_op}, BPF_REG_{dst_reg}, BPF_REG_{src_reg}),"
jump_template = "BPF_JMP{bitness}_REG({bpf_jmp_op}, BPF_REG_{dst_reg}, BPF_REG_{src_reg}, {offset}),"
reg_singleton_template = "BPF_LD_IMM64(BPF_REG_{dst_reg}, {imm_value}),"
reg_unknown_template_0 = "BPF_LD_IMM64(BPF_REG_{dst_reg}, {imm_value}),"
reg_unknown_template_1 = "BPF_ALU64_IMM(BPF_NEG, BPF_REG_{dst_reg}, 0),"
reg_unknown_template_2 = "BPF_ALU64_IMM(BPF_NEG, BPF_REG_{dst_reg}, 0),"
exit_template_0 = "BPF_MOV64_IMM(BPF_REG_0, 1),"
exit_template_1 = "BPF_EXIT_INSN(),"

bpf_prog = {}
bpf_prog_line_num = 0

poc_from_synthesis = jsonfile_to_array(
    "/home/harishankarv/rutgers/srinivas/bpf_synthesis/5.9_and32_s32.json")

############################################################
# main
############################################################

for i, dict_i in enumerate(poc_from_synthesis):
    # print(i, "----------")
    # pprint(dict_i)
    bitness_is_32 = "_32" in dict_i["insn"]
    opcode = dict_i["insn"].strip("_32")
    dst_inp = dict_i["dst_inp"]
    src_inp = dict_i["src_inp"]
    dst_out = dict_i["dst_out"]
    src_out = dict_i["src_out"]

    if is_alu_op(opcode):

        ####################################################
        if is_singleton(dst_inp):
            dict_i["dst_reg_num"] = reg_pool.pop()
            bpf_prog[bpf_prog_line_num] = reg_singleton_template.format(
                dst_reg=str(dict_i["dst_reg_num"]),
                imm_value=dst_inp["conc64"]
            )
            bpf_prog_line_num += 1
        elif is_completely_unknown(dst_inp):
            dict_i["dst_reg_num"] = reg_pool.pop()
            bpf_prog[bpf_prog_line_num] = reg_unknown_template_0.format(
                dst_reg=str(dict_i["dst_reg_num"]),
                imm_value=dst_inp["conc64"]
            )
            bpf_prog_line_num += 1
            bpf_prog[bpf_prog_line_num] = reg_unknown_template_1.format(
                dst_reg=str(dict_i["dst_reg_num"])
            )
            bpf_prog_line_num += 1
            bpf_prog[bpf_prog_line_num] = reg_unknown_template_2.format(
                dst_reg=str(dict_i["dst_reg_num"])
            )
            bpf_prog_line_num += 1
        else:
            for j in range(i-1, -1, -1):
                dict_j = poc_from_synthesis[j]
                if is_equal(dict_j["dst_out"], dst_inp):
                    dict_i["dst_reg_num"] = dict_j["dst_reg_num"]
                    break
                elif is_equal(dict_j["src_out"], dst_inp):
                    dict_i["dst_reg_num"] = dict_j["src_reg_num"]
                    break
        if "dst_reg_num" not in dict_i:
            raise RuntimeError("Unable to find reg to assign to.\n"
                               "POC insn number: {}, opcode: {}, dst_inp".format(str(i), opcode))

        ####################################################
        if is_singleton(src_inp):
            dict_i["src_reg_num"] = reg_pool.pop()
            bpf_prog[bpf_prog_line_num] = reg_singleton_template.format(
                dst_reg=str(dict_i["src_reg_num"]),
                imm_value=src_inp["conc64"]
            )
            bpf_prog_line_num += 1
        elif is_completely_unknown(src_inp):
            dict_i["src_reg_num"] = reg_pool.pop()
            bpf_prog[bpf_prog_line_num] = reg_unknown_template_0.format(
                dst_reg=str(dict_i["src_reg_num"]),
                imm_value=src_inp["conc64"]
            )
            bpf_prog_line_num += 1
            bpf_prog[bpf_prog_line_num] = reg_unknown_template_1.format(
                dst_reg=str(dict_i["src_reg_num"])
            )
            bpf_prog_line_num += 1
            bpf_prog[bpf_prog_line_num] = reg_unknown_template_2.format(
                dst_reg=str(dict_i["src_reg_num"])
            )
            bpf_prog_line_num += 1
        else:
            for j in range(i-1, -1, -1):
                dict_j = poc_from_synthesis[j]
                if is_equal(dict_j["dst_out"], src_inp):
                    dict_i["src_reg_num"] = dict_j["dst_reg_num"]
                    break
                elif is_equal(dict_j["src_out"], src_inp):
                    dict_i["src_reg_num"] = dict_j["src_reg_num"]
                    break
        if "src_reg_num" not in dict_i:
            raise RuntimeError("Unable to find reg to assign to.\n"
                               "POC insn number: {}, opcode: {}, src_inp".format(str(i), opcode))
        ####################################################

        insn_macro = alu_template.format(
            bitness="32" if bitness_is_32 else "",
            bpf_alu_op=opcode,
            dst_reg=str(dict_i["dst_reg_num"]),
            src_reg=str(dict_i["src_reg_num"])
        )
        bpf_prog[bpf_prog_line_num] = insn_macro
        bpf_prog_line_num += 1
        # pprint(dict_i)

print_bpf_prog(bpf_prog)
