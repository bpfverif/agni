#include "RemoveFunctionCalls.hpp"

using namespace llvm;

#define DEBUG_TYPE "remove-func-calls"

//-----------------------------------------------------------------------------
// InlineFunctionCalls implementation
//-----------------------------------------------------------------------------

void RemoveFunctionCalls::initFunctionsToRemove() {

  char *functionToRemoveTxtStr = std::getenv("FUNCTIONS_TO_REMOVE_TXT");
  if (!functionToRemoveTxtStr) {
    throw std::invalid_argument(
        "No file specified. Please set the "
        "FUNCTIONS_TO_REMOVE_TXT environment variable.\n");
  }

  std::ifstream ifs(functionToRemoveTxtStr);
  Json::Reader reader;
  Json::Value obj;
  reader.parse(ifs, obj);
  const Json::Value &map = obj["functions_to_remove"];
  outs() << "Number of functions:" << map.size() << "\n";
  for (int i = 0; i < map.size(); i++) {
    std::string funcName = map[i].asString();
    outs() << funcName << "\n";
    RemoveFunctionCalls::listOfFunctions.insert(funcName);
  }

#if 0
  std::ifstream inFileStream;
  inFileStream.open(functionToRemoveTxtStr);

  if (!inFileStream) {
    throw std::invalid_argument(
        "File not found: " + std::string(functionToRemoveTxtStr) + "\n");
  }

  std::string line;
  outs() << "Attempting to remove function calls to: \n";
  while (std::getline(inFileStream, line)) {
    outs() << llvm::StringRef(line) << "\n";
    listOfFunctions.insert(line);
  }
#endif
}

void RemoveFunctionCalls::initfunctionsToRemoveCallsInstsFrom(llvm::Module &M) {

  CallGraph callGraph = CallGraph(M);
  char *functionToRemoveCallsFromStr;
  Function *functionToStartRemovingCallInstsFrom;
  CallGraphNode *callGraphNode;

  functionToRemoveCallsFromStr = std::getenv("FUNCTION_TO_START_REMOVE");
  if (!functionToRemoveCallsFromStr) {
    throw std::invalid_argument(
        "No function specified. Please set the "
        "FUNCTION_TO_START_REMOVE environment variable.\n");
  }

  functionToStartRemovingCallInstsFrom =
      M.getFunction(llvm::StringRef(functionToRemoveCallsFromStr));
  if (!functionToStartRemovingCallInstsFrom) {
    throw std::invalid_argument("Function not found\n");
  }

  assert(functionToStartRemovingCallInstsFrom);
  outs() << "[initfunctionsToRemoveCallsInstsFrom] "
         << "functionToStartRemovingCallInstsFrom: "
         << functionToStartRemovingCallInstsFrom->getName() << "\n";

  callGraphNode = callGraph[functionToStartRemovingCallInstsFrom];
  outs() << "[initfunctionsToRemoveCallsInstsFrom] "
         << "callGraphNode: " << callGraphNode << "\n";

  callGraphNode->print(outs());

  for (auto IT = po_begin(callGraphNode), EI = po_end(callGraphNode); IT != EI;
       IT++) {
    Function *F = IT->getFunction();
    if (F) {
      functionsToRemoveCallsInstsFrom.push_back(F);
    }
  }
}

PreservedAnalyses RemoveFunctionCalls::run(llvm::Module &M,
                                           llvm::ModuleAnalysisManager &MAM) {
  bool Changed = false;
  initFunctionsToRemove();
  initfunctionsToRemoveCallsInstsFrom(M);

  for (auto &F : functionsToRemoveCallsInstsFrom) {
    for (auto &BB : *F) {
      for (auto Inst = BB.begin(), IE = BB.end(); Inst != IE;) {
        CallInst *callInst = dyn_cast<CallInst>(Inst);
        if (!callInst) {
          ++Inst;
          continue;
        }
        auto calledFunc = callInst->getCalledFunction();
        if (!calledFunc || !calledFunc->hasName()) {
          ++Inst;
          continue;
        }
        std::string calledFuncStr = calledFunc->getName().str();
        bool instIsToBeRemoved =
            listOfFunctions.find(calledFuncStr) != listOfFunctions.end();
        if (instIsToBeRemoved) {
          outs() << "Removing callInst in Function: " << F->getName() << ":\n";
          callInst->print(outs());
          Inst = callInst->eraseFromParent();
        } else {
          ++Inst;
        }
      }
    }
  }

  Changed = true;
  return (Changed ? llvm::PreservedAnalyses::none()
                  : llvm::PreservedAnalyses::all());
}

//-----------------------------------------------------------------------------
// New PM Registration
//-----------------------------------------------------------------------------
llvm::PassPluginLibraryInfo getInlineFunctionCallsPluginInfo() {
  return {LLVM_PLUGIN_API_VERSION, "remove-func-calls", LLVM_VERSION_STRING,
          [](PassBuilder &PB) {
            PB.registerPipelineParsingCallback(
                [](StringRef Name, ModulePassManager &MPM,
                   ArrayRef<PassBuilder::PipelineElement>) {
                  if (Name == "remove-func-calls") {
                    MPM.addPass(RemoveFunctionCalls());
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
