#ifndef LLVM2SMT_PROMOTE_MEMCPY_H
#define LLVM2SMT_PROMOTE_MEMCPY_H

#include <llvm/IR/PassManager.h>
#include <llvm/IR/IntrinsicInst.h>
#include <llvm/IR/IRBuilder.h>
#include <llvm/Passes/PassBuilder.h>
#include <llvm/Passes/PassPlugin.h>


// https://github.com/intel/llvm/blob/97d7eec5a71e0b28f688600f3666ae6eaff0403d/llvm-spirv/lib/SPIRV/SPIRVRegularizeLLVM.cpp
// https://llvm.org/doxygen/SPIRVPrepareFunctions_8cpp_source.html

struct LowerFunnelShifts : llvm::PassInfoMixin<LowerFunnelShifts> {
  llvm::PreservedAnalyses run(llvm::Module &M, llvm::ModuleAnalysisManager &);
  // bool runOnModule(llvm::Module &M);

  // std::string lowerLLVMIntrinsicName(llvm::IntrinsicInst *II);

  /// No SPIR-V counterpart for @llvm.fshl.i* intrinsic. It will be lowered
  /// to a newly generated @spirv.llvm_fshl_i* function.
  /// Conceptually, FSHL:
  /// 1. concatenates the ints, the first one being the more significant;
  /// 2. performs a left shift-rotate on the resulting doubled-sized int;
  /// 3. returns the most significant bits of the shift-rotate result,
  ///    the number of bits being equal to the size of the original integers.
  /// The actual implementation algorithm will be slightly different to speed
  /// things up.
  // void lowerFunnelShifts(llvm::IntrinsicInst *FSHIntrinsic);
  // void lowerFunnelShiftLeft(llvm::IntrinsicInst *FSHLIntrinsic);
  // void buildFunnelShiftLeftFunc(llvm::Function *FSHLFunc);


private:
  llvm::Module *module;
  llvm::LLVMContext *context;
};
#endif // LLVM2SMT_PROMOTE_MEMCPY_H
