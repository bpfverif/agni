#!/usr/bin/python3

import argparse
import glob
import json
from pprint import pprint, pformat
import sys
from collections import OrderedDict
import struct
import os

class BPF_PROG:

    alu_ops = [
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

    jmp_ops = [
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

    alu_macro_template = "BPF_ALU{bitness}_REG({bpf_alu_op}, BPF_REG_{dst_reg}, BPF_REG_{src_reg}),"
    jump_macro_template = "BPF_JMP{bitness}_REG({bpf_jmp_op}, BPF_REG_{dst_reg}, BPF_REG_{src_reg}, {offset}),"
    reg_singleton_macro_template = "BPF_LD_IMM64(BPF_REG_{dst_reg}, {imm_value}),"
    reg_unknown_macro_template_0 = "BPF_LD_IMM64(BPF_REG_{dst_reg}, {imm_value}),"
    reg_unknown_macro_template_1 = "BPF_ALU64_IMM(BPF_NEG, BPF_REG_{dst_reg}, 0),"
    reg_unknown_macro_template_2 = "BPF_ALU64_IMM(BPF_NEG, BPF_REG_{dst_reg}, 0),"
    exit_macro_template_0 = "BPF_MOV64_IMM(BPF_REG_0, 1),"
    exit_macro_template_1 = "BPF_EXIT_INSN(),"

    def debug_print(self, s):
        if self.debug_level == 2:
            print(str(s))

    def __repr__(self):
        s = ""
        for line_num, insn_macro in self.bpf_prog.items():
            s = s + "{:2} {}\n".format(line_num, insn_macro)
        return s.rstrip()

    def __str__(self):
        s = ""
        for line_num, insn_macro in self.bpf_prog.items():
            s = s + "{}\n".format(insn_macro)
        return s.rstrip()
    
    def write_to_file(self, file):
        with open(file, "w") as f:
            f.write(str(self))

    def __jsonfile_to_array(self, json_filepath):
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

    def is_alu_op(self, op):
        op = op.strip("_32")
        return op in BPF_PROG.alu_ops

    def is_jump_op(self, op):
        op = op.strip("_32")
        return op in BPF_PROG.jmp_ops

    def reg_st_is_completely_unknown(self, reg_st):
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

    def reg_sts_are_equal(self, reg_st_1, reg_st_2):
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

    def reg_st_is_singleton(self, reg_st):

        return (
            reg_st["var_off_mask"] == 0
            and (reg_st["var_off_value"] ==
                 reg_st["umin_value"] ==
                 reg_st["umax_value"])
            and (reg_st["smin_value"] ==
                 reg_st["smax_value"])
            and (reg_st["s32_min_value"] ==
                 reg_st["s32_max_value"])
            and (reg_st["u32_min_value"] ==
                 reg_st["u32_max_value"])
        )

    def is_jump_true_or_false(self, opcode, reg_sts_dict):
        # unsigned less/greater
        if (opcode == "BPF_JLE_32"):
            return reg_sts_dict["dst_inp"]["conc32"] <= reg_sts_dict["src_inp"]["conc32"]
        if (opcode == "BPF_JLE"):
            return reg_sts_dict["dst_inp"]["conc64"] <= reg_sts_dict["src_inp"]["conc64"]

        if (opcode == "BPF_JLT_32"):
            return reg_sts_dict["dst_inp"]["conc32"] < reg_sts_dict["src_inp"]["conc32"]
        if (opcode == "BPF_JLT"):
            return reg_sts_dict["dst_inp"]["conc64"] < reg_sts_dict["src_inp"]["conc64"]

        if (opcode == "BPF_JGE_32"):
            return reg_sts_dict["dst_inp"]["conc32"] >= reg_sts_dict["src_inp"]["conc32"]
        if (opcode == "BPF_JGE"):
            return reg_sts_dict["dst_inp"]["conc64"] >= reg_sts_dict["src_inp"]["conc64"]

        if (opcode == "BPF_JGT_32"):
            return reg_sts_dict["dst_inp"]["conc32"] > reg_sts_dict["src_inp"]["conc32"]
        if (opcode == "BPF_JGT"):
            return reg_sts_dict["dst_inp"]["conc64"] > reg_sts_dict["src_inp"]["conc64"]

        # signed less/greater
        if (opcode == "BPF_JSLE_32"):
            return reg_sts_dict["dst_inp"]["conc32"] <= reg_sts_dict["src_inp"]["conc32"]
        if (opcode == "BPF_JSLE"):
            return reg_sts_dict["dst_inp"]["conc64"] <= reg_sts_dict["src_inp"]["conc64"]

        if (opcode == "BPF_JSLT_32"):
            return reg_sts_dict["dst_inp"]["conc32"] < reg_sts_dict["src_inp"]["conc32"]
        if (opcode == "BPF_JSLT"):
            return reg_sts_dict["dst_inp"]["conc64"] < reg_sts_dict["src_inp"]["conc64"]

        if (opcode == "BPF_JSGE_32"):
            return reg_sts_dict["dst_inp"]["conc32"] >= reg_sts_dict["src_inp"]["conc32"]
        if (opcode == "BPF_JSGE"):
            return reg_sts_dict["dst_inp"]["conc64"] >= reg_sts_dict["src_inp"]["conc64"]

        if (opcode == "BPF_JSGT_32"):
            return reg_sts_dict["dst_inp"]["conc32"] > reg_sts_dict["src_inp"]["conc32"]
        if (opcode == "BPF_JSGT"):
            return reg_sts_dict["dst_inp"]["conc64"] > reg_sts_dict["src_inp"]["conc64"]

        # equal/not equal
        if (opcode == "BPF_JNE_32"):
            return reg_sts_dict["dst_inp"]["conc32"] != reg_sts_dict["src_inp"]["conc32"]
        if (opcode == "BPF_JNE"):
            return reg_sts_dict["dst_inp"]["conc64"] != reg_sts_dict["src_inp"]["conc64"]
        if (opcode == "BPF_JEQ_32"):
            return reg_sts_dict["dst_inp"]["conc32"] == reg_sts_dict["src_inp"]["conc32"]
        if (opcode == "BPF_JEQ"):
            return reg_sts_dict["dst_inp"]["conc64"] == reg_sts_dict["src_inp"]["conc64"]

    def assign_reg_singleton(self, reg_st_type, insn_reg_sts_dict):
        assigned_reg = self.reg_pool.pop()
        if reg_st_type == "dst":
            insn_reg_sts_dict["dst_reg_num"] = assigned_reg
        elif reg_st_type == "src":
            insn_reg_sts_dict["src_reg_num"] = assigned_reg
        return assigned_reg

    def assign_reg_completely_unknown(self, reg_st_type, insn_reg_sts_dict):
        assigned_reg = self.reg_pool.pop()
        if reg_st_type == "dst":
            insn_reg_sts_dict["dst_reg_num"] = assigned_reg
        elif reg_st_type == "src":
            insn_reg_sts_dict["src_reg_num"] = assigned_reg
        return assigned_reg

    def assign_reg_from_prev_insn(self, reg_st_type, poc_insn_num, insn_reg_sts_dict):
        if reg_st_type == "dst":
            curr_reg_st = insn_reg_sts_dict["dst_inp"]
        elif reg_st_type == "src":
            curr_reg_st = insn_reg_sts_dict["src_inp"]

        for j in range(poc_insn_num-1, -1, -1):
            prev_reg_st = self.jsonpoc[j]
            equal_to_prev_dst_out = self.reg_sts_are_equal(
                prev_reg_st["dst_out"], curr_reg_st)
            equal_to_prev_src_out = self.reg_sts_are_equal(
                prev_reg_st["src_out"], curr_reg_st)
            if equal_to_prev_dst_out and reg_st_type == "dst":
                insn_reg_sts_dict["dst_reg_num"] = prev_reg_st["dst_reg_num"]
                return j, prev_reg_st["dst_reg_num"], "dst"
            elif equal_to_prev_dst_out and reg_st_type == "src":
                insn_reg_sts_dict["src_reg_num"] = prev_reg_st["dst_reg_num"]
                return j, prev_reg_st["dst_reg_num"], "dst"
            elif equal_to_prev_src_out and reg_st_type == "dst":
                insn_reg_sts_dict["dst_reg_num"] = prev_reg_st["src_reg_num"]
                return j, prev_reg_st["src_reg_num"], "src"
            elif equal_to_prev_src_out and reg_st_type == "src":
                insn_reg_sts_dict["src_reg_num"] = prev_reg_st["src_reg_num"]
                return j, prev_reg_st["src_reg_num"], "src"

    def emit_insn_singleton(self, assigned_reg, conc64):
        self.bpf_prog[self.bpf_prog_line_num] = BPF_PROG.reg_singleton_macro_template.format(
            dst_reg=str(assigned_reg),
            imm_value=conc64
        )
        # BPF_LD_IMM64 is a two instruction macro
        self.bpf_prog_line_num += 2

    def emit_insn_completely_unknown(self, assigned_reg, conc64):
        self.bpf_prog[self.bpf_prog_line_num] = BPF_PROG.reg_unknown_macro_template_0.format(
            dst_reg=str(assigned_reg),
            imm_value=conc64
        )
        # BPF_LD_IMM64 is a two instruction macro
        self.bpf_prog_line_num += 2
        self.bpf_prog[self.bpf_prog_line_num] = BPF_PROG.reg_unknown_macro_template_1.format(
            dst_reg=str(assigned_reg)
        )
        self.bpf_prog_line_num += 1
        self.bpf_prog[self.bpf_prog_line_num] = BPF_PROG.reg_unknown_macro_template_2.format(
            dst_reg=str(assigned_reg)
        )
        self.bpf_prog_line_num += 1

    def emit_alu_insn(self, bitness, opcode, dst_reg_num, src_reg_num):
        self.bpf_prog[self.bpf_prog_line_num] = BPF_PROG.alu_macro_template.format(
            bitness=bitness,
            bpf_alu_op=opcode,
            dst_reg=dst_reg_num,
            src_reg=src_reg_num
        )
        self.bpf_prog_line_num += 1

    def emit_jump_insn(self, bitness, opcode, dst_reg_num, src_reg_num, offset):
        self.bpf_prog[self.bpf_prog_line_num] = BPF_PROG.jump_macro_template.format(
            bitness=bitness,
            bpf_jmp_op=opcode,
            dst_reg=dst_reg_num,
            src_reg=src_reg_num,
            offset=offset
        )
        if offset == "{offset}":
            self.jump_insn_stack.append(self.bpf_prog_line_num)
        self.bpf_prog_line_num += 1

    def emit_exit_insns(self):
        self.bpf_prog[self.bpf_prog_line_num] = BPF_PROG.exit_macro_template_0
        self.bpf_prog_line_num += 1
        self.bpf_prog[self.bpf_prog_line_num] = BPF_PROG.exit_macro_template_1
        self.bpf_prog_line_num += 1

    def resolve_jump_insn_offsets(self):
        while len(self.jump_insn_stack) != 0:
            i = self.jump_insn_stack.pop()
            offset = self.bpf_prog_line_num - i - 1
            self.bpf_prog[i] = self.bpf_prog[i].format(offset=str(offset))
            self.bpf_prog[self.bpf_prog_line_num] = BPF_PROG.exit_macro_template_0
            self.bpf_prog_line_num += 1
            self.bpf_prog[self.bpf_prog_line_num] = BPF_PROG.exit_macro_template_1
            self.bpf_prog_line_num += 1

    def generate_bpf_prog(self):
        for i, reg_sts_dict_i in enumerate(self.jsonpoc):
            bitness = 32 if "_32" in reg_sts_dict_i["insn"] else 64
            opcode = reg_sts_dict_i["insn"].strip("_32")
            self.debug_print("insn: {}; opcode: {}; bitness: {}".format(
                i, opcode, str(bitness)))
            
            assert (self.is_alu_op(opcode) or self.is_jump_op(opcode))

            # figure out dst input
            dst_inp_reg_st = reg_sts_dict_i["dst_inp"]
            dst_inp_conc64 = dst_inp_reg_st["conc64"]
            if self.reg_st_is_singleton(dst_inp_reg_st):
                assigned_reg_dst = self.assign_reg_singleton("dst", reg_sts_dict_i)
                self.emit_insn_singleton(assigned_reg_dst, dst_inp_conc64)
                self.debug_print(
                    "dst reg is singleton, assigned reg: {}".format(assigned_reg_dst))
            elif self.reg_st_is_completely_unknown(dst_inp_reg_st):
                assigned_reg_dst = self.assign_reg_completely_unknown(
                    "dst", reg_sts_dict_i)
                self.emit_insn_completely_unknown(assigned_reg_dst, dst_inp_conc64)
                self.debug_print(
                    "dst reg is unknown, assigned reg: {}".format(assigned_reg_dst))
            else:
                prev_insn_num, assigned_reg_dst, prev_insn_reg_type = self.assign_reg_from_prev_insn(
                    "dst", i, reg_sts_dict_i)
                self.debug_print(
                    "dst reg is from prev insn (#{}, {} reg), assigned reg: {}".format(prev_insn_num, prev_insn_reg_type, assigned_reg_dst))
            if "dst_reg_num" not in reg_sts_dict_i:
                raise RuntimeError("Unable to find reg to assign to.\n"
                                   "POC insn number: {}, opcode: {}, dst_inp".format(str(i), opcode))

            # figure out src input
            src_inp_reg_st = reg_sts_dict_i["src_inp"]
            src_inp_conc64 = src_inp_reg_st["conc64"]
            if self.reg_st_is_singleton(src_inp_reg_st):
                assigned_reg_src = self.assign_reg_singleton("src", reg_sts_dict_i)
                self.emit_insn_singleton(assigned_reg_src, src_inp_conc64)
                self.debug_print(
                    "src reg is singleton, assigned reg: {}".format(assigned_reg_src))
            elif self.reg_st_is_completely_unknown(src_inp_reg_st):
                assigned_reg_src = self.assign_reg_completely_unknown(
                    "src", reg_sts_dict_i)
                self.emit_insn_completely_unknown(assigned_reg_src, src_inp_conc64)
                self.debug_print(
                    "src reg is unknown, assigned reg: {}".format(assigned_reg_src))
            else:
                prev_insn_num, assigned_reg_src, prev_insn_reg_type = self.assign_reg_from_prev_insn(
                    "src", i, reg_sts_dict_i)
                self.debug_print(
                    "src reg is from prev insn (#{}, {} reg), assigned reg: {}".format(prev_insn_num, prev_insn_reg_type, assigned_reg_src))
            if "src_reg_num" not in reg_sts_dict_i:
                raise RuntimeError("Unable to find reg to assign to.\n"
                                   "POC insn number: {}, opcode: {}, src_inp".format(str(i), opcode))

            # emit ALU instruction macros
            if self.is_alu_op(opcode):
                self.emit_alu_insn("32" if bitness == 32 else "64",
                                   opcode,
                                   str(reg_sts_dict_i["dst_reg_num"]),
                                   str(reg_sts_dict_i["src_reg_num"]))
                # if this is the last instruction, exit
                if i == len(self.jsonpoc) - 1:
                    self.debug_print("last instruction")
                    self.emit_exit_insns()

            # emit JUMP instruction macros
            if self.is_jump_op(opcode):
                # if this is the last instruction, both true and false paths lead to exit
                if i == len(self.jsonpoc) - 1:
                    self.debug_print("last instruction")
                    self.emit_jump_insn("32" if bitness == 32 else "",
                                        opcode,
                                        str(reg_sts_dict_i["dst_reg_num"]),
                                        str(reg_sts_dict_i["src_reg_num"]),
                                        offset="2")
                    self.emit_exit_insns()  # false path exit
                    self.emit_exit_insns()  # true path exit
                else:
                    jump_outcome = self.is_jump_true_or_false(
                        opcode, reg_sts_dict_i)
                    if jump_outcome == True:
                        self.debug_print("jump outcome is True")
                        self.emit_jump_insn("32" if bitness == 32 else "",
                                            opcode,
                                            str(reg_sts_dict_i["dst_reg_num"]),
                                            str(reg_sts_dict_i["src_reg_num"]),
                                            offset="2")
                        self.emit_exit_insns()  # the fall-through leads to exit
                    else:
                        self.debug_print("jump outcome is False")
                        self.emit_jump_insn("32" if bitness == 32 else "",
                                            opcode,
                                            str(reg_sts_dict_i["dst_reg_num"]),
                                            str(reg_sts_dict_i["src_reg_num"]),
                                            offset="{offset}")
                        
            # if this is the last instruction, save the reg numbers
            if i == len(self.jsonpoc) - 1:
                self.final_insn_dst_reg = assigned_reg_dst
                self.final_insn_src_reg = assigned_reg_src
                self.debug_print("reg numbers: dst {}, src {}".format(self.final_insn_dst_reg, self.final_insn_src_reg))

            self.debug_print("----------")

        # now resolve jump offsets if any
        self.resolve_jump_insn_offsets()

    def setup_bpf(self):
        pass


    def __init__(self, json_poc_filepath, debug_level):
        self.reg_pool = set([1, 2, 3, 4, 5, 6, 7, 8, 9])
        self.bpf_prog = OrderedDict()
        self.bpf_prog_line_num = 0
        self.jump_insn_stack = []
        self.jsonpoc = self.__jsonfile_to_array(json_poc_filepath)
        self.debug_level = debug_level
        self.final_insn_dst_reg = -1
        self.final_insn_src_reg = -1


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--jsondir",
                        help="the directory containing all the POCs in JSON format",
                        type=str,
                        required=False)
    parser.add_argument("--debug_level",
                        help="Debug level: 1 or 2",
                        required=False,
                        default=2,
                        type=int)
    parser.add_argument("--jsonfile",
                        help="single json POC file",
                        type=str,
                        required=False)
    args = parser.parse_args()

    if args.jsonfile:
        if args.debug_level == 2:
            print(args.jsonfile)
        bpf_prog_i = BPF_PROG(args.jsonfile, debug_level=args.debug_level)
        if args.debug_level == 2:
            print(pformat(bpf_prog_i.jsonpoc))
        bpf_prog_i.generate_bpf_prog()
        print(bpf_prog_i)
    elif args.jsondir:
        file_pattern = "{}/*.json".format(args.jsondir)
        file_list = glob.glob(file_pattern)
        for i, json_poc_filepath in enumerate(file_list):
            poc_str = os.path.splitext(os.path.basename(json_poc_filepath))[0]
            if args.debug_level == 2:
                print(json_poc_filepath)
            bpf_prog_i = BPF_PROG(
                json_poc_filepath, debug_level=args.debug_level)
            if args.debug_level == 2:
                print(pformat(bpf_prog_i.jsonpoc))
            bpf_prog_i.generate_bpf_prog()
            bpf_prog_i.write_to_file(args.jsondir + "/prog_{}.txt".format(poc_str))
            print(bpf_prog_i)
            print("")
    else:
        print("Either --jsondir or --jsonfile required")
