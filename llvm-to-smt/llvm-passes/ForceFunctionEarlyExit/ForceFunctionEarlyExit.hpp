#ifndef LLVM2SMT_FORCE_FUNCTIONS_EARLY_EXIT_H
#define LLVM2SMT_FORCE_FUNCTIONS_EARLY_EXIT_H

#include <llvm/ADT/PostOrderIterator.h>
#include <llvm/Analysis/CallGraph.h>
#include <llvm/IR/Instructions.h>
#include <llvm/Passes/PassBuilder.h>
#include <llvm/Passes/PassPlugin.h>
#include <llvm/ADT/ArrayRef.h>
#include <llvm/ADT/StringRef.h>
#include <llvm/IR/Attributes.h>
#include <llvm/IR/IRBuilder.h>
#include <llvm/IR/Instruction.h>
#include <llvm/IR/LLVMContext.h>
#include <llvm/IR/Type.h>
#include <llvm/IR/Value.h>

#include <stdexcept>
#include <utility>
#include <unordered_map>
#include <fstream>
#include <iostream>

#include <jsoncpp/json/json.h>


struct ForceFunctionEarlyExit
    : public llvm::PassInfoMixin<ForceFunctionEarlyExit> {
  llvm::PreservedAnalyses run(llvm::Module &M, llvm::ModuleAnalysisManager &);
  bool runOnModule(llvm::Module &M);

  std::unordered_set<std::string> listOfFunctions;
  std::vector<llvm::Function *> functionsToRemoveCallsInstsFrom;
  void initFunctionsToRemove();
  void initfunctionsToRemoveCallsInstsFrom(llvm::Module &M);
  std::unordered_map<llvm::Function *, int> functionEarlyExitMap;

  void initFunctionEarlyExitMap(char *filePath, llvm::Module &M);
  bool replaceRetInst(llvm::Function &F, llvm::LLVMContext &CTX, int retval);
};

#endif // LLVM2SMT_FORCE_FUNCTIONS_EARLY_EXIT_H
