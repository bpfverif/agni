#include "BitvecHelper.hpp"

/* initialize global z3 context */
z3::context ctx;

/* initialize BitVecHelper static members */
int BitVecHelper::unique_bv_id = 0;
std::string BitVecHelper::global_bv_suffix = "";
std::unordered_map<Value *, z3::expr> BitVecHelper::singleValueTypeMap =
    std::unordered_map<Value *, z3::expr>();

z3::expr BitVecHelper::getBitVec(unsigned bitwidth, std::string prefix) {
  std::string unique_name = prefix + "_" + BitVecHelper::global_bv_suffix +
                            "_" + std::to_string(BitVecHelper::unique_bv_id++);
  z3::expr ret = ctx.bv_const(unique_name.c_str(), bitwidth);
  outs() << "[getBitVec] "
         << "returning uniq w prefix: " << ret.to_string().c_str() << "\n";
  return ret;
}

bool BitVecHelper::isValueConstantInt(Value *v) {
  if (ConstantInt *CI = dyn_cast<ConstantInt>(v)) {
    return true;
  } else {
    return false;
  }
}

/* TODO should this always return an int? */
int64_t BitVecHelper::getConstantIntValue(Value *v) {
  assert(isValueConstantInt(v) == true);
  ConstantInt *CI = cast<ConstantInt>(v);
  return CI->getSExtValue();
}

z3::expr BitVecHelper::getBitVecSingValType(Value *v) {
  assert((v != nullptr));
  outs() << "[getBitVecSingValType] " << *v << "\n";
  Type *t = v->getType();
  if (t->isAggregateType()) {
    throw std::runtime_error("[getBitVecSingValType] Value " +
                             v->getName().str() + " is of aggregate type\n");
  }
  outs() << "[getBitVecSingValType] type: " << *t << "\n";
  z3::expr resBV(ctx);
  bool BVExists = (BitVecHelper::singleValueTypeMap.find(v) !=
                   BitVecHelper::singleValueTypeMap.end());
  outs().flush();
  if (isValueConstantInt(v)) {
    resBV = ctx.bv_val(getConstantIntValue(v), t->getIntegerBitWidth());
    outs() << "[getBitVecSingValType] "
           << "returning new constBV\n";
    BitVecHelper::unique_bv_id++;
  } else if (BVExists) {
    resBV = BitVecHelper::singleValueTypeMap.at(v);
    outs() << "[getBitVecSingValType] "
           << "returning existing BV\n ";
  } else {
    std::string bvName = v->hasName() ? std::string(v->getName()) : "bv";
    resBV = getBitVec(t->getIntegerBitWidth(), bvName);
    outs() << "[getBitVecSingValType] "
           << "returning new BV\n ";
    BitVecHelper::singleValueTypeMap.insert({v, resBV});
  }

  outs() << "[getBitVecSingValType] " << resBV.to_string().c_str() << "\n";
  // astIDMap.insert({Z3_get_ast_id(ctx, ret), ret});
  return resBV;
}

void BitVecHelper::init(std::string s) {
  BitVecHelper::unique_bv_id = 0;
  BitVecHelper::global_bv_suffix = s;
}