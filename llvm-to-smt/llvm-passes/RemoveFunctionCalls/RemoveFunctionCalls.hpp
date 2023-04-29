#ifndef LLVM2SMT_REMOVE_VOID_FUNCTION_CALLS_H
#define LLVM2SMT_REMOVE_VOID_FUNCTION_CALLS_H

#include <fstream>
#include <llvm/ADT/PostOrderIterator.h>
#include <llvm/Analysis/CallGraph.h>
#include <llvm/IR/Instructions.h>
#include <llvm/Passes/PassBuilder.h>
#include <llvm/Passes/PassPlugin.h>
#include <unordered_set>

#include <jsoncpp/json/json.h>

struct RemoveFunctionCalls
    : public llvm::PassInfoMixin<RemoveFunctionCalls> {
  llvm::PreservedAnalyses run(llvm::Module &M, llvm::ModuleAnalysisManager &);
  bool runOnModule(llvm::Module &M);

  std::unordered_set<std::string> listOfFunctions;
  std::vector<llvm::Function *> functionsToRemoveCallsInstsFrom;
  void initFunctionsToRemove();
  void initfunctionsToRemoveCallsInstsFrom(llvm::Module &M);
};

#endif //LLVM2SMT_REMOVE_VOID_FUNCTION_CALLS_H
