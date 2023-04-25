import subprocess
import sys


class LLVMPassRunner:

    def __init__(self, logfile, logfile_err, scriptsdir_fullpath,
                 llvmdir_fullpath,
                 inputdir_fullpath, op, input_llfile_name, 
                 function_name, output_smtfile_name,
                 global_bv_suffix):
        self.logfile = logfile
        self.logfile_err = logfile_err
        self.scriptsdir_fullpath = scriptsdir_fullpath
        self.llvmdir_fullpath = llvmdir_fullpath
        self.inputdir_fullpath = inputdir_fullpath
        self.op = op
        self.input_llfile_name = input_llfile_name
        self.function_name = function_name
        self.output_smtfile_name = output_smtfile_name
        self.global_bv_suffix = global_bv_suffix

    def run_opt_pass(self, input_llfile_fullpath, output_llfile_fullpath, O1=True):
        llvm_opt_fullpath = self.llvmdir_fullpath.joinpath("bin", "opt")
        cmd_opt_O1 = '''{llvm_opt_fullpath} -O1 --strip-debug --instnamer --stats -S  {input_llfile_fullpath} -o {output_llfile_fullpath}'''
        cmd_opt_O0 = '''{llvm_opt_fullpath} -S --instnamer --simplifycfg --sroa --mergereturn --dce --deadargelim --memoryssa --always-inline --function-attrs --argpromotion --instcombine {input_llfile_fullpath} -o {output_llfile_fullpath}'''
        if O1 == True:
            cmd_opt = cmd_opt_O1.format(
                llvm_opt_fullpath=llvm_opt_fullpath,
                input_llfile_fullpath=input_llfile_fullpath,
                output_llfile_fullpath=output_llfile_fullpath
            )
            self.logfile.write("Running opt -O1\n")
            self.logfile.write(cmd_opt)
            self.logfile.write("\n")
        else:
            cmd_opt = cmd_opt_O0.format(
                llvm_opt_fullpath=llvm_opt_fullpath,
                input_llfile_fullpath=input_llfile_fullpath,
                output_llfile_fullpath=output_llfile_fullpath

            )
            self.logfile.write("Running opt -O0\n")
            self.logfile.write(cmd_opt)
            self.logfile.write("\n")
        subprocess.run(cmd_opt, shell=True, check=True, text=True,
                       stdout=self.logfile, stderr=self.logfile_err, bufsize=1)
        self.logfile.write("\nFinished running opt\n")

    def run_force_function_early_exit_pass(self, input_llfile_fullpath, outdir_fullpath, output_llfile_name):
        cmd_force_functions_early_exit = '''{force_functions_early_exit_pass_runner_sh} {path_to_llvm_file} {output_dir} {output_filename_ll}'''
        force_functions_early_exit_pass_fullpath = self.scriptsdir_fullpath.joinpath(
            "force_functions_early_exit.sh")
        cmd_force_functions_early_exit_op = cmd_force_functions_early_exit.format(
            force_functions_early_exit_pass_runner_sh=force_functions_early_exit_pass_fullpath,
            path_to_llvm_file=input_llfile_fullpath,
            output_dir=outdir_fullpath,
            output_filename_ll=output_llfile_name
        )
        self.logfile.write("Running force_function_early_exit_pass\n")
        self.logfile.write(cmd_force_functions_early_exit_op)
        self.logfile.write("\n")
        subprocess.run(cmd_force_functions_early_exit_op, shell=True, check=True,
                       text=True, stdout=self.logfile, stderr=self.logfile_err, bufsize=1)
        self.logfile.write("\nFinished force_function_early_exit_pass\n")

    def run_remove_functions_calls_pass(self, input_llfile_fullpath, function_name, outdir_fullpath, output_llfile_name):
        remove_func_calls_pass_fullpath = self.scriptsdir_fullpath.joinpath(
            "remove_func_calls.sh")
        cmd_remove_func_calls = '''{remove_func_calls_pass_runner_sh} {path_to_llvm_file} {function_to_start_remove} {output_dir} {output_filename_ll}'''
        cmd_remove_func_calls_op = cmd_remove_func_calls.format(
            remove_func_calls_pass_runner_sh=remove_func_calls_pass_fullpath,
            path_to_llvm_file=input_llfile_fullpath,
            function_to_start_remove=function_name,
            output_dir=outdir_fullpath,
            output_filename_ll=output_llfile_name
        )
        self.logfile.write("Running remove_functions_calls_pass\n")
        self.logfile.write(cmd_remove_func_calls_op)
        self.logfile.write("\n")
        subprocess.run(cmd_remove_func_calls_op, shell=True, check=True, text=True,
                       stdout=self.logfile, stderr=self.logfile_err, bufsize=1)
        self.logfile.write("\nFinished remove_functions_calls_pass\n")

    def run_inline_verifier_func_pass(self, input_llfile_fullpath, function_name, outdir_fullpath, output_llfile_name):
        inline_verifier_func_pass_fullpath = self.scriptsdir_fullpath.joinpath(
            "inline_verifier_func.sh")
        cmd_inline_verifier_func = '''{inline_verifier_func_pass_runner_sh} {path_to_llvm_file} {function_to_start_inline} {output_dir} {output_filename_ll}'''
        cmd_inline_verifier_func_op = cmd_inline_verifier_func.format(
            inline_verifier_func_pass_runner_sh=inline_verifier_func_pass_fullpath,
            path_to_llvm_file=input_llfile_fullpath,
            function_to_start_inline=function_name,
            output_dir=outdir_fullpath,
            output_filename_ll=output_llfile_name
        )
        self.logfile.write("Running inline_verifier_func_pass\n")
        self.logfile.write(cmd_inline_verifier_func_op)
        self.logfile.write("\n")
        subprocess.run(cmd_inline_verifier_func_op, shell=True, check=True, text=True,
                       stdout=self.logfile, stderr=self.logfile_err, bufsize=1)
        self.logfile.write("\nFinished inline_verifier_func_pass\n")

    def run_promote_memcpy_pass(self, input_llfile_fullpath, function_name, outdir_fullpath, output_llfile_name):
        promote_memcpy_pass_fullpath = self.scriptsdir_fullpath.joinpath(
            "promote_memcpy.sh")
        cmd_promote_memcpy = '''{promote_memcpy_pass_runner_sh} {path_to_llvm_file} {function_to_promote_memcpy} {output_dir} {output_filename_ll}'''
        cmd_promote_memcpy_op = cmd_promote_memcpy.format(
            promote_memcpy_pass_runner_sh=promote_memcpy_pass_fullpath,
            path_to_llvm_file=input_llfile_fullpath,
            function_to_promote_memcpy=function_name,
            output_dir=outdir_fullpath,
            output_filename_ll=output_llfile_name
        )
        self.logfile.write("Running promote_memcpy_pass\n")
        self.logfile.write(cmd_promote_memcpy_op)
        self.logfile.write("\n")
        subprocess.run(cmd_promote_memcpy_op, shell=True, check=True, text=True,
                       stdout=self.logfile, stderr=self.logfile_err, bufsize=1)
        self.logfile.write("\nFinished promote_memcpy_pass\n")

    def run_llvm_to_smt_pass(self, indir_fullpath, input_llfile_name, function_name, global_bv_suffix, output_smtfile_name):
        llvm_to_smt_pass_fullpath = self.scriptsdir_fullpath.joinpath(
            "llvm_to_smt.sh")
        cmd_llvm_to_smt = '''{llvm_to_smt_pass_runner_sh} {indir_fullpath} {input_llfile_name} {function_name} {global_bv_suffix} {output_smtfile_name}'''
        cmd_llvm_to_smt_op = cmd_llvm_to_smt.format(
            llvm_to_smt_pass_runner_sh=llvm_to_smt_pass_fullpath,
            indir_fullpath=indir_fullpath,
            input_llfile_name=input_llfile_name,
            function_name=function_name,
            global_bv_suffix=global_bv_suffix,
            output_smtfile_name=output_smtfile_name
        )
        self.logfile.write("Running llvm_to_smt_pass\n")
        self.logfile.write(cmd_llvm_to_smt_op)
        self.logfile.write("\n")
        subprocess.run(cmd_llvm_to_smt_op, shell=True, check=True, text=True,
                       stdout=self.logfile, stderr=self.logfile_err, bufsize=1)
        self.logfile.write("\nFinished llvm_to_smt_pass\n")

    def run(self):
        input_llfile_fullpath = str(
            self.inputdir_fullpath.joinpath(self.input_llfile_name))
        output_llfile_op_fullpath = self.inputdir_fullpath.joinpath(
            "{}.ll".format(self.op))

        self.run_opt_pass(input_llfile_fullpath, output_llfile_op_fullpath)
        self.run_force_function_early_exit_pass(
            output_llfile_op_fullpath, self.inputdir_fullpath, "{}.ll".format(self.op))
        self.run_opt_pass(output_llfile_op_fullpath, output_llfile_op_fullpath)
        self.run_remove_functions_calls_pass(
            output_llfile_op_fullpath, self.function_name, self.inputdir_fullpath, "{}.ll".format(self.op))
        self.run_opt_pass(output_llfile_op_fullpath, output_llfile_op_fullpath)
        self.run_inline_verifier_func_pass(
            output_llfile_op_fullpath, self.function_name, self.inputdir_fullpath, "{}.ll".format(self.op))
        self.run_opt_pass(output_llfile_op_fullpath, output_llfile_op_fullpath)
        self.run_promote_memcpy_pass(output_llfile_op_fullpath,
                                     self.function_name, self.inputdir_fullpath, "{}.ll".format(self.op))
        self.run_opt_pass(output_llfile_op_fullpath,
                          output_llfile_op_fullpath, O1=False)
        self.run_llvm_to_smt_pass(self.inputdir_fullpath, "{}.ll".format(
            self.op), self.function_name, self.global_bv_suffix, "{}.smt2".format(self.op))
