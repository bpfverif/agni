#include "ForceFunctionEarlyExit.hpp"

#define DEBUG_TYPE "force-function-early-exit"
using namespace llvm;

#define VERIFIER_FUNC_SANITIZE_NEEDED "sanitize_needed"
#define VERIFIER_FUNC_SANITIZE_VAL_ALU "sanitize_val_alu"
#define VERIFIER_FUNC_1 "can_skip_alu_sanitation"
#define VERIFIER_FUNC_2 "update_alu_sanitation_state"

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
    int retValue = map[i]["return_value"].asInt();
    llvm::Function *func = M.getFunction(funcName);
    if (func) {
      ForceFunctionEarlyExit::functionEarlyExitMap.insert({func, retValue});
      outs() << "func: " << func->getName() << ", retValue: " << retValue
             << "\n";
    }
  }

#if 0
  std::ifstream inFileStream;
  inFileStream.open(filePath);
  if (!inFileStream) {
    throw std::runtime_error("File not found: " + std::string(filePath) + "\n");
  }
  std::string line;
  while (std::getline(inFileStream, line)) {
    auto delimEnd = line.find(":");
    std::string funcName = line.substr(0, delimEnd);
    auto retValue = std::stoi(line.substr(delimEnd + 1));
    llvm::Function *func = M.getFunction(funcName);
    ForceFunctionEarlyExit::functionEarlyExitMap.insert({func, retValue});
    outs() << "func: " << func->getName() << "\n";
    outs() << "retValue: " << retValue << "\n";
  }
#endif
}

bool ForceFunctionEarlyExit::replaceRetInst(llvm::Function &F,
                                            llvm::LLVMContext &CTX,
                                            int retval) {
  outs() << "Changing return statement in function: " << F << "\n";

  bool Changed = false;
  llvm::ReturnInst *retInst;
  for (llvm::BasicBlock &B : F) {
    for (llvm::Instruction &I : B) {
      if (isa<ReturnInst>(&I)) {
        retInst = dyn_cast<llvm::ReturnInst>(&I);
      }
    }
  }
  outs() << "retInst (old): " << *retInst << "\n";

  Type *retType = F.getReturnType();
  IntegerType *retTypeInt = dyn_cast<llvm::IntegerType>(retType);
  if (!retTypeInt) {
    throw std::runtime_error("Return type is not an integer\n");
  }

  auto retTypeIntBitWidth = retTypeInt->getBitWidth();
  outs() << "retTypeIntBitWidth: " << retTypeIntBitWidth << "\n";

  Value *i32zero = ConstantInt::get(CTX, APInt(retTypeIntBitWidth, retval));
  outs() << "i32zero" << *i32zero << "\n";

  BasicBlock *newEntryBB =
      BasicBlock::Create(CTX, "newentry", &F, &F.getEntryBlock());
  llvm::ReturnInst *newRetInst =
      llvm::ReturnInst::Create(CTX, i32zero, newEntryBB);
  outs() << "newEntryBB" << *newEntryBB << "\n";

#if 0
  retInst->setOperand(0, i32zero);
  outs() << "retInst: (new)" << *retInst << "\n";
  outs() << "Changed function: \n" << F << "\n";
#endif

#if 0
  llvm::BasicBlock &entryBB = F.getEntryBlock();
  llvm::ReturnInst *newRetInst =
      llvm::ReturnInst::Create(CTX, i32zero, &entryBB);

  outs() << "retInst: (new first)" << *newRetInst << "\n";
  outs() << "Changed function: \n" << F << "\n";
#endif

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
        "expected early return values. Please set the "
        "FUNCTIONS_EARLY_RETVALUE_MAP_TXT environment variable.\n");
  }

  initFunctionEarlyExitMap(functionsEarlyRetValueMapStr, M);

  for (auto &pair : ForceFunctionEarlyExit::functionEarlyExitMap) {
    outs() << "--------------------\n";
    llvm::Function *f = pair.first;
    int r = pair.second;
    Changed |= replaceRetInst(*f, CTX, r);
    outs() << "--------------------\n";
  }

#if 0
  llvm::Function *functionSanitizeNeeded =
      M.getFunction(llvm::StringRef(VERIFIER_FUNC_SANITIZE_NEEDED));
  if (!functionSanitizeNeeded) {
    outs() << "Function not found: " << VERIFIER_FUNC_SANITIZE_NEEDED << "\n";
    outs() << "Continuing...\n";
  } else {
    Changed |= replaceRetInst(*functionSanitizeNeeded, CTX, 0);
  }
#endif

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
