#!/usr/bin/python3

import argparse
import subprocess
import sys
import pathlib
import os
import re
from termcolor import colored
from datetime import datetime
from packaging import version
import shutil
from run_llvm_passes import LLVMPassRunner
from wrappers import *
from typing import List


class bpf_op_attrs:
    def __init__(self, op_name, insn, insn_class, skip, intro_ver, suffix_id):
        self.op_name = op_name
        self.insn = insn
        self.insn_class = insn_class
        self.skip = skip
        self.intro_ver = intro_ver
        self.suffix_id = suffix_id
        if self.insn_class == 'BPF_ALU64_REG' or self.insn_class == 'BPF_ALU32_REG':
            self.function_name = "adjust_scalar_min_max_vals_wrapper_{}".format(
                self.op_name)
        elif self.insn_class == 'BPF_JMP_REG' or self.insn_class == 'BPF_JMP32_REG':
            self.function_name = "check_cond_jmp_op_wrapper_{}".format(
                self.op_name)
        elif self.insn_class == 'BPF_SYNC':
            self.function_name = "reg_bounds_sync___"
        else:
            raise RuntimeError(
                'Unsupported BPF insn_class {}'.format(insn_class))

    def __repr__(self):
        s = self.op_name + "_" + str(self.suffix_id)
        if self.skip:
            s += " (skip)"
        return s

# List of bpf ops we are interested in generating encodings for. Do not change 
# the suffix_ids of the ops below, they are meant to be the same across commits.
bpf_ops: List[bpf_op_attrs] = []

# 64-bit ALU ops
bpf_ops.append(bpf_op_attrs(op_name='BPF_ADD', insn='BPF_ADD', insn_class='BPF_ALU64_REG',
                            skip=False, intro_ver="3.18", suffix_id=0))
bpf_ops.append(bpf_op_attrs(op_name='BPF_SUB', insn='BPF_SUB', insn_class='BPF_ALU64_REG',
                            skip=False, intro_ver="3.18", suffix_id=1))
bpf_ops.append(bpf_op_attrs(op_name='BPF_MUL', insn='BPF_MUL', insn_class='BPF_ALU64_REG',
                            skip=True, intro_ver="3.18", suffix_id=2))
bpf_ops.append(bpf_op_attrs(op_name='BPF_DIV', insn='BPF_DIV', insn_class='BPF_ALU64_REG',
                            skip=True, intro_ver="3.18", suffix_id=3))
bpf_ops.append(bpf_op_attrs(op_name='BPF_OR', insn='BPF_OR', insn_class='BPF_ALU64_REG',
                            skip=False, intro_ver="3.18", suffix_id=4))
bpf_ops.append(bpf_op_attrs(op_name='BPF_AND', insn='BPF_AND', insn_class='BPF_ALU64_REG',
                            skip=False, intro_ver="3.18", suffix_id=5))
bpf_ops.append(bpf_op_attrs(op_name='BPF_LSH', insn='BPF_LSH', insn_class='BPF_ALU64_REG',
                            skip=False, intro_ver="3.18", suffix_id=6))
bpf_ops.append(bpf_op_attrs(op_name='BPF_RSH', insn='BPF_RSH', insn_class='BPF_ALU64_REG',
                            skip=False, intro_ver="3.18", suffix_id=7))
bpf_ops.append(bpf_op_attrs(op_name='BPF_NEG', insn='BPF_NEG', insn_class='BPF_ALU64_REG',
                            skip=True, intro_ver="3.18", suffix_id=8))
bpf_ops.append(bpf_op_attrs(op_name='BPF_MOD', insn='BPF_MOD', insn_class='BPF_ALU64_REG',
                            skip=True, intro_ver="3.18", suffix_id=9))
bpf_ops.append(bpf_op_attrs(op_name='BPF_XOR', insn='BPF_XOR', insn_class='BPF_ALU64_REG',
                            skip=False, intro_ver="3.18", suffix_id=10))
bpf_ops.append(bpf_op_attrs(op_name='BPF_ARSH', insn='BPF_ARSH', insn_class='BPF_ALU64_REG',
                            skip=False, intro_ver="3.18", suffix_id=11))

# 32-bit ALU ops
bpf_ops.append(bpf_op_attrs(op_name='BPF_ADD_32', insn='BPF_ADD', insn_class='BPF_ALU32_REG',
                            skip=False, intro_ver="3.18", suffix_id=12))
bpf_ops.append(bpf_op_attrs(op_name='BPF_SUB_32', insn='BPF_SUB', insn_class='BPF_ALU32_REG',
                            skip=False, intro_ver="3.18", suffix_id=13))
bpf_ops.append(bpf_op_attrs(op_name='BPF_MUL_32', insn='BPF_MUL', insn_class='BPF_ALU32_REG',
                            skip=True, intro_ver="3.18", suffix_id=14))
bpf_ops.append(bpf_op_attrs(op_name='BPF_DIV_32', insn='BPF_DIV', insn_class='BPF_ALU32_REG',
                            skip=True, intro_ver="3.18", suffix_id=15))
bpf_ops.append(bpf_op_attrs(op_name='BPF_OR_32', insn='BPF_OR', insn_class='BPF_ALU32_REG',
                                    skip=False, intro_ver="3.18", suffix_id=16))
bpf_ops.append(bpf_op_attrs(op_name='BPF_AND_32', insn='BPF_AND', insn_class='BPF_ALU32_REG',
                            skip=False, intro_ver="3.18", suffix_id=17))
bpf_ops.append(bpf_op_attrs(op_name='BPF_LSH_32', insn='BPF_LSH', insn_class='BPF_ALU32_REG',
                            skip=False, intro_ver="3.18", suffix_id=18))
bpf_ops.append(bpf_op_attrs(op_name='BPF_RSH_32', insn='BPF_RSH', insn_class='BPF_ALU32_REG',
                            skip=False, intro_ver="3.18", suffix_id=19))
bpf_ops.append(bpf_op_attrs(op_name='BPF_NEG_32', insn='BPF_NEG', insn_class='BPF_ALU32_REG',
                            skip=True, intro_ver="3.18", suffix_id=20))
bpf_ops.append(bpf_op_attrs(op_name='BPF_MOD_32', insn='BPF_MOD', insn_class='BPF_ALU32_REG',
                            skip=True, intro_ver="3.18", suffix_id=21))
bpf_ops.append(bpf_op_attrs(op_name='BPF_XOR_32', insn='BPF_XOR', insn_class='BPF_ALU32_REG',
                            skip=False, intro_ver="3.18", suffix_id=22))
bpf_ops.append(bpf_op_attrs(op_name='BPF_ARSH_32', insn='BPF_ARSH', insn_class='BPF_ALU32_REG',
                            skip=False, intro_ver="3.18", suffix_id=23))

# 64-bit jump ops
bpf_ops.append(bpf_op_attrs(op_name='BPF_JA', insn='BPF_JA', insn_class='BPF_JMP_REG',
                            skip=True, intro_ver="3.18", suffix_id=24))
bpf_ops.append(bpf_op_attrs(op_name='BPF_JEQ', insn='BPF_JEQ', insn_class='BPF_JMP_REG',
                            skip=False, intro_ver="3.18", suffix_id=25))
bpf_ops.append(bpf_op_attrs(op_name='BPF_JGT', insn='BPF_JGT', insn_class='BPF_JMP_REG',
                            skip=False, intro_ver="3.18", suffix_id=26))
bpf_ops.append(bpf_op_attrs(op_name='BPF_JGE', insn='BPF_JGE', insn_class='BPF_JMP_REG',
                            skip=False, intro_ver="3.18", suffix_id=27))
bpf_ops.append(bpf_op_attrs(op_name='BPF_JSET', insn='BPF_JSET', insn_class='BPF_JMP_REG',
                            skip=False, intro_ver="3.18", suffix_id=28))
bpf_ops.append(bpf_op_attrs(op_name='BPF_JNE', insn='BPF_JNE', insn_class='BPF_JMP_REG',
                            skip=False, intro_ver="3.18", suffix_id=29))
bpf_ops.append(bpf_op_attrs(op_name='BPF_JLT', insn='BPF_JLT', insn_class='BPF_JMP_REG',
                            skip=False, intro_ver="v4.14", suffix_id=30))
bpf_ops.append(bpf_op_attrs(op_name='BPF_JLE', insn='BPF_JLE', insn_class='BPF_JMP_REG',
                            skip=False, intro_ver="v4.14", suffix_id=31))
bpf_ops.append(bpf_op_attrs(op_name='BPF_JSGT', insn='BPF_JSGT', insn_class='BPF_JMP_REG',
                            skip=False, intro_ver="v4.14", suffix_id=32))
bpf_ops.append(bpf_op_attrs(op_name='BPF_JSGE', insn='BPF_JSGE', insn_class='BPF_JMP_REG',
                            skip=False, intro_ver="v4.14", suffix_id=33))
bpf_ops.append(bpf_op_attrs(op_name='BPF_JSLT', insn='BPF_JSLT', insn_class='BPF_JMP_REG',
                            skip=False, intro_ver="v4.14", suffix_id=34))
bpf_ops.append(bpf_op_attrs(op_name='BPF_JSLE', insn='BPF_JSLE', insn_class='BPF_JMP_REG',
                            skip=False, intro_ver="v4.14", suffix_id=35))

# 32-bit jump ops
bpf_ops.append(bpf_op_attrs(op_name='BPF_JA_32', insn='BPF_JA', insn_class='BPF_JMP32_REG',
                                    skip=True, intro_ver="5.1", suffix_id=36))
bpf_ops.append(bpf_op_attrs(op_name='BPF_JEQ_32', insn='BPF_JEQ', insn_class='BPF_JMP32_REG',
                            skip=False, intro_ver="5.1", suffix_id=37))
bpf_ops.append(bpf_op_attrs(op_name='BPF_JGT_32', insn='BPF_JGT', insn_class='BPF_JMP32_REG',
                            skip=False, intro_ver="5.1", suffix_id=38))
bpf_ops.append(bpf_op_attrs(op_name='BPF_JGE_32', insn='BPF_JGE', insn_class='BPF_JMP32_REG',
                            skip=False, intro_ver="5.1", suffix_id=39))
bpf_ops.append(bpf_op_attrs(op_name='BPF_JSET_32', insn='BPF_JSET', insn_class='BPF_JMP32_REG',
                            skip=False, intro_ver="5.1", suffix_id=40))
bpf_ops.append(bpf_op_attrs(op_name='BPF_JNE_32', insn='BPF_JNE', insn_class='BPF_JMP32_REG',
                            skip=False, intro_ver="5.1", suffix_id=41))
bpf_ops.append(bpf_op_attrs(op_name='BPF_JLT_32', insn='BPF_JLT', insn_class='BPF_JMP32_REG',
                            skip=False, intro_ver="5.1", suffix_id=42))
bpf_ops.append(bpf_op_attrs(op_name='BPF_JLE_32', insn='BPF_JLE', insn_class='BPF_JMP32_REG',
                            skip=False, intro_ver="5.1", suffix_id=43))
bpf_ops.append(bpf_op_attrs(op_name='BPF_JSGT_32', insn='BPF_JSGT', insn_class='BPF_JMP32_REG',
                            skip=False, intro_ver="5.1", suffix_id=44))
bpf_ops.append(bpf_op_attrs(op_name='BPF_JSGE_32', insn='BPF_JSGE', insn_class='BPF_JMP32_REG',
                            skip=False, intro_ver="5.1", suffix_id=45))
bpf_ops.append(bpf_op_attrs(op_name='BPF_JSLT_32', insn='BPF_JSLT', insn_class='BPF_JMP32_REG',
                            skip=False, intro_ver="5.1", suffix_id=46))
bpf_ops.append(bpf_op_attrs(op_name='BPF_JSLE_32', insn='BPF_JSLE', insn_class='BPF_JMP32_REG',
                            skip=False, intro_ver="5.1", suffix_id=47))

# refinement ops
bpf_ops.append(bpf_op_attrs(op_name='BPF_SYNC', insn='NA', insn_class="BPF_SYNC",
                            skip=False, intro_ver="5.19", suffix_id=48))

# Ops that are broken on < 6.10 kernels when using modular mode.
broken_ops_modular = ['BPF_AND', 'BPF_OR', 'BPF_XOR', 'BPF_AND_32', 'BPF_OR_32', 'BPF_XOR_32']

def insert_sync_wrapper(verifier_c_filepath, kernver):
    wrapper_sync = ''
    if version.parse(kernver) >= version.parse("6.8-rc1"):
        wrapper_sync = wrapper_sync_4
    elif version.parse(kernver) >= version.parse("5.19-rc6"):
        wrapper_sync = wrapper_sync_3
    elif version.parse(kernver) >= version.parse("5.7-rc1"):
        wrapper_sync = wrapper_sync_2
    elif version.parse(kernver) >= version.parse("4.14.214"):
        wrapper_sync = wrapper_sync_1
    else:
        raise RuntimeError('Unsupported kernel version')
    assert (len(wrapper_sync) != 0)

    inputfile_handle = verifier_c_filepath.open('r')
    input_file_lines = inputfile_handle.readlines()
    tmpdir_path = pathlib.Path("/tmp")
    tmpfile_name = datetime.now().strftime('tmp_verifier_%H_%M_%d_%m_%Y.c')
    tmpfile_path = tmpdir_path.joinpath(tmpfile_name)
    tmpfile_handle = tmpfile_path.open('w')
    func_start_found = False
    func_end_found = False
    func_insert_done = False
    parens = 0
    for line in input_file_lines:
        if not func_insert_done:
            if r"int adjust_scalar_min_max_vals(" in line:
                func_start_found = True
            if r"{" in line and func_start_found:
                parens += 1
            if r"}" in line and func_start_found:
                parens -= 1
                if parens == 0:
                    func_end_found = True
            tmpfile_handle.write(line)
            if func_end_found:
                tmpfile_handle.write(wrapper_sync)
                func_insert_done = True
        else:
            tmpfile_handle.write(line)

    tmpfile_handle.close()
    inputfile_handle.close()

    shutil.copy(tmpfile_path, verifier_c_filepath)


def get_all_jmp_wrappers_concatenated(kernver):
    wrapper_jmp = ''
    wrapper_jmp32 = ''

    if version.parse(kernver) >= version.parse("6.10-rc5"):
        # Starting with v6.10-rc5~30^2~33^2~6
        wrapper_jmp = wrapper_jmp_8
        wrapper_jmp32 = wrapper_jmp32_8
    elif version.parse(kernver) >= version.parse("6.8-rc1"):
        # Starting with v6.8-rc1~131^2~289^2~25.
        wrapper_jmp = wrapper_jmp_7
        wrapper_jmp32 = wrapper_jmp32_7
    elif version.parse(kernver) >= version.parse("6.4-rc1"):
        # Starting with v6.4-rc1~77^2~118^2~26^2~1.
        wrapper_jmp = wrapper_jmp_6
        wrapper_jmp32 = wrapper_jmp32_6
    elif version.parse(kernver) >= version.parse("5.7-rc1"):
        # Starting with v5.7-rc1~146^2~10^2~1^2~5.
        wrapper_jmp = wrapper_jmp_5
        wrapper_jmp32 = wrapper_jmp32_5
    elif version.parse(kernver) >= version.parse("5.3-rc1"):
        # Starting with v5.3-rc1~140^2~179^2^2~6.
        wrapper_jmp = wrapper_jmp_4
        wrapper_jmp32 = wrapper_jmp32_4
    elif version.parse(kernver) >= version.parse("5.1-rc1"):
        # Starting with v5.1-rc1~178^2~404^2~4^2~13.
        wrapper_jmp = wrapper_jmp_3
        wrapper_jmp32 = wrapper_jmp32_3

    # no 32-bit jumps before 5.1-rc1
    elif version.parse(kernver) >= version.parse("4.20-rc6"):
        # Starting with v4.20-rc6~1^2~12^2^2~1.
        wrapper_jmp = wrapper_jmp_2
    elif version.parse(kernver) >= version.parse("4.16-rc1"):
        # Starting with v4.16-rc1~123^2~431^2~2^2~2.
        wrapper_jmp = wrapper_jmp_1
    elif version.parse(kernver) >= version.parse("4.14.214"):
        wrapper_jmp = wrapper_jmp_0
    else:
        raise RuntimeError('Unsupported kernel version')
    assert (len(wrapper_jmp) != 0)

    bpf_jmp_ops = [op for op in bpf_ops if op.insn_class == 'BPF_JMP_REG' and op.skip == False]
    bpf_jmp32_ops = [op for op in bpf_ops if op.insn_class == 'BPF_JMP32_REG' and op.skip == False]
    s = ""
    for op in bpf_jmp_ops:
        s += wrapper_jmp.format(op.op_name, op.insn)
    # no 32-bit jumps before 5.1-rc1
    if version.parse(kernver) >= version.parse("5.1-rc1"):
        for op in bpf_jmp32_ops:
            s += wrapper_jmp32.format(op.op_name, op.insn)

    return s


def insert_jmp_wrapper(verifier_c_filepath, kernver):
    all_jmp_wrappers_concat = get_all_jmp_wrappers_concatenated(kernver)
    print(all_jmp_wrappers_concat)
    if version.parse(kernver) >= version.parse("5.7-rc1"):
        all_jmp_wrappers_concat = wrapper_push_stack_w32 + all_jmp_wrappers_concat
    else:
        # no 32-bit bounds until 5.7-rc1
        all_jmp_wrappers_concat = wrapper_push_stack_no32 + all_jmp_wrappers_concat
    inputfile_handle = verifier_c_filepath.open('r')
    input_file_lines = inputfile_handle.readlines()
    tmpdir_path = pathlib.Path("/tmp")
    tmpfile_name = datetime.now().strftime('tmp_verifier_%H_%M_%d_%m_%Y.c')
    tmpfile_path = tmpdir_path.joinpath(tmpfile_name)
    tmpfile_handle = tmpfile_path.open('w')
    func_start_found = False
    func_end_found = False
    func_insert_done = False
    parens = 0
    for line in input_file_lines:
        if not func_insert_done:
            if r"int check_cond_jmp_op(" in line:
                func_start_found = True
            if r"{" in line and func_start_found:
                parens += 1
            if r"}" in line and func_start_found:
                parens -= 1
                if parens == 0:
                    func_end_found = True
            tmpfile_handle.write(line)
            if func_end_found:
                tmpfile_handle.write(all_jmp_wrappers_concat)
                func_insert_done = True
        else:
            tmpfile_handle.write(line)

    tmpfile_handle.close()
    inputfile_handle.close()

    shutil.copy(tmpfile_path, verifier_c_filepath)


def insert_wrapper_unknown(verifier_c_filepath):
    inputfile_handle = verifier_c_filepath.open('r')
    input_file_lines = inputfile_handle.readlines()
    tmpdir_path = pathlib.Path("/tmp")
    tmpfile_name = datetime.now().strftime('tmp_verifier_%H_%M_%d_%m_%Y.c')
    tmpfile_path = tmpdir_path.joinpath(tmpfile_name)
    tmpfile_handle = tmpfile_path.open('w')
    func_start_found = False
    func_end_found = False
    func_insert_done = False
    parens = 0
    for line in input_file_lines:
        if not func_insert_done:
            if r"void __mark_reg_unbounded(" in line:
                func_start_found = True
            if r"{" in line and func_start_found:
                parens += 1
            if r"}" in line and func_start_found:
                parens -= 1
                if parens == 0:
                    func_end_found = True
            tmpfile_handle.write(line)
            if func_end_found:
                tmpfile_handle.write(wrapper_unknown)
                func_insert_done = True
        else:
            tmpfile_handle.write(line)

    tmpfile_handle.close()
    inputfile_handle.close()

    shutil.copy(tmpfile_path, verifier_c_filepath)


def get_all_alu_wrappers_concatenated():
    wrapper_alu = wrapper_alu_1
    wrapper_alu32 = wrapper_alu32_1
    bpf_alu_ops = [op for op in bpf_ops if op.insn_class == 'BPF_ALU64_REG'  and op.skip == False]
    bpf_alu32_ops = [op for op in bpf_ops if op.insn_class == 'BPF_ALU32_REG' and op.skip == False]
    s = ""
    for op in bpf_alu_ops:
        s += wrapper_alu.format(op.op_name, op.insn)
    for op in bpf_alu32_ops:
        s += wrapper_alu32.format(op.op_name, op.insn)
    return s


def insert_alu_wrapper(verifier_c_filepath):
    all_alu_wrappers_concat = get_all_alu_wrappers_concatenated()
    inputfile_handle = verifier_c_filepath.open('r')
    input_file_lines = inputfile_handle.readlines()
    tmpdir_path = pathlib.Path("/tmp")
    tmpfile_name = datetime.now().strftime('tmp_verifier_%H_%M_%d_%m_%Y.c')
    tmpfile_path = tmpdir_path.joinpath(tmpfile_name)
    tmpfile_handle = tmpfile_path.open('w')
    func_start_found = False
    func_end_found = False
    func_insert_done = False
    parens = 0
    for line in input_file_lines:
        if not func_insert_done:
            if r"int adjust_scalar_min_max_vals(" in line:
                func_start_found = True
            if r"{" in line and func_start_found:
                parens += 1
            if r"}" in line and func_start_found:
                parens -= 1
                if parens == 0:
                    func_end_found = True
            if func_start_found and "mark_reg_unknown" in line:
                line = re.sub(r'^(\s*)(mark_reg_unknown\()(.*)->(.+)(\))',
                              r'\1mark_reg_unknown___(\4)',
                              line)
            tmpfile_handle.write(line)
            if func_end_found:
                tmpfile_handle.write(all_alu_wrappers_concat)
                func_insert_done = True
        else:
            tmpfile_handle.write(line)

    tmpfile_handle.close()
    inputfile_handle.close()

    shutil.copy(tmpfile_path, verifier_c_filepath)

def insert_verifier_fls_wrapper(verifier_c_filepath):

    # inject new fls64___ and fls___ functions at an appropriate location
    inputfile_handle = verifier_c_filepath.open('r')
    input_file_lines = inputfile_handle.readlines()
    tmpdir_path = pathlib.Path("/tmp")
    tmpfile_1_name = datetime.now().strftime('tmp_tnum_%H_%M_%d_%m_%Y.c')
    tmpfile_1_path = tmpdir_path.joinpath(tmpfile_1_name)
    tmpfile_1_handle = tmpfile_1_path.open('w')
    # replace call to fls64 with call to fls64___
    for line in input_file_lines:
        if r"fls64" in line:
            tmpfile_1_handle.write(line.replace(r" fls64(", r" fls64___("))
        elif r"fls" in line:
            tmpfile_1_handle.write(line.replace(r" fls(", r" fls___("))
        else:
            tmpfile_1_handle.write(line)
    inputfile_handle.close()
    tmpfile_1_handle.close()

    # inject the custom fls___ and fls64___ wrappers to verifier.c
    # after the all the #includes
    tmpfile_1_handle = tmpfile_1_path.open('r')
    tmpfile_1_lines = tmpfile_1_handle.readlines()
    tmpfile_2_name = datetime.now().strftime('tmp_tnum_2_%H_%M_%d_%m_%Y.c')
    tmpfile_2_path = tmpdir_path.joinpath(tmpfile_2_name)
    tmpfile_2_handle = tmpfile_2_path.open('w')
    for line in tmpfile_1_lines:
        tmpfile_2_handle.write(line)
        if r'#include "disasm.h"' in line:
            tmpfile_2_handle.write(wrapper_fls)

    tmpfile_1_handle.close()
    tmpfile_2_handle.close()

    shutil.copy(tmpfile_2_path, verifier_c_filepath)


def insert_tnum_fls_wrapper(tnum_c_filepath):

    # replace call to fls and fls64 with calls to custom fls___ and 
    # fls64___
    inputfile_handle = tnum_c_filepath.open('r')
    input_file_lines = inputfile_handle.readlines()
    tmpdir_path = pathlib.Path("/tmp")
    tmpfile_1_name = datetime.now().strftime('tmp_tnum_%H_%M_%d_%m_%Y.c')
    tmpfile_1_path = tmpdir_path.joinpath(tmpfile_1_name)
    tmpfile_1_handle = tmpfile_1_path.open('w')
    for line in input_file_lines:
        if r"fls64" in line:
            tmpfile_1_handle.write(line.replace(r" fls64(", r" fls64___("))
        elif r"fls" in line:
            tmpfile_1_handle.write(line.replace(r" fls(", r" fls___("))
        else:
            tmpfile_1_handle.write(line)
    inputfile_handle.close()
    tmpfile_1_handle.close()

    # inject the custom fls___ and fls64___ functions at an appropriate 
    # location
    tmpfile_1_handle = tmpfile_1_path.open('r')
    tmpfile_1_lines = tmpfile_1_handle.readlines()
    tmpfile_2_name = datetime.now().strftime('tmp_tnum_2_%H_%M_%d_%m_%Y.c')
    tmpfile_2_path = tmpdir_path.joinpath(tmpfile_2_name)
    tmpfile_2_handle = tmpfile_2_path.open('w')
    for line in tmpfile_1_lines:
        tmpfile_2_handle.write(line)
        if r'#include <linux/tnum.h>' in line:
            tmpfile_2_handle.write(wrapper_fls)

    tmpfile_1_handle.close()
    tmpfile_2_handle.close()

    shutil.copy(tmpfile_2_path, tnum_c_filepath)

def mark_reg_known_memset_remove(verifier_c_filepath):
    inputfile_handle = verifier_c_filepath.open('r')
    input_file_lines = inputfile_handle.readlines()
    tmpdir_path = pathlib.Path("/tmp")
    tmpfile_name = datetime.now().strftime('tmp_verifier_%H_%M_%d_%m_%Y.c')
    tmpfile_path = tmpdir_path.joinpath(tmpfile_name)
    tmpfile_handle = tmpfile_path.open('w')
    func_start_found = False
    memset_removal_done = False
    input_file_line_iter = iter(input_file_lines)
    for line in input_file_line_iter:
        if not memset_removal_done:
            if r"void __mark_reg_known(" in line:
                func_start_found = True
            if func_start_found and "memset" in line:
                num_parens_open = line.count("(")
                num_parens_close = line.count(")")
                while (num_parens_open != num_parens_close):
                    next_line = next(input_file_line_iter)
                    num_parens_open += next_line.count("(")
                    num_parens_close += next_line.count(")")
                memset_removal_done = True
                continue
            tmpfile_handle.write(line)
        else:
            tmpfile_handle.write(line)

    tmpfile_handle.close()
    inputfile_handle.close()

    shutil.copy(tmpfile_path, verifier_c_filepath)


def mark_reg_unknown_imprecise_memset_remove(verifier_c_filepath):
    inputfile_handle = verifier_c_filepath.open('r')
    input_file_lines = inputfile_handle.readlines()
    tmpdir_path = pathlib.Path("/tmp")
    tmpfile_name = datetime.now().strftime('tmp_verifier_%H_%M_%d_%m_%Y.c')
    tmpfile_path = tmpdir_path.joinpath(tmpfile_name)
    tmpfile_handle = tmpfile_path.open('w')
    func_start_found = False
    memset_removal_done = False
    input_file_line_iter = iter(input_file_lines)
    for line in input_file_line_iter:
        if not memset_removal_done:
            if r"void __mark_reg_unknown_imprecise(struct bpf_reg_state" in line:
                func_start_found = True
            if func_start_found and "memset" in line:
                num_parens_open = line.count("(")
                num_parens_close = line.count(")")
                while (num_parens_open != num_parens_close):
                    next_line = next(input_file_line_iter)
                    num_parens_open += next_line.count("(")
                    num_parens_close += next_line.count(")")
                memset_removal_done = True
                continue
            tmpfile_handle.write(line)
        else:
            tmpfile_handle.write(line)

    tmpfile_handle.close()
    inputfile_handle.close()

    shutil.copy(tmpfile_path, verifier_c_filepath)
    return memset_removal_done


def mark_reg_unknown_memset_remove(verifier_c_filepath):
    inputfile_handle = verifier_c_filepath.open('r')
    input_file_lines = inputfile_handle.readlines()
    tmpdir_path = pathlib.Path("/tmp")
    tmpfile_name = datetime.now().strftime('tmp_verifier_%H_%M_%d_%m_%Y.c')
    tmpfile_path = tmpdir_path.joinpath(tmpfile_name)
    tmpfile_handle = tmpfile_path.open('w')
    func_start_found = False
    memset_removal_done = False
    input_file_line_iter = iter(input_file_lines)
    for i, line in enumerate(input_file_line_iter):
        if not memset_removal_done:
            if r"static void __mark_reg_unknown(" in line:
                # this is just a function declaration, continue.
                if ";" in line:
                    tmpfile_handle.write(line)
                    continue
                next_line = next(input_file_line_iter)
                line += next_line
                # this is just a function declaration, continue.
                if ";" in next_line:
                    tmpfile_handle.write(line)
                    continue
                next_next_line = next(input_file_line_iter)
                line += next_next_line
                # this is the actual function definition.
                if "{" in next_line or "{" in next_next_line:
                    func_start_found = True
            if func_start_found and "memset" in line:
                num_parens_open = line.count("(")
                num_parens_close = line.count(")")
                while (num_parens_open != num_parens_close):
                    next_line = next(input_file_line_iter)
                    num_parens_open += next_line.count("(")
                    num_parens_close += next_line.count(")")
                memset_removal_done = True
                continue
            tmpfile_handle.write(line)
        else:
            tmpfile_handle.write(line)

    tmpfile_handle.close()
    inputfile_handle.close()

    shutil.copy(tmpfile_path, verifier_c_filepath)


def reg_bounds_sync_calls_remove(verifier_c_filepath):
    inputfile_handle = verifier_c_filepath.open("r")
    input_file_lines = inputfile_handle.readlines()
    tmpdir_path = pathlib.Path("/tmp")
    tmpfile_name = datetime.now().strftime("tmp_verifier_%H_%M_%d_%m_%Y.c")
    tmpfile_path = tmpdir_path.joinpath(tmpfile_name)
    tmpfile_handle = tmpfile_path.open("w")
    input_file_line_iter = iter(input_file_lines)
    for i, line in enumerate(input_file_line_iter):
        if r"reg_bounds_sync" in line:
            if not r"static void reg_bounds_sync" in line:
                line = r"//" + line

        tmpfile_handle.write(line)

    tmpfile_handle.close()
    inputfile_handle.close()

    shutil.copy(tmpfile_path, verifier_c_filepath)


def reg_bounds_sanity_check_calls_remove(verifier_c_filepath):
    inputfile_handle = verifier_c_filepath.open("r")
    input_file_lines = inputfile_handle.readlines()
    tmpdir_path = pathlib.Path("/tmp")
    tmpfile_name = datetime.now().strftime("tmp_verifier_%H_%M_%d_%m_%Y.c")
    tmpfile_path = tmpdir_path.joinpath(tmpfile_name)
    tmpfile_handle = tmpfile_path.open("w")
    input_file_line_iter = iter(input_file_lines)
    for i, line in enumerate(input_file_line_iter):
        if r"reg_bounds_sanity_check" in line:
            if r"static int reg_bounds_sanity_check" in line:
                line = line
            elif "return" in line:
                line = "return 0;\n"
            else:
                line = r"//" + line
        tmpfile_handle.write(line)

    tmpfile_handle.close()
    inputfile_handle.close()

    shutil.copy(tmpfile_path, verifier_c_filepath)


def reg_bounds_sync_add(verifier_c_filepath):
    inputfile_handle = verifier_c_filepath.open("r")
    input_file_lines = inputfile_handle.readlines()
    tmpdir_path = pathlib.Path("/tmp")
    tmpfile_name = datetime.now().strftime("tmp_verifier_%S_%H_%M_%d_%m_%Y.c")
    tmpfile_path = tmpdir_path.joinpath(tmpfile_name)
    print(tmpfile_path)
    tmpfile_handle = tmpfile_path.open("w")
    func_start_found = False
    sync_add_done = False
    input_file_line_iter = iter(input_file_lines)
    for i, line in enumerate(input_file_line_iter):
        if not sync_add_done:
            if not func_start_found:
                if r"static void reg_bounds_sync(struct bpf_reg_state *reg)" in line:
                    func_start_found = True
                    # line containing just "{"
                    next_line = next(input_file_line_iter)
                    line += next_line
            else:
                if r"}" in line:
                    sync_add_done = True
                else:
                    line = line.replace("//", "")

        tmpfile_handle.write(line)

    tmpfile_handle.close()
    inputfile_handle.close()

    shutil.copy(tmpfile_path, verifier_c_filepath)


def print_and_log(s, pend="\n"):
    logfile.write(">>> " + s + "\n")
    logfile_err.write(">>> " + s + "\n")
    print(colored(s, "green"), flush=True, end=pend)


################################################################################
# main
################################################################################
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--llvmdir", help="llvm install directory", type=str,
                        required=False, default="/usr/")
    parser.add_argument("--kernver", help="kernel version, used to perpare verifier.c using appropriate wrappers (see wrappers.py)", type=str,
                        required=True)
    parser.add_argument("--kernbasedir", help="kernel base directory", type=str,
                        required=True)
    parser.add_argument("--outdir", help="output directory", type=str,
                        required=True)
    parser.add_argument("--specific-op", dest='specific_op',
                        help='single specific BPF op to encode',
                        choices = [op.op_name for op in bpf_ops],
                        type=str, required=False)
    parser.add_argument("--bv-suffix-override", dest='bv_suffix_override',
                        help='use a different bitvector suffix than the default, i.e. use default + 1000',
                        action=argparse.BooleanOptionalAction,
                        required=False)
    parser.add_argument("--commit",
                        help="specific kernel commit, instead of a kernel version",
                        type=str, required=False, default="-")
    parser.add_argument("--modular",
                        help="generate encodings of BPF ops without reg_bonds_sync logic (necessary to perform modular verifcation, which is faster)",
                        action=argparse.BooleanOptionalAction,
                        )

    args = parser.parse_args()

    llvm_to_smt_dir_fullpath = pathlib.Path(__file__).parent.resolve()
    assert llvm_to_smt_dir_fullpath.exists()

    llvmdir_fullpath = pathlib.Path(args.llvmdir).resolve()
    assert llvmdir_fullpath.exists()

    scriptsdir_fullpath = llvm_to_smt_dir_fullpath.joinpath("llvm-passes")
    assert scriptsdir_fullpath.exists()

    outdir_fullpath = pathlib.Path(args.outdir).resolve()
    assert outdir_fullpath.exists()

    kerndir_fullpath = pathlib.Path(args.kernbasedir).resolve()
    assert kerndir_fullpath.exists()

    if version.parse(args.kernver) < version.parse("4.14.214"):
        raise RuntimeError(
            'Unsupported kernel version. Only >= 4.14.214 supported.')

    if args.specific_op is not None:
        for op in bpf_ops:
            if op.op_name != args.specific_op:
                op.skip = True

    print(", ".join([op.op_name for op in bpf_ops if op.skip == False]))

    if args.modular:
        if version.parse(args.kernver) < version.parse("5.19-rc6"):
            raise RuntimeError('Modular mode requires kernels >= 5.19-rc6 with reg_bounds_sync.')
        if (version.parse(args.kernver) < version.parse("6.10-rc1") and
            (args.specific_op is None or args.specific_op in broken_ops_modular)):
            raise RuntimeError('Modular mode requires kernels >= 6.10-rc1 for some of the targeted ops.')

    if args.bv_suffix_override:
        if args.specific_op is None:
            raise RuntimeError(
            '--bv-suffix-override can only be used with --specific-op')
        for op in bpf_ops:
            if op.op_name == args.specific_op:
                op.suffix_id = op.suffix_id + 1000

    ####################
    #  setup logging   #
    ####################
    logdir_fullpath = outdir_fullpath
    datetime_str = datetime.now().strftime('%H_%M_%d_%m_%Y')

    logfile_name = datetime.now().strftime('log_{}.log'.format(datetime_str))
    logfile_path = pathlib.Path.joinpath(logdir_fullpath, logfile_name)
    logfile_path.touch()
    logfile = logfile_path.open("w")
    logfile_err_name = datetime.now().strftime('log_err_{}.log'.format(datetime_str))
    logfile_err_path = pathlib.Path.joinpath(logdir_fullpath, logfile_err_name)
    logfile_err_path.touch()
    logfile_err = logfile_err_path.open("w")
    print_and_log("Log file: {}".format(logfile_path))
    print_and_log("Log error file: {}".format(logfile_err_path))

    logfile.flush()
    logfile_err.flush()

    ##############################
    # change to kernel directory #
    ##############################
    print_and_log("Enterning kernel directory".format(str(kerndir_fullpath)))
    old_curdir = os.getcwd()
    os.chdir("{}".format(str(kerndir_fullpath)))
    newdir = os.getcwd()
    print_and_log(" ... done")

    logfile.flush()
    logfile_err.flush()

    ###################
    # checkout kernel #
    ###################
    print_and_log("Checkout kernel version v{}".format(args.kernver))
    if args.commit == "-":
        cmd_checkout = ['git', 'checkout', '-f', 'v{}'.format(args.kernver)]
    else:
        cmd_checkout = ['git', 'checkout', '-f', '{}'.format(args.commit)]
    print(" ".join(cmd_checkout))
    subprocess.run(cmd_checkout, stdout=logfile, stderr=logfile_err,
                   check=True, text=True, bufsize=1)
    print_and_log(" ... done")

    logfile.flush()
    logfile_err.flush()

    ##################################
    # make config, and add BPF flags #
    ##################################
    print_and_log("Run make config and edit BPF flags")
    cmd_make_clean = ['make', 'clean']
    print(" ".join(cmd_make_clean))
    subprocess.run(cmd_make_clean, stdout=logfile,
                   stderr=logfile_err, check=True, text=True, bufsize=1)
    cmd_make_defconfig = ['make', 'defconfig']
    print(" ".join(cmd_make_defconfig))
    subprocess.run(cmd_make_defconfig, stdout=logfile,
                   stderr=logfile_err, check=True, text=True, bufsize=1)
    config_path = pathlib.Path(".config")
    config_text = config_path.read_text()
    config_text = config_text.replace(
        "# CONFIG_BPF is not set", "CONFIG_BPF=y")
    config_text = config_text.replace("# CONFIG_BPF_SYSCALL is not set",
                                      "CONFIG_BPF_SYSCALL=y")
    config_path.write_text(config_text)
    print_and_log(" ... done")

    logfile.flush()
    logfile_err.flush()

    ############################
    # get kernel compile flags #
    ############################
    print_and_log("Extract compile flags for current kernel version")
    clang_fullpath = llvmdir_fullpath.joinpath("bin", "clang")
    cmd_make_olddefconfig = ['make', 'CC={}'.format(
        str(clang_fullpath)), 'olddefconfig']
    print(" ".join(cmd_make_olddefconfig))
    cmdout_make_config = subprocess.run(cmd_make_olddefconfig,
                                        stdout=logfile, stderr=logfile_err, text=True, bufsize=1, check=True)

    # attempt to build verifier.o
    cmd_make_verifier = ['make', 'CC={}'.format(
        str(clang_fullpath)), 'V=1', 'KCFLAGS="-Wno-error"', 'kernel/bpf/verifier.o']
    print(" ".join(cmd_make_verifier))
    cmdout_make_verifier = subprocess.run(
        cmd_make_verifier, stdout=subprocess.PIPE, stderr=logfile_err, text=True, bufsize=1, check=True)
    print(cmdout_make_verifier.stdout)
    logfile.write("cmdout_verifier:\n")
    logfile.write(cmdout_make_verifier.stdout)
    logfile.write("\n")

    additional_clang_options = r''' -fno-discard-value-names -emit-llvm -S -O0 -Xclang -no-opaque-pointers -Xclang -disable-O0-optnone'''

    # search for verifier.o clang compile command
    verifier_re_search_pattern = r'([\s]*)(.*,kernel\/bpf\/\.verifier\.o\.d.*)(-c -o.*)'
    regex_res_verifier = re.search(
        verifier_re_search_pattern, cmdout_make_verifier.stdout)
    res_str_verifier = regex_res_verifier.group(2)
    res_str_verifier = res_str_verifier.replace("-Werror ", "")
    res_str_verifier += additional_clang_options + \
        r" kernel/bpf/verifier.c -o " + \
        str(outdir_fullpath.joinpath("verifier.ll"))
    logfile.write("res_str_verifier: \n {}\n".format(res_str_verifier))

    # attempt to build tnum.o
    cmd_make_tnum = ['make', 'CC={}'.format(
        str(clang_fullpath)), 'V=1', 'kernel/bpf/tnum.o']
    cmdout_make_tnum = subprocess.run(
        cmd_make_tnum, stdout=subprocess.PIPE, stderr=logfile_err, text=True, bufsize=1, check=True)
    logfile.write("cmdout_tnum:\n")
    logfile.write(cmdout_make_tnum.stdout)
    logfile.write("\n")

    # search for tnum.o clang compile command
    tnum_re_search_pattern = r'([\s]*)(.*,kernel\/bpf\/\.tnum\.o\.d.*)(-c -o.*)'
    regex_res_tnum = re.search(tnum_re_search_pattern, cmdout_make_tnum.stdout)
    res_str_tnum = regex_res_tnum.group(2)
    res_str_tnum = res_str_tnum.replace("-Werror ", "")
    res_str_tnum += additional_clang_options + \
        r" kernel/bpf/tnum.c -o " + str(outdir_fullpath.joinpath("tnum.ll"))
    logfile.write("res_str_tnum: \n {}\n".format(res_str_tnum))
    print_and_log(" ... done")

    logfile.flush()
    logfile_err.flush()

    ################################
    # Edit verifier.c and tnum.c#
    ################################
    print_and_log("Edit tnum.c and verifier.c to add wrappers")
    tnum_file_path = kerndir_fullpath.joinpath("kernel", "bpf", "tnum.c")
    insert_tnum_fls_wrapper(tnum_file_path)
    verifier_file_path = kerndir_fullpath.joinpath(
        "kernel", "bpf", "verifier.c")
    insert_verifier_fls_wrapper(verifier_file_path)
    insert_wrapper_unknown(verifier_file_path)
    mark_reg_known_memset_remove(verifier_file_path)
    if not mark_reg_unknown_imprecise_memset_remove(verifier_file_path):
        mark_reg_unknown_memset_remove(verifier_file_path)
    insert_alu_wrapper(verifier_file_path)
    insert_jmp_wrapper(verifier_file_path, args.kernver)
    if args.modular:
        reg_bounds_sync_calls_remove(verifier_file_path)
        reg_bounds_sanity_check_calls_remove(verifier_file_path)
    insert_sync_wrapper(verifier_file_path, args.kernver)
    print_and_log(" ... done")

    logfile.flush()
    logfile_err.flush()

    ################################
    # Compile verifier.c and tnum.c#
    ################################
    print_and_log("Compile verifier.c and tnum.c")
    subprocess.run(res_str_verifier,  shell=True, stdout=logfile,
                   stderr=logfile_err, check=True, text=True, bufsize=1)
    subprocess.run(res_str_tnum,  shell=True, stdout=logfile,
                   stderr=logfile_err, check=True, text=True, bufsize=1)
    # delete_all_files_in_dir(args.outdir)
    print_and_log(" ... done")

    logfile.flush()
    logfile_err.flush()

    ############################################
    # Link verifier.ll and tnum.ll to verifier_tnum.ll #
    ############################################
    print_and_log(
        "Link verifier.ll and tnum.ll to single verifier_tnum.ll")
    os.chdir(str(outdir_fullpath))

    llvm_link_fullpath = llvmdir_fullpath.joinpath("bin", "llvm-link")
    cmd_link = [str(llvm_link_fullpath), '-S', 'tnum.ll', '-opaque-pointers=0',
                'verifier.ll', '-o', 'verifier_tnum.ll']
    print(" ".join(cmd_link))
    cmdout_link = subprocess.run(
        cmd_link, stdout=logfile, stderr=logfile_err, text=True, bufsize=1, check=True)

    print_and_log(" ... done")
    os.chdir(old_curdir)

    logfile.flush()
    logfile_err.flush()

    ########################################
    # Prepare .config file for llvm-to-smt #
    ########################################
    print_and_log("Prepare .config file for llvm-to-smt")
    config_fullpath = scriptsdir_fullpath.joinpath(".config")
    with open(config_fullpath, "w") as config_file:
        config_file.write("LLVM_DIR=\"%s\"\n" % llvmdir_fullpath)
        config_file.write("BASE_DIR=\"%s\"\n" % scriptsdir_fullpath)
    print_and_log(" ... done")

    # ###################################
    # # Run llvm passes and llvm-to-smt #
    # ###################################

    input_llfile_fullpath = outdir_fullpath.joinpath("verifier_tnum.ll")
    error_ops = []

    for op in bpf_ops:
        if op.skip == True:
            continue
        print(colored("Getting encoding for {}".format(op.op_name), 'green'), flush=True)
        llvmpassrunner_for_op = LLVMPassRunner(
                scriptsdir_fullpath=scriptsdir_fullpath,
                llvmdir_fullpath=llvmdir_fullpath,
                inputdir_fullpath=outdir_fullpath,
                op=op.op_name,
                input_llfile_fullpath=input_llfile_fullpath,
                function_name=op.function_name,
                output_smtfile_name="{}.smt2".format(op.op_name),
                global_bv_suffix=str(op.suffix_id),
                logfile_name = logfile_name,
                logfile_err_name = logfile_err_name)
        try:
            llvmpassrunner_for_op.run()
        except subprocess.CalledProcessError as e:
            error_ops.append(op.op_name)
            continue
        del llvmpassrunner_for_op
        print(colored(" ... done", 'green'))

    logfile.flush()
    logfile_err.flush()
    logfile.close()
    logfile_err.close()

    if len(error_ops) > 0:
        print(colored("Finished generating encodings. There are errors with the following BPF ops: {}.".format(
            ", ".join(error_ops)), "yellow"))
        exit(1)
    else:
        print(colored("Finished generating all encodings successfully{}".format(
            " (modular)." if args.modular else "."), "green"))
