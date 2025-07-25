#ifndef LLVM2SMT_FUNCTIONENCODER_H
#define LLVM2SMT_FUNCTIONENCODER_H

#include <llvm/Analysis/MemorySSA.h>
#include <llvm/IR/Argument.h>
#include <llvm/IR/DerivedTypes.h>
#include <llvm/IR/Function.h>
#include <llvm/IR/Instructions.h>
#include <llvm/IR/IntrinsicInst.h>
#include <llvm/IR/Type.h>
#include <llvm/Support/Casting.h>

#include <stdexcept>
#include <string>
#include <unordered_map>
#include <unordered_set>

#include <jsoncpp/json/json.h>
#include <jsoncpp/json/value.h>

#include "BVTree.hpp"
#include "BitvecHelper.hpp"
#include "ModuleEncoder.hpp"

using namespace llvm;

typedef std::pair<BasicBlock *, BasicBlock *> BBPair;
typedef std::unordered_map<Value *, BVTree *> ValueBVTreeMap;
typedef std::pair<Value *, Value *> ValuePair;
typedef std::pair<Value *, std::vector<int> *> ValueIndicesPair;
typedef std::pair<Value *, BasicBlock *> ValueBBPair;

extern z3::context ctx;

enum FunctionEncoderPassType {
  BBAssertionsMapPass = 1,
  PathConditionsMapPass = 2,
  HandlePhiNodesPass = 3,
  HandleReturnInstPass = 4
};

class FunctionEncoder {

public:
  Instruction *currentInstruction;
  BasicBlock *currentBB;
  Function *currentFunction;
  MemorySSA *currentMemorySSA;
  MemoryAccess *mostRecentMemoryDef;
  bool functionReturnsVoid = false;
  z3::expr_vector functionEncodingZ3ExprVec;
  ValueBVTreeMap *inputValueBVTreeMap;
  ValueBVTreeMap *outputValueBVTreeMap;
  Json::Value *inputJsonDict;
  Json::Value *outputJsonDict;

  FunctionEncoder(Function *F, MemorySSA *MSSA)
      : currentFunction(F), currentMemorySSA(MSSA),
        functionEncodingZ3ExprVec(ctx) {
    this->inputValueBVTreeMap = new ValueBVTreeMap();
    this->outputValueBVTreeMap = new ValueBVTreeMap();
  };

  std::unordered_set<Value *> FunctionArgs;

  /* Maps a BasicBlock to a list of Z3 expressions which correspond the encoding
   * of the Instructions in the BasicBlock. Populated in the 1st Pass. */
  std::unordered_map<BasicBlock *, z3::expr_vector> BBAssertionsMap;

  /* Maps a Basic Block to its path condition expression. Populated in the 2nd
   * pass */
  std::unordered_map<BasicBlock *, z3::expr> pathConditionsMap;

  /* To distinguish _which_ path was taken to reach a particular BB from another
   * BB, we need to track path conditions for an edge, i.e. for a <BB, BB> pair.
   * This is necessary to resolve PHI nodes */
  std::unordered_map<BBPair, z3::expr, pair_hash<BasicBlock *, BasicBlock *>>
      EdgeAssertionsMap;

  /* Maps a "view" of Memory, i.e., a MemoryDef i.e., a MemoryAccess to a map of
   * type ValueBVTreeMap. The ValueBVTreeMap maps a Value* to a BVTree (~ vector
   * of bitvectors). We begin with the MemoryDef "liveOnEntry", and its
   * ValueBVTreeMap containing all the functions arguments as keys. eg.
   * liveOnEntry: [arg_a: [bv_a_1, bv_a_2, bv_a_3], arg_b: [bv_b]] */
  std::unordered_map<MemoryAccess *, ValueBVTreeMap> MemoryAccessValueBVTreeMap;
  std::unordered_map<BBPair, z3::expr, pair_hash<BasicBlock *, BasicBlock *>>
      PhiResolutionMap;
  std::unordered_map<BBPair, z3::expr_vector,
                     pair_hash<BasicBlock *, BasicBlock *>>
      MemoryPhiResolutionMap;

  /* A list of structs relevent to the encoding. All other structs are ignored
   * when creating BVTrees. */
  /* TODO move this to a file, and read from file to populate this set */
  std::unordered_set<std::string> relevantStructs{
      "struct.bpf_reg_state",  "struct.bpf_verifier_env",
      "struct.bpf_func_state", "struct.bpf_verifier_state",
      "struct.tnum",           "struct.bpf_insn"};

  /* A map to keep track of what Type a bitcasted value originally came from */
  std::unordered_map<Value *, Type *> BitCastTypeMap;

  /* A map to keep track of values created and accessed by a GEP instruction.
   * E.g. a GEP instruction:
   * %a = getelementptr %struct.foo, %struct.foo* %dst_reg, i64 0, i32 1.
   * %b = load i64, i64* %a, align 8
   * Will be stored in the map as: {a : <foo, [0, 1]>}.
   *
   * Reason for addition of GEPMap: Usually, load instructions are preceded by a
   * GEP, which makes sure that the pointer used by the load looks into the
   * mostRecentMemoryDef. However, there are some cases where a load instruction
   * is not preceded by a GEP (e.g. when compiled with O1). The loads uses to an
   * older GEP pointer. Since GEPMap maintains each GEP pointer and its
   * corresponding GEP indices, it can be used to treat the load as if it were
   * preceded by a GEP */
  std::unordered_map<Value *, ValueIndicesPair> GEPMap;

  std::unordered_map<Value *, ValuePair> SelectMap;

  std::unordered_map<Value *, std::vector<ValueBBPair>> PhiMap;

  /* Associate with each BasicBlock, a ValueBVTreeMap; to track insertValue
   * instructions or intrinsic call instructions that return an aggregate type.
   * This map will store BVTrees for aggregate types that can be retreived
   * later. */
  std::unordered_map<BasicBlock *, ValueBVTreeMap *> BBValueBVTreeMap;

  /* Functions to print things */
  void printEdgeAssertionsMap();
  void printPathConditionsMap();
  void printBBAssertionsMap(BasicBlock *BB = nullptr);
  std::string ValueBVTreeMapToString(ValueBVTreeMap vt);
  void printValueBVTreeMap(ValueBVTreeMap vt);
  void printMemoryAccessValueBVTreeMap();
  void printPhiResolutionMap();
  void printMemoryPhiResolutionMap();
  void printGEPMap();
  void printSelectMap();
  void printPhiMap();
  std::string GEPMapSingleElementToString(Value *v0, Value *v1,
                                          std::vector<int> *gepIndices);
  std::string stdVectorIntToString(std::vector<int> &vec);

  /* Functions that handle individual llvm instructions */
  void handleCastInst(CastInst &i);
  void handleBinaryOperatorInst(BinaryOperator &i);
  void handleExtractValueInst(ExtractValueInst &i);
  void handleReturnInstPointerArgs(ReturnInst &i);
  bool functionHasPointerArguments(Function &F);
  void handleReturnInst(ReturnInst &i, FunctionEncoderPassType passID);
  void handleICmpInst(ICmpInst &i);
  void handleSelectInst(SelectInst &i);
  void handleBranchInst(BranchInst &i, FunctionEncoderPassType passID);
  void handlePhiNode(PHINode &inst, int passID);
  void handlePhiNodeSetupBitVecs(PHINode &inst);
  void handlePhiNodeResolvePathConditions(PHINode &inst);
  void handleGEPInst(GetElementPtrInst &i);
  void handleLoadInst(LoadInst &i);
  void handleStoreInst(StoreInst &i);
  void handleMemoryPhiNode(MemoryPhi &mphi, FunctionEncoderPassType passID);
  void handleCallInst(CallInst &i);
  void handleIntrinsicCallInst(IntrinsicInst &i);
  void handleLLVMOverflowInstrinsics(IntrinsicInst &i);
  void handleInstrinsicLLVMMax(IntrinsicInst &i);
  void handleIntrinsicLLVMCTPop(IntrinsicInst &i);
  void handleGEPInstFromSelect(GetElementPtrInst &i);
  void handleGEPInstFromPHI(GetElementPtrInst &i);
  void handlePhiInstPointer(PHINode &inst);
  void handleStoreToGEPPtrDerivedFromFunctionArg(
      z3::expr BVToStore, Value *destPointerValue,
      std::vector<int> *GEPMapIndices, ValueBVTreeMap *newValueBVTreeMap,
      MemoryUseOrDef *storeMemoryAccess);
  void handleLoadFromGEPPtrDerivedFromSelect(LoadInst &i,
                                             SelectInst &selectInst);
  void handleLoadFromGEPPtrDerivedFromPhi(LoadInst &i, PHINode &phiNode);

  void handleStoreToGEPPtr(z3::expr BVToStore, GetElementPtrInst &GEPInst,
                           ValueBVTreeMap *newValueBVTreeMap,
                           MemoryUseOrDef *storeMemoryAccess);
  void handleStoreToGEPPtrDerivedFromSelect(z3::expr BVToStore,
                                            SelectInst &selectInst,
                                            std::vector<int> *GEPMapIndices,
                                            ValueBVTreeMap *newValueBVTreeMap,
                                            MemoryUseOrDef *storeMemoryAccess);
  void handleStoreToGEPPtrDerivedFromPhi(z3::expr BVToStore, PHINode &phiInst,
                                         std::vector<int> *GEPMapIndices,
                                         ValueBVTreeMap *newValueBVTreeMap,
                                         MemoryUseOrDef *storeMemoryAccess);

  void handleStoreToPhiPtr(z3::expr BVToStore, PHINode &phiPtrInst,
                           ValueBVTreeMap *newValueBVTreeMap,
                           MemoryUseOrDef *storeMemoryAccess);
  void handleStoreToPhiPtrDerivedFromPhi(z3::expr BVToStore, PHINode &phiInst,
                                         std::vector<int> *GEPMapIndices,
                                         ValueBVTreeMap *newValueBVTreeMap,
                                         MemoryUseOrDef *storeMemoryAccess,
                                         z3::expr pathCondition);

  /* Json output related functions */
  void populateInputAndOutputJsonDict();
  Json::Value *setupJSONDictForArg(Value *argVal);
  Json::Value *getJsonDictFromValueBVTree(Value *val, BVTree *bvT);
  void JsonRecursive(Json::Value *jsonRoot, BVTree *bvTreeRoot,
                     StructType *baseStructType, int recursionDepth);

  /* Other high-level functions */
  void populateBBAssertionsMap(BasicBlock &B);
  void populatePathConditionsMap(BasicBlock &B);
  z3::expr_vector encodeFunctionBody(Function &F);
  void convertAggregateTypeArgToBVTree(BVTree *parent,
                                       StructType *baseStructType,
                                       std::string prefix);
  BVTree *setupBVTreeForArg(Value *argVal, std::string prefix);
  bool isRelevantStruct(StructType *s);

  bool isFunctionCFGaDAG(llvm::Function &F);
  void buildSMT();
  std::string toString();
};

#endif // LLVM2SMT_FUNCTIONENCODER_H