#ifndef LLVM2SMT_INLINE_FUNCTION_CALLS_H
#define LLVM2SMT_INLINE_FUNCTION_CALLS_H

#include "llvm/IR/PassManager.h"
#include "llvm/Pass.h"

struct InlineFunctionCalls : public llvm::PassInfoMixin<InlineFunctionCalls> {
  llvm::PreservedAnalyses run(llvm::Module &M,
                              llvm::ModuleAnalysisManager &);
  bool runOnModule(llvm::Module &M);
};

#endif
