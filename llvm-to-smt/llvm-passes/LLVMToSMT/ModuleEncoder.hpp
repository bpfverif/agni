#ifndef LLVM2SMT_MODULEENCODER_H
#define LLVM2SMT_MODULEENCODER_H

#include <llvm/Analysis/MemorySSA.h>
#include <unordered_map>
#include <z3++.h>

using namespace llvm;

struct ModuleEncoder {
private:
  static ModuleEncoder *instance; /* singleton instance */
  Module *module;
  ModuleAnalysisManager *moduleAnalysisManager;
  FunctionAnalysisManager *functionAnalysisManager;
  DataLayout *dataLayout;
  ModuleEncoder(){}; /* disallow creating instance of this class */

public:
  static ModuleEncoder *getInstance();
  void init(Module &M, ModuleAnalysisManager &MAM);
  ModuleAnalysisManager *getModuleAnalysisManager();
  MemorySSA &getMemorySSA(Function &F);
  Module *getModule();
  DataLayout *getDataLayout();
};

#endif // LLVM2SMT_MODULEENCODER_H