import subprocess
import sys
import argparse
from shutil import copy2
from pathlib import Path
from datetime import datetime


class LLVMPassRunner:

    def __init__(self, logfile, logfile_err, scriptsdir_fullpath,
                 llvmdir_fullpath,
                 inputdir_fullpath,
                 input_llfile_fullpath,
                 op,
                 function_name, output_smtfile_name,
                 global_bv_suffix):
        self.logfile = logfile
        self.logfile_err = logfile_err
        self.scriptsdir_fullpath = scriptsdir_fullpath
        self.llvmdir_fullpath = llvmdir_fullpath
        self.parentdir_fullpath = inputdir_fullpath
        self.op = op
        self.input_llfile_fullpath = input_llfile_fullpath
        self.curr_llfile_fullpath = self.input_llfile_fullpath
        self.function_name = function_name
        self.output_smtfile_name = output_smtfile_name
        self.global_bv_suffix = global_bv_suffix
        self.op_dir_fullpath = self.parentdir_fullpath.joinpath(
            '{}'.format(self.op))

    def create_op_dir(self):
        self.logfile.write(
            "Creating directory and file for op: {}\n".format(self.op))
        try:
            # TODO, remove try-catch, fail on error
            self.op_dir_fullpath.mkdir()
        except FileExistsError:
            pass
        op_llfile_fullpath = self.op_dir_fullpath.joinpath(
            '{}.ll'.format(self.op))
        print(op_llfile_fullpath)
        copy2(str(self.input_llfile_fullpath), str(op_llfile_fullpath))
        self.curr_llfile_fullpath = op_llfile_fullpath

    def run_opt_pass(self, O1=True):
        llvm_opt_fullpath = self.llvmdir_fullpath.joinpath("bin", "opt")
        cmd_opt_O1 = '''{llvm_opt_fullpath} -Oz --strip-debug --instnamer --stats -S  {input_llfile_fullpath} -o {output_llfile_fullpath}'''
        # cmd_opt_O0 = '''{llvm_opt_fullpath} -S --instnamer --simplifycfg --sroa --mergereturn --dce --deadargelim --memoryssa --always-inline --function-attrs --argpromotion --instcombine {input_llfile_fullpath} -o {output_llfile_fullpath}'''
        cmd_opt_O0 = '''{llvm_opt_fullpath} -S --instnamer --sroa --adce --bdce --dce --globaldce --deadargelim --unreachableblockelim --lowerswitch --function-attrs --argpromotion --instcombine {input_llfile_fullpath} -o {output_llfile_fullpath}'''
        if O1 == True:
            output_llfile_fullpath = self.curr_llfile_fullpath.parent.joinpath(
                self.curr_llfile_fullpath.stem + ".Oz" + ".ll")
            cmd_opt = cmd_opt_O1.format(
                llvm_opt_fullpath=llvm_opt_fullpath,
                input_llfile_fullpath=str(self.curr_llfile_fullpath),
                output_llfile_fullpath=output_llfile_fullpath
            )
            self.logfile.write("Running opt -O1\n")
            self.logfile.write(cmd_opt)
            self.logfile.write("\n")
        else:
            output_llfile_fullpath = self.curr_llfile_fullpath.parent.joinpath(
                self.curr_llfile_fullpath.stem + ".O0" + ".ll")
            cmd_opt = cmd_opt_O0.format(
                llvm_opt_fullpath=llvm_opt_fullpath,
                input_llfile_fullpath=str(self.curr_llfile_fullpath),
                output_llfile_fullpath=output_llfile_fullpath
            )
            self.logfile.write("Running opt -O0\n")
            self.logfile.write(cmd_opt)
            self.logfile.write("\n")
        print(cmd_opt)
        subprocess.run(cmd_opt, shell=True, check=True, text=True,
                       stdout=self.logfile, stderr=self.logfile_err, bufsize=1)
        self.logfile.write("\nFinished running opt\n")
        self.curr_llfile_fullpath = output_llfile_fullpath

    def run_force_function_early_exit_pass(self):
        cmd_force_functions_early_exit = '''{force_functions_early_exit_pass_runner_sh} {path_to_llvm_file} {output_dir} {output_filename_ll}'''
        force_functions_early_exit_pass_fullpath = self.scriptsdir_fullpath.joinpath(
            "force_functions_early_exit.sh")
        output_llfile_fullpath = self.curr_llfile_fullpath.parent.joinpath(
            self.curr_llfile_fullpath.stem + ".ffee" + ".ll")
        cmd_force_functions_early_exit_op = cmd_force_functions_early_exit.format(
            force_functions_early_exit_pass_runner_sh=force_functions_early_exit_pass_fullpath,
            path_to_llvm_file=self.curr_llfile_fullpath,
            output_dir=output_llfile_fullpath.parent,
            output_filename_ll=output_llfile_fullpath.name
        )
        self.logfile.write("Running force_function_early_exit_pass\n")
        self.logfile.write(cmd_force_functions_early_exit_op)
        self.logfile.write("\n")
        print(cmd_force_functions_early_exit_op)
        subprocess.run(cmd_force_functions_early_exit_op, shell=True, check=True,
                       text=True, stdout=self.logfile, stderr=self.logfile_err, bufsize=1)
        self.logfile.write("\nFinished force_function_early_exit_pass\n")
        self.curr_llfile_fullpath = output_llfile_fullpath

    def run_remove_functions_calls_pass(self):
        remove_func_calls_pass_fullpath = self.scriptsdir_fullpath.joinpath(
            "remove_func_calls.sh")
        cmd_remove_func_calls = '''{remove_func_calls_pass_runner_sh} {path_to_llvm_file} {function_to_start_remove} {output_dir} {output_filename_ll}'''
        output_llfile_fullpath = self.curr_llfile_fullpath.parent.joinpath(
            self.curr_llfile_fullpath.stem + ".rfc" + ".ll")
        cmd_remove_func_calls_op = cmd_remove_func_calls.format(
            remove_func_calls_pass_runner_sh=remove_func_calls_pass_fullpath,
            path_to_llvm_file=self.curr_llfile_fullpath,
            function_to_start_remove=self.function_name,
            output_dir=output_llfile_fullpath.parent,
            output_filename_ll=output_llfile_fullpath.name
        )
        self.logfile.write("Running remove_functions_calls_pass\n")
        self.logfile.write(cmd_remove_func_calls_op)
        self.logfile.write("\n")
        print(cmd_remove_func_calls_op)
        subprocess.run(cmd_remove_func_calls_op, shell=True, check=True, text=True,
                       stdout=self.logfile, stderr=self.logfile_err, bufsize=1)
        self.logfile.write("\nFinished remove_functions_calls_pass\n")
        self.curr_llfile_fullpath = output_llfile_fullpath

    def run_lower_funnel_shifts_pass(self):
        lower_funnel_shifts_fullpath = self.scriptsdir_fullpath.joinpath(
            "lower_funnel_shifts.sh")
        cmd_lower_funnel_shifts = '''{lower_funnel_shifts_pass_runner_sh} {path_to_llvm_file} {function_name} {output_dir} {output_filename_ll}'''
        output_llfile_fullpath = self.curr_llfile_fullpath.parent.joinpath(
            self.curr_llfile_fullpath.stem + ".lfsh" + ".ll")
        cmd_lower_funnel_shifts_op = cmd_lower_funnel_shifts.format(
            lower_funnel_shifts_pass_runner_sh=lower_funnel_shifts_fullpath,
            path_to_llvm_file=self.curr_llfile_fullpath,
            function_name=self.function_name,  # TODO, and fix cpp,sh as well.
            output_dir=output_llfile_fullpath.parent,
            output_filename_ll=output_llfile_fullpath.name
        )
        self.logfile.write("Running lower_funnel_shifts_pass\n")
        self.logfile.write(cmd_lower_funnel_shifts_op)
        self.logfile.write("\n")
        print(cmd_lower_funnel_shifts_op)
        subprocess.run(cmd_lower_funnel_shifts_op, shell=True, check=True, text=True,
                       stdout=self.logfile, stderr=self.logfile_err, bufsize=1)
        self.logfile.write("\nFinished lower_funnel_shifts_pass\n")
        self.curr_llfile_fullpath = output_llfile_fullpath

    def run_inline_verifier_func_pass(self):
        inline_verifier_func_pass_fullpath = self.scriptsdir_fullpath.joinpath(
            "inline_verifier_func.sh")
        cmd_inline_verifier_func = '''{inline_verifier_func_pass_runner_sh} {path_to_llvm_file} {function_to_start_inline} {output_dir} {output_filename_ll}'''
        output_llfile_fullpath = self.curr_llfile_fullpath.parent.joinpath(
            self.curr_llfile_fullpath.stem + ".ivf" + ".ll")
        cmd_inline_verifier_func_op = cmd_inline_verifier_func.format(
            inline_verifier_func_pass_runner_sh=inline_verifier_func_pass_fullpath,
            path_to_llvm_file=self.curr_llfile_fullpath,
            function_to_start_inline=self.function_name,
            output_dir=output_llfile_fullpath.parent,
            output_filename_ll=output_llfile_fullpath.name
        )
        self.logfile.write("Running inline_verifier_func_pass\n")
        self.logfile.write(cmd_inline_verifier_func_op)
        self.logfile.write("\n")
        print(cmd_inline_verifier_func_op)
        subprocess.run(cmd_inline_verifier_func_op, shell=True, check=True, text=True,
                       stdout=self.logfile, stderr=self.logfile_err, bufsize=1)
        self.logfile.write("\nFinished inline_verifier_func_pass\n")
        self.curr_llfile_fullpath = output_llfile_fullpath

    def run_promote_memcpy_pass(self):
        promote_memcpy_pass_fullpath = self.scriptsdir_fullpath.joinpath(
            "promote_memcpy.sh")
        cmd_promote_memcpy = '''{promote_memcpy_pass_runner_sh} {path_to_llvm_file} {function_to_promote_memcpy} {output_dir} {output_filename_ll}'''
        output_llfile_fullpath = self.curr_llfile_fullpath.parent.joinpath(
            self.curr_llfile_fullpath.stem + ".pmc" + ".ll")
        cmd_promote_memcpy_op = cmd_promote_memcpy.format(
            promote_memcpy_pass_runner_sh=promote_memcpy_pass_fullpath,
            path_to_llvm_file=self.curr_llfile_fullpath,
            function_to_promote_memcpy=self.function_name,
            output_dir=output_llfile_fullpath.parent,
            output_filename_ll=output_llfile_fullpath.name
        )
        self.logfile.write("Running promote_memcpy_pass\n")
        self.logfile.write(cmd_promote_memcpy_op)
        self.logfile.write("\n")
        print(cmd_promote_memcpy_op)
        subprocess.run(cmd_promote_memcpy_op, shell=True, check=True, text=True,
                       stdout=self.logfile, stderr=self.logfile_err, bufsize=1)
        self.logfile.write("\nFinished promote_memcpy_pass\n")
        self.curr_llfile_fullpath = output_llfile_fullpath

    def run_llvm_to_smt_pass(self):
        llvm_to_smt_pass_fullpath = self.scriptsdir_fullpath.joinpath(
            "llvm_to_smt.sh")
        cmd_llvm_to_smt = '''{llvm_to_smt_pass_runner_sh} {indir_fullpath} {input_llfile_name} {function_name} {global_bv_suffix} {output_smtfile_name}'''
        cmd_llvm_to_smt_op = cmd_llvm_to_smt.format(
            llvm_to_smt_pass_runner_sh=llvm_to_smt_pass_fullpath,
            indir_fullpath=self.curr_llfile_fullpath.parent,
            input_llfile_name=self.curr_llfile_fullpath.name,
            function_name=self.function_name,
            global_bv_suffix=self.global_bv_suffix,
            output_smtfile_name=self.output_smtfile_name
        )
        self.logfile.write("Running llvm_to_smt_pass\n")
        self.logfile.write(cmd_llvm_to_smt_op)
        self.logfile.write("\n")
        print(cmd_llvm_to_smt_op)
        subprocess.run(cmd_llvm_to_smt_op, shell=True, check=True, text=True,
                       stdout=self.logfile, stderr=self.logfile_err, bufsize=1)
        self.logfile.write("\nFinished llvm_to_smt_pass\n")

    def run_llvm_extract(self):
        # extract
        llvm_extract_fullpath = self.llvmdir_fullpath.joinpath(
            "bin", "llvm-extract")
        output_llfile_fullpath = self.curr_llfile_fullpath.parent.joinpath(
            self.curr_llfile_fullpath.stem + ".ex" + ".ll")
        cmd_extract = [str(llvm_extract_fullpath), '--func={}'.format(self.function_name),
                       '-S', str(self.curr_llfile_fullpath), '-o', str(output_llfile_fullpath)]
        self.logfile.write("Running llvm-extract\n")
        self.logfile.write(" ".join(cmd_extract))
        self.logfile.write("\n")
        print(cmd_extract)
        cmdout_extract = subprocess.run(
            cmd_extract, stdout=self.logfile, stderr=self.logfile_err, text=True, bufsize=1, check=True)
        self.logfile.write("\nFinished running llvm-extract\n")
        # self.curr_llfile_fullpath = output_llfile_fullpath

    def run(self):
        self.create_op_dir()
        self.run_opt_pass(O1=True)

        self.run_force_function_early_exit_pass()
        self.run_opt_pass(O1=True)

        self.run_remove_functions_calls_pass()
        self.run_opt_pass(O1=True)
        
        self.run_inline_verifier_func_pass()
        self.run_opt_pass(O1=True)

        self.run_promote_memcpy_pass()
        self.run_opt_pass(O1=False)

        self.run_lower_funnel_shifts_pass()
        self.run_inline_verifier_func_pass()
        
        self.run_opt_pass(O1=False)

        self.run_llvm_extract()
        self.run_llvm_to_smt_pass()
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--llvmdir", help="llvm install directory", type=str,
                        required=True, default="/usr/")
    parser.add_argument("--scriptsdir", help="scripts directory from llvm-to-smt",
                        type=str, required=True)
    parser.add_argument("--outdir", help="directory to use for ll/smt files", type=str,
                        required=True)
    parser.add_argument(
        "--llfile", help="input LLVM file name path", required=True)
    parser.add_argument(
        "--funcname", help="function to encode within", required=True)
    parser.add_argument("--op", help="BPF op", required=True)
    args = parser.parse_args()

    outdir_fullpath = Path(args.outdir).resolve()
    scriptsdir_fullpath = Path(args.scriptsdir).resolve()
    llvmdir_fullpath = Path(args.llvmdir).resolve()
    inputfile_fullpath = Path(args.llfile)

    assert (outdir_fullpath.exists() and scriptsdir_fullpath.exists()
            and llvmdir_fullpath.exists())

    logdir_fullpath = outdir_fullpath

    logfile_name = datetime.now().strftime('log_%H_%M_%d_%m_%Y.log')
    logfile_path = Path.joinpath(logdir_fullpath, logfile_name)
    logfile_path.touch()
    logfile = logfile_path.open("w")
    logfile_err_name = datetime.now().strftime('log_err_%H_%M_%d_%m_%Y.log')
    logfile_err_path = Path.joinpath(logdir_fullpath, logfile_err_name)
    logfile_err_path.touch()
    logfile_err = logfile_err_path.open("w")

    print("Log file: {}".format(logfile_path))
    print("Log error file: {}".format(logfile_err_path))

    llvmpassrunner_for_op = LLVMPassRunner(
        logfile=logfile,
        logfile_err=logfile_err,
        scriptsdir_fullpath=scriptsdir_fullpath,
        llvmdir_fullpath=llvmdir_fullpath,
        inputdir_fullpath=outdir_fullpath,
        input_llfile_fullpath=inputfile_fullpath,
        op=args.op,
        function_name=args.funcname,
        output_smtfile_name="{}.smt2".format(args.op),
        global_bv_suffix="1")

    llvmpassrunner_for_op.run()
