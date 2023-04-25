#ifndef LLVM_TO_SMT_H
#define LLVM_TO_SMT_H

#include <fstream>
#include <llvm/IR/Function.h>
#include <vector>

#include <llvm/Passes/PassBuilder.h>
#include <llvm/Passes/PassPlugin.h>

#include "BitvecHelper.hpp"
#include "FunctionEncoder.hpp"
#include "ModuleEncoder.hpp"

using namespace llvm;

using ResultLLVMToSMT = FunctionEncoder;

struct LLVMToSMT : public llvm::AnalysisInfoMixin<LLVMToSMT> {
  using Result = ResultLLVMToSMT;

  Result run(llvm::Module &M, llvm::ModuleAnalysisManager &);
  // Result runOnModule(llvm::Module &M, llvm::ModuleAnalysisManager &);
  static bool isRequired() { return true; }

private:
  /* A special type used by analysis passes to provide an address that
   * identifies that particular analysis pass type. */
  static llvm::AnalysisKey Key;
  friend struct llvm::AnalysisInfoMixin<LLVMToSMT>;
};

class LLVMToSMTPrinter : public llvm::PassInfoMixin<LLVMToSMTPrinter> {
public:
  explicit LLVMToSMTPrinter(llvm::raw_ostream &OutS) : OS(OutS) {}
  llvm::PreservedAnalyses run(llvm::Module &M,
                              llvm::ModuleAnalysisManager &MAM);
  static bool isRequired() { return true; }

private:
  void printFormulaToFile(FunctionEncoder &functionEncoder);
  llvm::raw_ostream &OS;
};

#endif // LLVM_TO_SMT_H
