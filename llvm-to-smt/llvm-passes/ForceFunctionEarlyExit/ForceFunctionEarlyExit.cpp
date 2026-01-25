#include "ForceFunctionEarlyExit.hpp"

#define DEBUG_TYPE "force-function-early-exit"
using namespace llvm;

void ForceFunctionEarlyExit::initFunctionEarlyExitMap(char *filePath,
                                                      Module &M) {
  std::ifstream ifs(filePath);
  Json::Reader reader;
  Json::Value obj;
  reader.parse(ifs, obj);

  const Json::Value &map = obj["function_returnvalue_map"];
  std::cout << map.size() << std::endl;

  for (int i = 0; i < map.size(); i++) {
    std::string funcName = map[i]["function"].asString();
    Json::Value retValJson = map[i]["return_value"];
    // int retValue = map[i]["return_value"].asInt();
    llvm::Function *func = M.getFunction(funcName);

    if (func) {
      if (retValJson.isNull()) {
        ForceFunctionEarlyExit::functionEarlyExitMap.insert(
            {func, std::nullopt});
      } else if (retValJson.isBool()) {
        ForceFunctionEarlyExit::functionEarlyExitMap.insert(
            {func, retValJson.asBool() ? 1 : 0});
      } else {
        ForceFunctionEarlyExit::functionEarlyExitMap.insert(
            {func, retValJson.asInt()});
      }
    } else {
      outs() << "[initFunctionEarlyExitMap]"
             << "Function not found: " << funcName << "\n";
    }
  }
}

bool ForceFunctionEarlyExit::replaceRetInst(llvm::Function &F,
                                            llvm::LLVMContext &CTX,
                                            std::optional<int> retval) {
  Type *retType = F.getReturnType();

  BasicBlock *newEntryBB =
      BasicBlock::Create(CTX, "early_exit", &F, &F.getEntryBlock());
  ReturnInst *newRetInst = nullptr;

  if (retType->isVoidTy()) {
    assert(!retval.has_value()); // if return value is void, retval from json
                                 // should be "null"
    newRetInst = ReturnInst::Create(CTX, nullptr, newEntryBB);
  } else if (retType->isIntegerTy()) {
    Value *retValObj = ConstantInt::get(retType, retval.value());
    newRetInst = ReturnInst::Create(CTX, retValObj, newEntryBB);
  } else {
    throw std::runtime_error("Unsupported return type \n");
  }

  return true;
}

PreservedAnalyses
ForceFunctionEarlyExit::run(llvm::Module &M, llvm::ModuleAnalysisManager &MAM) {
  bool Changed = false;

  llvm::LLVMContext &CTX = M.getContext();

  char *functionsEarlyRetValueMapStr =
      std::getenv("FUNCTIONS_EARLY_RETVALUE_MAP_TXT");
  if (!functionsEarlyRetValueMapStr) {
    throw std::invalid_argument(
        "No file specified: needs a list of functions and their corresponding "
        "expected early return values in config.json. Please set the "
        "FUNCTIONS_EARLY_RETVALUE_MAP_TXT environment variable.\n");
  }

  initFunctionEarlyExitMap(functionsEarlyRetValueMapStr, M);

  for (auto &pair : ForceFunctionEarlyExit::functionEarlyExitMap) {
    outs() << "--------------------\n";
    llvm::Function *f = pair.first;
    std::optional<int> r = pair.second;
    outs() << "function: " << f->getName() << "\n";
    outs() << "return type: " << r << "\n";
    Changed |= replaceRetInst(*f, CTX, r);
    outs() << "--------------------\n";
  }

  return (Changed ? llvm::PreservedAnalyses::none()
                  : llvm::PreservedAnalyses::all());
}

//-----------------------------------------------------------------------------
// New PM Registration
//-----------------------------------------------------------------------------
llvm::PassPluginLibraryInfo getInlineFunctionCallsPluginInfo() {
  return {LLVM_PLUGIN_API_VERSION, "force-function-early-exit",
          LLVM_VERSION_STRING, [](PassBuilder &PB) {
            PB.registerPipelineParsingCallback(
                [](StringRef Name, ModulePassManager &MPM,
                   ArrayRef<PassBuilder::PipelineElement>) {
                  if (Name == "force-function-early-exit") {
                    MPM.addPass(ForceFunctionEarlyExit());
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
