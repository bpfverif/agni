#ifndef LLVM2SMT_BITVEC_HELPER_HPP
#define LLVM2SMT_BITVEC_HELPER_HPP

#include <sstream>
#include <stdexcept>
#include <unordered_map>
#include <vector>

#include <z3++.h>

#include <llvm/IR/Constants.h>
#include <llvm/IR/Value.h>

using namespace llvm;

class BitVecHelper {
private:
  static int unique_bv_id;
  static std::string global_bv_suffix;

public:
  static std::unordered_map<Value *, z3::expr> singleValueTypeMap;
  static z3::expr getBitVec(unsigned bitwidth, std::string = "");
  static z3::expr getBool(std::string prefix);
  static z3::expr getBitVecSingValType(Value *);
  static bool isValueConstantInt(Value *);
  static int64_t getConstantIntValue(Value *);
  static void init(std::string);

  static std::unordered_map<std::string, z3::expr> fieldBitVecMap;

  static z3::expr getBitVecForField(Type *fieldType,
                                    const std::string &fieldName);
};

#endif // LLVM2SMT_BITVEC_HELPER_HPP