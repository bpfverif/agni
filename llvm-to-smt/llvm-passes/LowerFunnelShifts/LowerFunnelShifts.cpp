//=============================================================================
// FILE:
//    LowerFunnelShifts.cpp
//
// DESCRIPTION:
//   Lower llvm.fshl and llvm.fshr calls to a separate function
//
//=============================================================================
#include "LowerFunnelShifts.hpp"
#include <llvm/IR/Attributes.h>
#include <llvm/IR/IntrinsicInst.h>
#include <llvm/Transforms/Utils/Cloning.h>

#define DEBUG_TYPE "lower-funnel-shifts"
using namespace llvm;

Function *getOrCreateFunction(Module *M, Type *RetTy, ArrayRef<Type *> ArgTypes,
                              StringRef Name) {
  FunctionType *FT = FunctionType::get(RetTy, ArgTypes, false);
  Function *F = M->getFunction(Name);
  if (F && F->getFunctionType() == FT)
    return F;
  Function *NewF = Function::Create(FT, GlobalValue::ExternalLinkage, Name, M);
  if (F)
    NewF->setDSOLocal(F->isDSOLocal());
  NewF->setCallingConv(CallingConv::C);
  return NewF;
}

std::string lowerLLVMIntrinsicName(IntrinsicInst *II) {
  Function *IntrinsicFunc = II->getCalledFunction();
  assert(IntrinsicFunc && "Missing function");
  std::string FuncName = IntrinsicFunc->getName().str();
  std::replace(FuncName.begin(), FuncName.end(), '.', '_');
  FuncName = "spirv." + FuncName;
  return FuncName;
}

void lowerFunnelShifts(IntrinsicInst *FSHIntrinsic) {
  // Get a separate function - otherwise, we'd have to rework the CFG of the
  // current one. Then simply replace the intrinsic uses with a call to the new
  // function.
  // Generate LLVM IR for  i* @spirv.llvm_fsh?_i* (i* %a, i* %b, i* %c)
  Module *M = FSHIntrinsic->getModule();
  FunctionType *FSHFuncTy = FSHIntrinsic->getFunctionType();
  Type *FSHRetTy = FSHFuncTy->getReturnType();
  const std::string FuncName = lowerLLVMIntrinsicName(FSHIntrinsic);
  Function *FSHFunc =
      getOrCreateFunction(M, FSHRetTy, FSHFuncTy->params(), FuncName);
  FSHFunc->addFnAttr("optnone");
  if (!FSHFunc->empty()) {
    FSHIntrinsic->setCalledFunction(FSHFunc);
    return;
  }
  BasicBlock *RotateBB = BasicBlock::Create(M->getContext(), "rotate", FSHFunc);
  IRBuilder<> IRB(RotateBB);
  Type *Ty = FSHFunc->getReturnType();
  // Build the actual funnel shift rotate logic.
  // In the comments, "int" is used interchangeably with "vector of int
  // elements".
  FixedVectorType *VectorTy = dyn_cast<FixedVectorType>(Ty);
  Type *IntTy = VectorTy ? VectorTy->getElementType() : Ty;
  unsigned BitWidth = IntTy->getIntegerBitWidth();
  ConstantInt *BitWidthConstant = IRB.getInt({BitWidth, BitWidth});
  Value *BitWidthForInsts =
      VectorTy
          ? IRB.CreateVectorSplat(VectorTy->getNumElements(), BitWidthConstant)
          : BitWidthConstant;
  Value *RotateModVal =
      IRB.CreateURem(/*Rotate*/ FSHFunc->getArg(2), BitWidthForInsts);
  Value *FirstShift = nullptr, *SecShift = nullptr;
  if (FSHIntrinsic->getIntrinsicID() == Intrinsic::fshr) {
    // Shift the less significant number right, the "rotate" number of bits
    // will be 0-filled on the left as a result of this regular shift.
    FirstShift = IRB.CreateLShr(FSHFunc->getArg(1), RotateModVal);
  } else {
    // Shift the more significant number left, the "rotate" number of bits
    // will be 0-filled on the right as a result of this regular shift.
    FirstShift = IRB.CreateShl(FSHFunc->getArg(0), RotateModVal);
  }
  // We want the "rotate" number of the more significant int's LSBs (MSBs) to
  // occupy the leftmost (rightmost) "0 space" left by the previous operation.
  // Therefore, subtract the "rotate" number from the integer bitsize...
  Value *SubRotateVal = IRB.CreateSub(BitWidthForInsts, RotateModVal);
  if (FSHIntrinsic->getIntrinsicID() == Intrinsic::fshr) {
    // ...and left-shift the more significant int by this number, zero-filling
    // the LSBs.
    SecShift = IRB.CreateShl(FSHFunc->getArg(0), SubRotateVal);
  } else {
    // ...and right-shift the less significant int by this number, zero-filling
    // the MSBs.
    SecShift = IRB.CreateLShr(FSHFunc->getArg(1), SubRotateVal);
  }
  // A simple binary addition of the shifted ints yields the final result.
  IRB.CreateRet(IRB.CreateOr(FirstShift, SecShift));

  FSHIntrinsic->setCalledFunction(FSHFunc);
}

#if 0
static bool lowerIntrinsicToFunction(IntrinsicInst *Intrinsic) {
  // For @llvm.memset.* intrinsic cases with constant value and length arguments
  // are emulated via "storing" a constant array to the destination. For other
  // cases we wrap the intrinsic in @spirv.llvm_memset_* function and expand the
  // intrinsic to a loop via expandMemSetAsLoop().
  if (auto *MSI = dyn_cast<MemSetInst>(Intrinsic))
    if (isa<Constant>(MSI->getValue()) && isa<ConstantInt>(MSI->getLength()))
      return false; // It is handled later using OpCopyMemorySized.
 
  Module *M = Intrinsic->getModule();
  std::string FuncName = lowerLLVMIntrinsicName(Intrinsic);
  // Redirect @llvm.intrinsic.* call to @spirv.llvm_intrinsic_*
  Function *F = M->getFunction(FuncName);
  if (F) {
    Intrinsic->setCalledFunction(F);
    return true;
  }
  // TODO copy arguments attributes: nocapture writeonly.
  FunctionCallee FC =
      M->getOrInsertFunction(FuncName, Intrinsic->getFunctionType());
  auto IntrinsicID = Intrinsic->getIntrinsicID();
  Intrinsic->setCalledFunction(FC);
 
  F = dyn_cast<Function>(FC.getCallee());
  assert(F && "Callee must be a function");
  return true;
}
#endif

// Substitutes calls to LLVM intrinsics with either calls to SPIR-V intrinsics
// or calls to proper generated functions. Returns True if F was modified.
bool substituteIntrinsicCalls(Function *F) {
  bool Changed = false;
  for (BasicBlock &BB : *F) {
    for (Instruction &I : BB) {
      auto Call = dyn_cast<CallInst>(&I);
      if (!Call)
        continue;
      Function *CF = Call->getCalledFunction();
      if (!CF || !CF->isIntrinsic())
        continue;
      auto *II = cast<IntrinsicInst>(Call);
#if 0
      if (II->getIntrinsicID() == Intrinsic::memset ||
          II->getIntrinsicID() == Intrinsic::bswap)
        Changed |= lowerIntrinsicToFunction(II);
      else
#endif
      if (II->getIntrinsicID() == Intrinsic::fshl ||
          II->getIntrinsicID() == Intrinsic::fshr) {
        lowerFunnelShifts(II);
        outs() << "[substituteIntrinsicCalls] lowered fshl in function: "
               << F->getName() << "\n";
        Changed = true;
      }
    }
  }
  return Changed;
}

#if 0
// Returns F if aggregate argument/return types are not present or cloned F
// function with the types replaced by i32 types. The change in types is
// noted in 'spv.cloned_funcs' metadata for later restoration.
Function *
removeAggregateTypesFromSignature(Function *F) {
  IRBuilder<> B(F->getContext());
 
  bool IsRetAggr = F->getReturnType()->isAggregateType();
  bool HasAggrArg =
      std::any_of(F->arg_begin(), F->arg_end(), [](Argument &Arg) {
        return Arg.getType()->isAggregateType();
      });
  bool DoClone = IsRetAggr || HasAggrArg;
  if (!DoClone)
    return F;
  SmallVector<std::pair<int, Type *>, 4> ChangedTypes;
  Type *RetType = IsRetAggr ? B.getInt32Ty() : F->getReturnType();
  if (IsRetAggr)
    ChangedTypes.push_back(std::pair<int, Type *>(-1, F->getReturnType()));
  SmallVector<Type *, 4> ArgTypes;
  for (const auto &Arg : F->args()) {
    if (Arg.getType()->isAggregateType()) {
      ArgTypes.push_back(B.getInt32Ty());
      ChangedTypes.push_back(
          std::pair<int, Type *>(Arg.getArgNo(), Arg.getType()));
    } else
      ArgTypes.push_back(Arg.getType());
  }
  FunctionType *NewFTy =
      FunctionType::get(RetType, ArgTypes, F->getFunctionType()->isVarArg());
  Function *NewF =
      Function::Create(NewFTy, F->getLinkage(), F->getName(), *F->getParent());
 
  ValueToValueMapTy VMap;
  auto NewFArgIt = NewF->arg_begin();
  for (auto &Arg : F->args()) {
    StringRef ArgName = Arg.getName();
    NewFArgIt->setName(ArgName);
    VMap[&Arg] = &(*NewFArgIt++);
  }
  SmallVector<ReturnInst *, 8> Returns;
  llvm::CloneFunctionInto(NewF, F, VMap, false,
                    Returns);
  NewF->takeName(F);
 
  NamedMDNode *FuncMD =
      F->getParent()->getOrInsertNamedMetadata("spv.cloned_funcs");
  SmallVector<Metadata *, 2> MDArgs;
  MDArgs.push_back(MDString::get(B.getContext(), NewF->getName()));
  for (auto &ChangedTyP : ChangedTypes)
    MDArgs.push_back(MDNode::get(
        B.getContext(),
        {ConstantAsMetadata::get(B.getInt32(ChangedTyP.first)),
         ValueAsMetadata::get(Constant::getNullValue(ChangedTyP.second))}));
  MDNode *ThisFuncMD = MDNode::get(B.getContext(), MDArgs);
  FuncMD->addOperand(ThisFuncMD);
 
  for (auto *U : make_early_inc_range(F->users())) {
    if (auto *CI = dyn_cast<CallInst>(U))
      CI->mutateFunctionType(NewF->getFunctionType());
    U->replaceUsesOfWith(F, NewF);
  }
  return NewF;
}
#endif

bool runOnModule(Module &M) {
  bool Changed = false;
  char *functionToLowerFunnelShifts =
      std::getenv("FUNCTION_TO_LOWER_FUNNEL_SHIFTS");
  if (!functionToLowerFunnelShifts) {
    throw std::invalid_argument(
        "No function specified. Please set the FUNCTION_TO_LOWER_FUNNEL_SHIFTS "
        "environment variable.\n");
  }
  for (Function &F : M) {
    // if (F.getName() != functionToLowerFunnelShifts)
    //   continue;
    Changed |= substituteIntrinsicCalls(&F);
  }

#if 0
  std::vector<Function *> FuncsWorklist;
  for (auto &F : M)
    FuncsWorklist.push_back(&F);
 
  for (auto *F : FuncsWorklist) {
    Function *NewF = removeAggregateTypesFromSignature(F);
 
    if (NewF != F) {
      F->eraseFromParent();
      Changed = true;
    }
  }
#endif
  return Changed;
}

PreservedAnalyses LowerFunnelShifts::run(llvm::Module &M,
                                         llvm::ModuleAnalysisManager &MAM) {

  bool Changed = runOnModule(M);
  return (Changed ? llvm::PreservedAnalyses::none()
                  : llvm::PreservedAnalyses::all());
}

//-----------------------------------------------------------------------------
// New PM Registration
//-----------------------------------------------------------------------------
llvm::PassPluginLibraryInfo getLowerFunnelShiftsPluginInfo() {
  return {LLVM_PLUGIN_API_VERSION, "lower-funnel-shifts", LLVM_VERSION_STRING,
          [](PassBuilder &PB) {
            PB.registerPipelineParsingCallback(
                [](StringRef Name, ModulePassManager &MPM,
                   ArrayRef<PassBuilder::PipelineElement>) {
                  if (Name == "lower-funnel-shifts") {
                    MPM.addPass(LowerFunnelShifts());
                    return true;
                  }
                  return false;
                });
          }};
}

extern "C" LLVM_ATTRIBUTE_WEAK ::llvm::PassPluginLibraryInfo
llvmGetPassPluginInfo() {
  return getLowerFunnelShiftsPluginInfo();
}
