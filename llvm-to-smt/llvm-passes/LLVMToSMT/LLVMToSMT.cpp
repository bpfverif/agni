#include "LLVMToSMT.h"

/* -----------------------------------------------------------------------------
 * The LLVMToSMT pass implementation, an analysis pass which builds the SMT
 * formula corresponding to a function
 * -------------------------------------------------------------------------- */
LLVMToSMT::Result LLVMToSMT::run(Module &M, ModuleAnalysisManager &MAM) {

  /* TODO find a better way to pass command line arguments to the pass */
  char *bvSuffix = std::getenv("GLOBAL_BITVECTOR_SUFFIX");
  if (!bvSuffix) {
    throw std::invalid_argument("No function specified. Please set the "
                                "FUNCTION_UNDER_EVAL environment variable "
                                "before running the LLVMToSMT Pass.\n");
  }
  BitVecHelper::init(std::string(bvSuffix));

  /* MemorySSA analysis is only done at the FunctionAnalysis level.
   * FunctionAnalysisManagerModuleProxy is a proxy for FunctionAnalysisManager.
   * Use it to get the MemorySSA for the function. */
  ModuleEncoder *moduleEncoderInstance = moduleEncoderInstance->getInstance();
  moduleEncoderInstance->init(M, MAM);

  char *functionUnderEvalStr = std::getenv("FUNCTION_UNDER_EVAL");
  if (!functionUnderEvalStr) {
    throw std::invalid_argument("No function specified. Please set the "
                                "FUNCTION_UNDER_EVAL environment variable "
                                "before running the LLVMToSMT Pass.\n");
  }

  Function *functionUnderEval = M.getFunction(StringRef(functionUnderEvalStr));
  if (!functionUnderEval) {
    throw std::invalid_argument(
        "Function not found: " + std::string(functionUnderEvalStr) + "\n");
  }
  MemorySSA &MSSA = moduleEncoderInstance->getMemorySSA(*functionUnderEval);

  /* Create new FunctionEncoder instance for FUNCTION_UNDER_EVAL and build
  the SMT for the function */
  FunctionEncoder *functionEncoder =
      new FunctionEncoder(functionUnderEval, &MSSA);
  functionEncoder->buildSMT();
  return *functionEncoder;
}

/* -----------------------------------------------------------------------------
 * Printer pass implementation, which prints the SMT built from the LLVMToSMT
 * pass
 * -------------------------------------------------------------------------- */
void LLVMToSMTPrinter::printFormulaToFile(FunctionEncoder &functionEncoder) {
  outs()
      << "<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>\n"
      << "Saving encoding to .smt2 file...\n"
      << "<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>\n";

  char *smt2OutputFilepath = std::getenv("SMT2LIB_OUTPUT_FILEPATH");
  if (!smt2OutputFilepath) {
    throw std::invalid_argument(
        "Output file path for .smt2 encoding not given. Please set the "
        "SMT2LIB_OUTPUT_FILEPATH environment variable before running the "
        "pass.\n");
  }

  Z3_set_ast_print_mode(ctx, Z3_PRINT_SMTLIB_FULL);

  outs() << "\nOutput .smt2 file path: " << smt2OutputFilepath << "\n";

  /* Final SMT formula is the conjunction of all clauses in the
   * functionEncoder's functionEncodingZ3ExprVec. Add formula to solver to print
   * it in SMT format. */
  z3::expr_vector &formulaVec = functionEncoder.functionEncodingZ3ExprVec;
  z3::expr finalSMT = z3::mk_and(formulaVec);
  z3::solver z3SolverInstance = z3::solver(ctx);
  z3SolverInstance.add(finalSMT);
  std::ofstream smt2FileOutStream(smt2OutputFilepath);
  smt2FileOutStream << z3SolverInstance << "\n";

  /* Now add as comments, the input and output Json dictionaries */
  Json::FastWriter fastJsonWriter;
  std::string inputJsonDictStr =
      fastJsonWriter.write(*functionEncoder.inputJsonDict);
  std::string outputJsonDictStr =
      fastJsonWriter.write(*functionEncoder.outputJsonDict);
  smt2FileOutStream << ";";
  smt2FileOutStream << inputJsonDictStr;
  smt2FileOutStream << ";";
  smt2FileOutStream << outputJsonDictStr;
}

PreservedAnalyses LLVMToSMTPrinter::run(Module &M, ModuleAnalysisManager &MAM) {
  auto functionEncoder = MAM.getResult<LLVMToSMT>(M);
  LLVMToSMTPrinter::printFormulaToFile(functionEncoder);
  return PreservedAnalyses::all();
}

/* -----------------------------------------------------------------------------
 * PassManager Registration
 * -------------------------------------------------------------------------- */
AnalysisKey LLVMToSMT::Key;

PassPluginLibraryInfo getLLVMToSMTPassPluginInfo() {
  return {LLVM_PLUGIN_API_VERSION, "llvm-to-smt", LLVM_VERSION_STRING,
          [](PassBuilder &PB) {
            // #1. Register for opt --passes=print<llvmtosmt>
            PB.registerPipelineParsingCallback(
                [&](StringRef Name, ModulePassManager &MPM,
                    ArrayRef<PassBuilder::PipelineElement>) {
                  if (Name == "print<llvm-to-smt>") {
                    MPM.addPass(LLVMToSMTPrinter(errs()));
                    return true;
                  }
                  return false;
                });
            // #2: Register FAM.getResult<LLVMToSMT>(Function)
            PB.registerAnalysisRegistrationCallback(
                [](ModuleAnalysisManager &MAM) {
                  MAM.registerPass([&] { return LLVMToSMT(); });
                });
          }};
};

extern "C" LLVM_ATTRIBUTE_WEAK ::PassPluginLibraryInfo llvmGetPassPluginInfo() {
  return getLLVMToSMTPassPluginInfo();
}
