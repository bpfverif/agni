#include "ModuleEncoder.hpp"

/* Initialize singleton instance */
ModuleEncoder *ModuleEncoder::instance = 0;

ModuleEncoder *ModuleEncoder::getInstance() {
  if (!ModuleEncoder::instance)
    ModuleEncoder::instance = new ModuleEncoder;
  return ModuleEncoder::instance;
}

void ModuleEncoder::init(Module &M, ModuleAnalysisManager &MAM) {
  ModuleEncoder::instance->module = &M;
  ModuleEncoder::instance->moduleAnalysisManager = &MAM;
  ModuleEncoder::instance->functionAnalysisManager =
      &MAM.getResult<FunctionAnalysisManagerModuleProxy>(M).getManager();
  ModuleEncoder::instance->dataLayout = new DataLayout(&M);
}

ModuleAnalysisManager *ModuleEncoder::getModuleAnalysisManager() {
  return moduleAnalysisManager;
}

DataLayout *ModuleEncoder::getDataLayout() { return dataLayout; }

Module *ModuleEncoder::getModule() { return module; }

MemorySSA &ModuleEncoder::getMemorySSA(Function &F) {
  auto FAM = ModuleEncoder::instance->functionAnalysisManager;
  MemorySSA &MSSA = FAM->getResult<MemorySSAAnalysis>(F).getMSSA();
  return MSSA;
}