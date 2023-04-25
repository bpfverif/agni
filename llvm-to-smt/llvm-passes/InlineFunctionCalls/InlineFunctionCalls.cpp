#include "InlineFunctionCalls.hpp"

#include "llvm/IR/IRBuilder.h"
#include "llvm/Passes/PassBuilder.h"
#include "llvm/Passes/PassPlugin.h"
#include <fstream>
#include <llvm/ADT/ArrayRef.h>
#include <llvm/ADT/PostOrderIterator.h>
#include <llvm/ADT/SCCIterator.h>
#include <llvm/ADT/SmallVector.h>
#include <llvm/ADT/StringExtras.h>
#include <llvm/ADT/StringRef.h>
#include <llvm/Analysis/CallGraph.h>
#include <llvm/Analysis/CallGraphSCCPass.h>
#include <llvm/IR/Function.h>
#include <llvm/IR/Instruction.h>
#include <llvm/IR/Instructions.h>
#include <llvm/Pass.h>
#include <llvm/Support/FileSystem.h>
#include <llvm/Transforms/IPO/Inliner.h>
#include <llvm/Transforms/Utils/Cloning.h>
#include <queue>
#include <vector>

using namespace llvm;

#define DEBUG_TYPE "inline-func-calls"

//-----------------------------------------------------------------------------
// InlineFunctionCalls implementation
//-----------------------------------------------------------------------------
PreservedAnalyses InlineFunctionCalls::run(llvm::Module &M,
                                           llvm::ModuleAnalysisManager &MAM) {
  bool Changed = false;
  CallGraph callGraph = CallGraph(M);

  char *functionToInlineStr = std::getenv("FUNCTION_TO_INLINE");
  if (!functionToInlineStr) {
    throw std::invalid_argument("No function specified. Please set the "
                                "FUNCTION_TO_INLINE environment variable.\n");
  }

  Function *functionToInline =
      M.getFunction(llvm::StringRef(functionToInlineStr));
  if (!functionToInline) {
    throw std::invalid_argument("Function not found\n");
  }

  std::vector<Function *> functionsToInline;

  CallGraphNode *callGraphNode =
      callGraph.getOrInsertFunction(functionToInline);
  callGraphNode->print(outs());

  for (auto IT = po_begin(callGraphNode), EI = po_end(callGraphNode); IT != EI;
       IT++) {
    Function *F = IT->getFunction();
    if (F) {
      functionsToInline.push_back(F);
    }
  }

  outs() << "---------------------------\n";
  outs() << "Functions to Inline:\n";
  for (Function *F : functionsToInline) {
    outs() << F->getName() << "\n";
  }
  outs() << "---------------------------\n";

  for (Function *F : functionsToInline) {
    outs() << "********\n";
    outs() << F->getName() << "\n";
    outs() << "********\n";

    // TODO worklist pattern from DCE implementation
    // TODO post on llvm forum about correctness
    for (auto &BB : *F) {
      // Replacing instructions requires iterators, hence a for-range loop
      // wouldn't be suitable.
      for (auto Inst = BB.begin(), IE = BB.end(); Inst != IE; ++Inst) {
        auto *callInst = dyn_cast<CallInst>(Inst);
        if (!callInst)
          continue;
        outs() << *callInst << "\n";
        InlineFunctionInfo ifi;
        auto res = llvm::InlineFunction(*callInst, ifi);
        outs() << res.isSuccess() << "\n";
        if (res.isSuccess()) {
          Inst = BB.begin();
          IE = BB.end();
          Changed = true;
        }
      }
    }

    std::string inlinedFuncOutputFile =
        std::string(functionToInlineStr) + ".dump.ll";

    raw_ostream *outfileStream = &outs();
    std::error_code EC;
    outfileStream =
        new raw_fd_ostream(inlinedFuncOutputFile, EC, sys::fs::F_None);
    functionToInline->print(*outfileStream);
  }

  return (Changed ? llvm::PreservedAnalyses::none()
                  : llvm::PreservedAnalyses::all());
}

//-----------------------------------------------------------------------------
// New PM Registration
//-----------------------------------------------------------------------------
llvm::PassPluginLibraryInfo getInlineFunctionCallsPluginInfo() {
  return {LLVM_PLUGIN_API_VERSION, "inline-func-calls", LLVM_VERSION_STRING,
          [](PassBuilder &PB) {
            PB.registerPipelineParsingCallback(
                [](StringRef Name, ModulePassManager &MPM,
                   ArrayRef<PassBuilder::PipelineElement>) {
                  if (Name == "inline-func-calls") {
                    MPM.addPass(InlineFunctionCalls());
                    return true;
                  }
                  return false;
                });
          }};
}

extern "C" LLVM_ATTRIBUTE_WEAK ::llvm::PassPluginLibraryInfo
llvmGetPassPluginInfo() {
  return getInlineFunctionCallsPluginInfo();
}
