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

bpf_sync_op = [
    "BPF_SYNC"
]

def insert_sync_wrapper(verifier_c_filepath, kernver):
    wrapper_sync = ''
    if version.parse(kernver) >= version.parse("5.19"):
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
    if version.parse(kernver) >= version.parse("6.4-rc1"):
        # Starting with v6.4-rc1~77^2~118^2~26^2~1.
        wrapper_jmp = wrapper_jmp_6
        wrapper_jmp32 = wrapper32_jmp_6
    elif version.parse(kernver) >= version.parse("5.7-rc1"):
        # Starting with v5.7-rc1~146^2~10^2~1^2~5.
        wrapper_jmp = wrapper_jmp_5
        wrapper_jmp32 = wrapper32_jmp_5
    elif version.parse(kernver) >= version.parse("5.3-rc1"):
        # Starting with v5.3-rc1~140^2~179^2^2~6.
        wrapper_jmp = wrapper_jmp_4
        wrapper_jmp32 = wrapper32_jmp_4
    elif version.parse(kernver) >= version.parse("5.1-rc1"):
        # Starting with v5.1-rc1~178^2~404^2~4^2~13.
        wrapper_jmp = wrapper_jmp_3
        wrapper_jmp32 = wrapper32_jmp_3
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

    s = ""
    for op in bpf_jmp_ops:
        s += wrapper_jmp.format(op, op)

    # no 32-bit jumps before 5.1-rc1
    if version.parse(kernver) >= version.parse("5.1-rc1"):
        for op in bpf_jmp_ops:
            s += wrapper_jmp32.format(op, op)

    return s


def insert_jmp_wrapper(verifier_c_filepath, kernver):
    all_jmp_wrappers_concat = get_all_jmp_wrappers_concatenated(kernver)
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
    s = ""
    for op in bpf_alu_ops:
        s += wrapper_alu.format(op, op)
        s += wrapper_alu32.format(op, op)
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


def insert_tnum_wrapper(tnum_c_filepath):

    # inject new fls64___ and fls___ functions at an appropriate location
    string_to_search = r"const struct tnum tnum_unknown = { .value = 0, .mask = -1 };"
    inputfile_handle = tnum_c_filepath.open('r')
    input_file_lines = inputfile_handle.readlines()
    tmpdir_path = pathlib.Path("/tmp")
    tmpfile_1_name = datetime.now().strftime('tmp_tnum_%H_%M_%d_%m_%Y.c')
    tmpfile_1_path = tmpdir_path.joinpath(tmpfile_1_name)
    tmpfile_1_handle = tmpfile_1_path.open('w')
    for line in input_file_lines:
        tmpfile_1_handle.write(line)
        if string_to_search in line:
            tmpfile_1_handle.write(wrapper_tnum_fls)
    inputfile_handle.close()
    tmpfile_1_handle.close()

    # replace call to fls64 with call to fls64___
    tmpfile_1_handle = tmpfile_1_path.open('r')
    tmpfile_1_lines = tmpfile_1_handle.readlines()
    tmpfile_2_name = datetime.now().strftime('tmp_tnum_2_%H_%M_%d_%m_%Y.c')
    tmpfile_2_path = tmpdir_path.joinpath(tmpfile_2_name)
    tmpfile_2_handle = tmpfile_2_path.open('w')
    for line in tmpfile_1_lines:
        if r"u8 bits = fls64(chi);" in line:
            tmpfile_2_handle.write(line.replace(
                r"u8 bits = fls64(chi);", r"u8 bits = fls64___(chi);"))
        else:
            tmpfile_2_handle.write(line)

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
                line = r'//' + line
                num_parens_open = line.count("(")
                num_parens_close = line.count(")")
                while (num_parens_open != num_parens_close):
                    next_line = next(input_file_line_iter)
                    num_parens_open += next_line.count("(")
                    num_parens_close += next_line.count(")")
                    line += r'//' + next_line
                memset_removal_done = True
            tmpfile_handle.write(line)
        else:
            tmpfile_handle.write(line)

    tmpfile_handle.close()
    inputfile_handle.close()

    shutil.copy(tmpfile_path, verifier_c_filepath)


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
            if r"static void __mark_reg_unknown(const struct bpf_verifier_env *env," in line:
                next_line = next(input_file_line_iter)
                line += next_line
                next_next_line = next(input_file_line_iter)
                line += next_next_line
                if "struct bpf_reg_state *reg)" in next_line and "{" in next_next_line:
                    func_start_found = True
            if func_start_found and "memset" in line:
                line = r'//' + line
                num_parens_open = line.count("(")
                num_parens_close = line.count(")")
                while (num_parens_open != num_parens_close):
                    next_line = next(input_file_line_iter)
                    num_parens_open += next_line.count("(")
                    num_parens_close += next_line.count(")")
                    line += r'//' + next_line
                memset_removal_done = True
            tmpfile_handle.write(line)
        else:
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
    parser.add_argument("--kernver", help="kernel version", type=str,
                        required=True)
    parser.add_argument("--kernbasedir", help="kernel base directory", type=str,
                        required=False, default="/home/linux-stable")
    parser.add_argument("--outdir", help="output directory", type=str,
                        required=True)
    parser.add_argument("--scriptsdir", help="scripts directory from llvm-to-smt",
                        type=str, required=False, default="/home/cav23-artifact/llvm-to-smt/llvm-passes")
    parser.add_argument("--specific-op", dest='specific_op',
                        help='single specific BPF op to encode',
                        choices= bpf_alu_ops + bpf_jmp_ops,
                        type=str, required=False)

    args = parser.parse_args()

    llvmdir_fullpath = pathlib.Path(args.llvmdir).resolve()

    scriptsdir_fullpath = pathlib.Path(args.scriptsdir).resolve()
    assert scriptsdir_fullpath.exists()

    if version.parse(args.kernver) < version.parse("4.14.214"):
        raise RuntimeError(
            'Unsupported kernel version. Only >= 4.14.214 supported.')

    if args.specific_op is not None:
        if args.specific_op in bpf_alu_ops:
            bpf_alu_ops = [args.specific_op]
            bpf_jmp_ops = []
            bpf_sync_op = []
        elif args.specific_op in bpf_jmp_ops:
            bpf_jmp_ops = [args.specific_op]
            bpf_alu_ops = []
            bpf_sync_op = []
        else:
            raise RuntimeError(
                'Unsupported BPF op {}'.format(args.specific_op))

    outdir_fullpath = pathlib.Path(args.outdir).resolve()
    assert outdir_fullpath.exists()

    ####################
    #  setup logging   #
    ####################
    logdir_fullpath = outdir_fullpath

    logfile_name = datetime.now().strftime('log_%H_%M_%d_%m_%Y.log')
    logfile_path = pathlib.Path.joinpath(logdir_fullpath, logfile_name)
    logfile_path.touch()
    logfile = logfile_path.open("w")
    logfile_err_name = datetime.now().strftime('log_err_%H_%M_%d_%m_%Y.log')
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
    kerndir_fullpath = pathlib.Path(args.kernbasedir).resolve()
    print_and_log("Change to kernel directory: {}".format(
        str(kerndir_fullpath)), pend="")
    assert kerndir_fullpath.exists()
    old_curdir = os.getcwd()
    os.chdir("{}".format(str(kerndir_fullpath)))
    newdir = os.getcwd()
    print_and_log(" ... done")

    logfile.flush()
    logfile_err.flush()

    ###################
    # checkout kernel #
    ###################
    print_and_log("Checkout kernel version v{}".format(args.kernver), pend="")
    cmd_checkout = ['git', 'checkout', '-f', 'v{}'.format(args.kernver)]
    subprocess.run(cmd_checkout, stdout=logfile, stderr=logfile_err,
                   check=True, text=True, bufsize=1)
    print_and_log(" ... done")

    logfile.flush()
    logfile_err.flush()

    ##################################
    # make config, and add BPF flags #
    ##################################
    print_and_log("Run make config and edit BPF flags", pend="")
    subprocess.run(['make', 'clean'], stdout=logfile,
                   stderr=logfile_err, check=True, text=True, bufsize=1)
    subprocess.run(['make', 'defconfig'], stdout=logfile,
                   stderr=logfile_err, check=True, text=True, bufsize=1)
    path = pathlib.Path(".config")
    text = path.read_text()
    text = text.replace("# CONFIG_BPF is not set", "CONFIG_BPF=y")
    text = text.replace("# CONFIG_BPF_SYSCALL is not set",
                        "CONFIG_BPF_SYSCALL=y")
    path.write_text(text)
    print_and_log(" ... done")

    logfile.flush()
    logfile_err.flush()

    ############################
    # get kernel compile flags #
    ############################
    print_and_log("Extract compile flags for current kernel version", pend="")
    clang_fullpath = llvmdir_fullpath.joinpath("bin", "clang")
    logfile.write("clang_fullpath: {}\n".format(str(clang_fullpath)))

    cmdout_make_config = subprocess.run(['make', 'CC={}'.format(str(clang_fullpath)), 'olddefconfig'],
                                        stdout=logfile, stderr=logfile_err, text=True, bufsize=1, check=True)

    # cmdout_make_verifier = subprocess.check_output(
    #     ['make', 'CC={}'.format(str(clang_fullpath)), 'V=1', 'kernel/bpf/verifier.o'], text=True, bufsize=1)
    cmd_make_verifier = ['make', 'CC={}'.format(
        str(clang_fullpath)), 'V=1', 'kernel/bpf/verifier.o']
    cmdout_make_verifier = subprocess.run(
        cmd_make_verifier, stdout=subprocess.PIPE, stderr=logfile_err, text=True, bufsize=1, check=True)
    logfile.write("cmdout_verifier:\n")
    logfile.write(cmdout_make_verifier.stdout)
    logfile.write("\n")

    additional_clang_options = r''' -fno-discard-value-names -emit-llvm -S -O0 -Xclang -disable-O0-optnone'''

    verifier_re_search_pattern = r'([\s]*)(.*,kernel\/bpf\/\.verifier\.o\.d.*)(-c -o.*)'
    regex_res_verifier = re.search(
        verifier_re_search_pattern, cmdout_make_verifier.stdout)
    res_str_verifier = regex_res_verifier.group(2)
    res_str_verifier = res_str_verifier.replace("-Werror ", "")
    res_str_verifier += additional_clang_options + \
        r" kernel/bpf/verifier.c -o " + \
        str(outdir_fullpath.joinpath("verifier.ll"))
    logfile.write("res_str_verifier: \n {}\n".format(res_str_verifier))

    cmd_make_tnum = ['make', 'CC={}'.format(
        str(clang_fullpath)), 'V=1', 'kernel/bpf/tnum.o']
    cmdout_make_tnum = subprocess.run(
        cmd_make_tnum, stdout=subprocess.PIPE, stderr=logfile_err, text=True, bufsize=1, check=True)
    logfile.write("cmdout_tnum:\n")
    logfile.write(cmdout_make_tnum.stdout)
    logfile.write("\n")

    tnum_re_search_pattern = '([\s]*)(.*,kernel\/bpf\/\.tnum\.o\.d.*)(-c -o.*)'
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
    print_and_log("Edit tnum.c and verifier.c to add wrappers", pend="")
    tnum_file_path = kerndir_fullpath.joinpath("kernel", "bpf", "tnum.c")
    insert_tnum_wrapper(tnum_file_path)
    verifier_file_path = kerndir_fullpath.joinpath(
        "kernel", "bpf", "verifier.c")
    insert_wrapper_unknown(verifier_file_path)
    mark_reg_known_memset_remove(verifier_file_path)
    mark_reg_unknown_memset_remove(verifier_file_path)
    insert_alu_wrapper(verifier_file_path)
    insert_jmp_wrapper(verifier_file_path, args.kernver)
    insert_sync_wrapper(verifier_file_path, args.kernver)
    print_and_log(" ... done")

    logfile.flush()
    logfile_err.flush()

    ################################
    # Compile verifier.c and tnum.c#
    ################################
    print_and_log("Compile verifier.c and tnum.c", pend="")
    subprocess.run(res_str_verifier,  shell=True, stdout=logfile,
                   stderr=logfile_err, check=True, text=True, bufsize=1)
    subprocess.run(res_str_tnum,  shell=True, stdout=logfile,
                   stderr=logfile_err, check=True, text=True, bufsize=1)
    # delete_all_files_in_dir(args.outdir)
    print_and_log(" ... done")

    logfile.flush()
    logfile_err.flush()

    ############################################
    # Link verifier.ll and tnum.ll to verifier.ll #
    ############################################
    print_and_log(
        "Link verifier.ll and tnum.ll to single verifier.ll", pend="")
    os.chdir(str(outdir_fullpath))

    llvm_link_fullpath = llvmdir_fullpath.joinpath("bin", "llvm-link")
    cmd_link = [str(llvm_link_fullpath), '-S', 'tnum.ll',
                'verifier.ll', '-o', 'verifier.ll']
    cmdout_link = subprocess.run(
        cmd_link, stdout=logfile, stderr=logfile_err, text=True, bufsize=1, check=True)
    print_and_log(" ... done")
    os.chdir(old_curdir)

    logfile.flush()
    logfile_err.flush()

    # ###################################
    # # Run llvm passes and llvm-to-smt #
    # ###################################

    idx = 0
    input_llfile_fullpath = str(outdir_fullpath.joinpath("verifier.ll"))

    # All ALU_64 ops
    for i, op in enumerate(bpf_alu_ops):
        idx = i
        print(colored("Getting encoding for {}".format(
            op), 'green'), flush=True, end="")
        llvmpassrunner_for_op = LLVMPassRunner(
            logfile=logfile,
            logfile_err=logfile_err,
            scriptsdir_fullpath=scriptsdir_fullpath,
            llvmdir_fullpath=llvmdir_fullpath,
            inputdir_fullpath=outdir_fullpath,
            op=op,
            input_llfile_name="verifier.ll",
            function_name="adjust_scalar_min_max_vals_wrapper_{}".format(op),
            output_smtfile_name="{}.smt2".format(op),
            global_bv_suffix=str(i))
        llvmpassrunner_for_op.run()
        del llvmpassrunner_for_op
        print(colored(" ... done", 'green'))

    # All ALU_32 ops
    for i, op in enumerate(bpf_alu_ops, start=idx+1):
        op32 = op+"_32"
        idx = i
        print(colored("Getting encoding for {}".format(
            op32), 'green'), flush=True, end="")
        llvmpassrunner_for_op = LLVMPassRunner(
            logfile=logfile,
            logfile_err=logfile_err,
            scriptsdir_fullpath=scriptsdir_fullpath,
            llvmdir_fullpath=llvmdir_fullpath,
            inputdir_fullpath=outdir_fullpath,
            op=op32,
            input_llfile_name="verifier.ll",
            function_name="adjust_scalar_min_max_vals_wrapper_32_{}".format(op),
            output_smtfile_name="{}.smt2".format(op32),
            global_bv_suffix=str(i))
        llvmpassrunner_for_op.run()
        del llvmpassrunner_for_op
        print(colored(" ... done", 'green'))

    # All JMP_64 ops
    for i, op in enumerate(bpf_jmp_ops, start=idx+1):
        idx = i
        print(colored("Getting encoding for {}".format(
            op), 'green'), flush=True, end="")
        llvmpassrunner_for_op = LLVMPassRunner(
            logfile=logfile,
            logfile_err=logfile_err,
            scriptsdir_fullpath=scriptsdir_fullpath,
            llvmdir_fullpath=llvmdir_fullpath,
            inputdir_fullpath=outdir_fullpath,
            op=op,
            input_llfile_name="verifier.ll",
            function_name="check_cond_jmp_op_wrapper_{}".format(op),
            output_smtfile_name="{}.smt2".format(op),
            global_bv_suffix=str(i))
        llvmpassrunner_for_op.run()
        del llvmpassrunner_for_op
        print(colored(" ... done", 'green'))

    # All JMP_32 ops
    # Note: no 32-bit jumps until 5.1-rc1        
    if (version.parse(args.kernver) >= version.parse("5.1-rc1")):
        for i, op in enumerate(bpf_jmp_ops, start=idx+1):
            idx = i
            op32 = op+"_32"
            print(colored("Getting encoding for {}".format(
                op32), 'green'), flush=True, end="")
            llvmpassrunner_for_op = LLVMPassRunner(
                logfile=logfile,
                logfile_err=logfile_err,
                scriptsdir_fullpath=scriptsdir_fullpath,
                llvmdir_fullpath=llvmdir_fullpath,
                inputdir_fullpath=outdir_fullpath,
                op=op32,
                input_llfile_name="verifier.ll",
                function_name="check_cond_jmp_op_wrapper_32_{}".format(op),
                output_smtfile_name="{}.smt2".format(op32),
                global_bv_suffix=str(i))
            llvmpassrunner_for_op.run()
            del llvmpassrunner_for_op
            print(colored(" ... done", 'green'))

    # SYNC
    for i, op in enumerate(bpf_sync_op, start=idx+1):
        idx = i
        print(colored("Getting encoding for {}".format(
            op), 'green'), flush=True, end="")
        llvmpassrunner_for_op = LLVMPassRunner(
            logfile=logfile,
            logfile_err=logfile_err,
            scriptsdir_fullpath=scriptsdir_fullpath,
            llvmdir_fullpath=llvmdir_fullpath,
            inputdir_fullpath=outdir_fullpath,
            op=op,
            input_llfile_name="verifier.ll",
            function_name="sync___",
            output_smtfile_name="{}.smt2".format(op),
            global_bv_suffix=str(i))
        llvmpassrunner_for_op.run()
        del llvmpassrunner_for_op
        print(colored(" ... done", 'green'))

    logfile.flush()
    logfile_err.flush()
    logfile.close()
    logfile_err.close()
