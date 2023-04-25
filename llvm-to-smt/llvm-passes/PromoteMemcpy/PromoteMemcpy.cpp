//=============================================================================
// FILE:
//    PromoteMemcpy.cpp
//
// DESCRIPTION:
//    Promote memcpy instructions to sequence of stores.
//
//=============================================================================
#include "PromoteMemcpy.hpp"

using namespace llvm;

// TODO Convert to ModulePass

bool PromoteMemcpy::runOnFunction(Function &F, FunctionAnalysisManager &FAM) {

  char *functionToPromoteMemcpy = std::getenv("FUNCTION_TO_PROMOTE_MEMCPY");
  if (!functionToPromoteMemcpy) {
    throw std::invalid_argument(
        "No function specified. Please set the FUNCTION_TO_PROMOTE_MEMCPY "
        "environment variable.\n");
  }

  if (F.getName() != functionToPromoteMemcpy)
    return false;

  if (F.empty())
    return false;

  m_DT = &FAM.getResult<DominatorTreeAnalysis>(F);
  m_M = F.getParent();
  m_Ctx = &m_M->getContext();
  m_DL = &m_M->getDataLayout();
  m_AC = &FAM.getResult<AssumptionAnalysis>(F);

  bool Changed = false;
  SmallVector<MemCpyInst *, 8> ToDeleteQueue;
  outs() << "\n############## Start Promote Memcpy ###################\n";

  for (auto &BB : F)
    for (auto &I : BB)
      if (auto *MCpy = dyn_cast<MemCpyInst>(&I)) {
        MCpy->print(outs() << "Visiting: \n");
        outs() << "\n";

        if (!simplifyMemCpy(MCpy))
          continue;

        ToDeleteQueue.push_back(MCpy);
        Changed = true;
      }

  outs() << "Removing dead memcpys in " << F.getName() << ":\n";
  for (auto *MCpy : ToDeleteQueue) {
    MCpy->print(outs() << "\n\t");

    // Using getArgOperand API to avoid looking through casts.
    auto *SrcPtr = dyn_cast<BitCastInst>(MCpy->getArgOperand(1));
    auto *DstPtr = dyn_cast<BitCastInst>(MCpy->getArgOperand(0));

    MCpy->eraseFromParent();
    if (SrcPtr && SrcPtr->hasNUses(0)) {
      SrcPtr->print(outs() << "\n\t\tdeleting:\t");
      SrcPtr->eraseFromParent();
    }
    if (DstPtr && DstPtr->hasNUses(0)) {
      DstPtr->print(outs() << "\n\t\tdeleting:\t");
      DstPtr->eraseFromParent();
    }
  }

  outs() << "\n############## End Promote Memcpy ###################\n";
  outs().flush();
  return Changed;
}

bool PromoteMemcpy::simplifyMemCpy(MemCpyInst *MI) {
  assert(MI);

  auto DstAlign = getKnownAlignment(MI->getDest(), *m_DL, MI, m_AC, m_DT);
  auto SrcAlign = getKnownAlignment(MI->getSource(), *m_DL, MI, m_AC, m_DT);
  outs() << "DstAlign: " << DstAlign.value() << "\n";
  outs() << "SrcAlign: " << SrcAlign.value() << "\n";

  // skip non-constant length memcpy()
  ConstantInt *MemOpLength = dyn_cast<ConstantInt>(MI->getLength());
  if (!MemOpLength) {
    return false;
  }

  // Source and destination pointer types are always "i8*" for intrinsic.  See
  // if the size is something we can handle with a single primitive load/store.
  // A single load+store correctly handles overlapping memory in the memmove
  // case.
  uint64_t Size = MemOpLength->getLimitedValue();
  if (Size == 0) {
    outs() << "unexpected 0 length memcpy: " << *MI << "\n";
    return false;
  }
  auto *SrcPtr = MI->getSource();
  auto *DstPtr = MI->getDest();
  outs() << *SrcPtr << "\n";
  outs() << *DstPtr << "\n";

  unsigned SrcAddrSp = cast<PointerType>(SrcPtr->getType())->getAddressSpace();
  unsigned DstAddrSp = cast<PointerType>(DstPtr->getType())->getAddressSpace();

  if (SrcAddrSp != DstAddrSp) {
    llvm_unreachable("unexpected");
    return false;
  }

  auto *SrcPtrTy = cast<PointerType>(SrcPtr->getType());
  auto *DstPtrTy = cast<PointerType>(DstPtr->getType());

  if (SrcPtrTy != DstPtrTy) {
    outs() << "memcpy between different types: " << *MI << "\n";
    return false;
  }

  if (!SrcPtrTy->getPointerElementType()->isFirstClassType()) {
    outs() << "Not a first class type! " << *MI << "\n";
    return false;
  }

  outs() << "\nSrc:\t";
  SrcPtr->print(outs());
  SrcPtrTy->print(outs() << "\t");
  outs() << "\nDst:\t";
  DstPtr->print(outs());
  DstPtrTy->print(outs() << "\t");
  outs() << "\n";
  outs().flush();

  auto *BufferTy = dyn_cast<StructType>(SrcPtrTy->getPointerElementType());
  // require src to be a struct
  if (!BufferTy) {
    outs() << "memcpy on non-struct types: " << *MI;
    return false;
  }
  // require constant length argument equal to struct size
  if (m_DL->getTypeStoreSize(BufferTy) != Size) {
    outs() << "memcpy length not equal to struct size: " << *MI;
    return false;
  }

  llvm::IRBuilder<> Builder(MI);
  auto *I64Ty = IntegerType::getInt64Ty(*m_Ctx);
  auto *NullInt = Constant::getNullValue(I64Ty);
  auto *I32Ty = IntegerType::getInt32Ty(*m_Ctx);

  // Perform field-wise copy. Note that this doesn't recurse and only explores
  // the immediately visible fields.
  //
  // The transformation we do here looks roughly like this:
  //   memcpy(Dst, Source, sizeof(BufferTy))
  //    ||
  //    V
  // for each field_id in fields(BufferTy):
  //   *GEP(Dst, field_id) = *GEP(Src, field_id)
  //

  using Transfer = std::pair<Value *, Value *>;
  SmallVector<Transfer, 4> ToLower = {std::make_pair(SrcPtr, DstPtr)};
  while (!ToLower.empty()) {
    Value *TrSrc, *TrDst;
    std::tie(TrSrc, TrDst) = ToLower.pop_back_val();
    auto *Ty = TrSrc->getType();
    assert(Ty == TrDst->getType());

    if (!Ty->isStructTy()) {
      auto *NewLoad = Builder.CreateLoad(TrSrc, SrcPtr->getName() + ".pmcpy");
      auto *NewStore = Builder.CreateStore(NewLoad, TrDst);

      outs() << "New load-store:\n\t";
      NewLoad->print(outs());
      outs() << "\n\t";
      NewStore->print(outs());
      outs() << "\n";
      continue;
    }

    SmallVector<Transfer, 8> TmpBuff;
    for (unsigned i = 0, e = Ty->getStructNumElements(); i != e; ++i) {
      auto *Idx = Constant::getIntegerValue(I32Ty, APInt(32, i));
      auto *SrcGEP = Builder.CreateInBoundsGEP(nullptr, SrcPtr, {NullInt, Idx},
                                               "src.gep.pmcpy");
      auto *DstGEP = Builder.CreateInBoundsGEP(nullptr, DstPtr, {NullInt, Idx},
                                               "buffer.gep.pmcpy");
      TmpBuff.push_back({SrcGEP, DstGEP});
    }

    for (auto &P : llvm::reverse(TmpBuff))
      ToLower.push_back(P);

    outs() << "\tSecond level\n";
  }
  return true;
}

//-----------------------------------------------------------------------------
// New PM Registration
//-----------------------------------------------------------------------------
llvm::PassPluginLibraryInfo getPromoteMemcpyPluginInfo() {
  return {LLVM_PLUGIN_API_VERSION, "PromoteMemcpy", LLVM_VERSION_STRING,
          [](PassBuilder &PB) {
            PB.registerPipelineParsingCallback(
                [](StringRef Name, FunctionPassManager &FPM,
                   ArrayRef<PassBuilder::PipelineElement>) {
                  if (Name == "promote-memcpy") {
                    FPM.addPass(PromoteMemcpy());
                    return true;
                  }
                  return false;
                });
          }};
}

// This is the core interface for pass plugins. It guarantees that 'opt' will
// be able to recognize PromoteMemcpy when added to the pass pipeline on the
// command line, i.e. via '-passes=hello-world'
extern "C" LLVM_ATTRIBUTE_WEAK ::llvm::PassPluginLibraryInfo
llvmGetPassPluginInfo() {
  return getPromoteMemcpyPluginInfo();
}
