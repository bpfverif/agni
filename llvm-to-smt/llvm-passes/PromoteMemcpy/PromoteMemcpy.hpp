#ifndef LLVM2SMT_PROMOTE_MEMCPY_H
#define LLVM2SMT_PROMOTE_MEMCPY_H

#include <llvm/Analysis/AssumptionCache.h>
#include <llvm/IR/Dominators.h>
#include <llvm/IR/PassManager.h>
#include <llvm/IR/IntrinsicInst.h>
#include "llvm/Passes/PassBuilder.h"
#include "llvm/Passes/PassPlugin.h"
#include "llvm/Support/raw_ostream.h"
#include <llvm/IR/Dominators.h>
#include <llvm/IR/IRBuilder.h>
#include <llvm/Transforms/Utils/Local.h>

// New PM implementation

struct PromoteMemcpy : llvm::PassInfoMixin<PromoteMemcpy> {
  // Main entry point, takes IR unit to run the pass on (&F) and the
  // corresponding pass manager (to be queried if need be)
  llvm::PreservedAnalyses run(llvm::Function &F,
                              llvm::FunctionAnalysisManager &FAM) {
    bool Changed = runOnFunction(F, FAM);
    return (Changed ? llvm::PreservedAnalyses::none()
                    : llvm::PreservedAnalyses::all());
  }

  // Without isRequired returning true, this pass will be skipped for functions
  // decorated with the optnone LLVM attribute. Note that clang -O0 decorates
  // all functions with optnone.
  static bool isRequired() { return true; }
  bool runOnFunction(llvm::Function &F, llvm::FunctionAnalysisManager &FAM);

private:
  llvm::Module *m_M = nullptr;
  llvm::LLVMContext *m_Ctx = nullptr;
  const llvm::DataLayout *m_DL = nullptr;
  llvm::DominatorTree *m_DT = nullptr;
  llvm::AssumptionCache *m_AC = nullptr;

  bool simplifyMemCpy(llvm::MemCpyInst *MCpy);
};
#endif // LLVM2SMT_PROMOTE_MEMCPY_H
