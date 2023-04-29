#include "FunctionEncoder.hpp"

std::string FunctionEncoder::toString() {
  z3::expr f = z3::mk_and(this->functionEncodingZ3ExprVec);
  z3::solver solv = z3::solver(ctx);
  solv.add(f);

  Z3_set_ast_print_mode(ctx, Z3_PRINT_SMTLIB_FULL);
  std::string os;
  llvm::raw_string_ostream llvmos(os);
  std::ostringstream oss;
  Json::StyledWriter styledWriter;

  llvmos << "---------\n";
  llvmos << "Function: " << this->currentFunction->getName() << "\n";
  llvmos << "---------\n";

  llvmos << "---------\n";
  llvmos << "Inputs: \n";
  std::string inputJsonDictStr = styledWriter.write(*(this->inputJsonDict));
  llvmos << inputJsonDictStr << "\n";
  llvmos << "---------\n";

  llvmos << "\n---------\n";
  llvmos << "Outputs: \n";
  std::string outputJsonDictStr = styledWriter.write(*(this->outputJsonDict));
  llvmos << outputJsonDictStr << "\n";
  llvmos << "\n---------\n";

  llvmos << "Solver: \n";
  llvmos << solv.to_smt2();
  llvmos << "\n---------\n";

  return llvmos.str();
}

void FunctionEncoder::printEdgeAssertionsMap() {
  for (auto &pair : EdgeAssertionsMap) {
    outs() << "<" << std::get<0>(pair).first->getName() << ", "
           << std::get<0>(pair).second->getName() << "> :";
    outs() << std::get<1>(pair).to_string().c_str() << "\n";
  }
}

void FunctionEncoder::printPathConditionsMap() {
  for (auto KeyValue : pathConditionsMap) {
    BasicBlock *BB = KeyValue.first;
    z3::expr Z3Expr = KeyValue.second;
    outs() << BB->getName() << "\n";
    outs() << "  " << Z3Expr.to_string().c_str() << "\n";
  }
}

void FunctionEncoder::printBBAssertionsMap(BasicBlock *BB) {
  if (BB) {
    for (auto Z3Expr : BBAssertionsMap.at(BB)) {
      outs() << "  " << Z3Expr.to_string().c_str() << "\n";
    }
    outs() << "\n";
    return;
  }
  for (auto KeyValue : BBAssertionsMap) {
    BasicBlock *BB = KeyValue.first;
    z3::expr_vector Z3ExprVec = KeyValue.second;
    outs() << BB->getName() << ", " << Z3ExprVec.size() << "\n";
    for (auto Z3Expr : Z3ExprVec) {
      outs() << "  " << Z3Expr.to_string().c_str() << "\n";
    }
  }
  outs() << "\n";
}

std::string FunctionEncoder::ValueBVTreeMapToString(ValueBVTreeMap vt) {
  std::string os;
  llvm::raw_string_ostream llvmos(os);
  for (auto kv : vt) {
    Value *v = kv.first;
    BVTree *bvt = kv.second;
    llvmos << "- " << v->getName() << ": " << bvt->toString() << "\n";
  }
  return llvmos.str();
}

void FunctionEncoder::printValueBVTreeMap(ValueBVTreeMap vt) {
  outs() << ValueBVTreeMapToString(vt) << "\n";
  outs().flush();
}

void FunctionEncoder::printMemoryAccessValueBVTreeMap() {
  std::string os;
  llvm::raw_string_ostream llvmos(os);
  for (std::pair<MemoryAccess *, ValueBVTreeMap> kv :
       MemoryAccessValueBVTreeMap) {
    MemoryAccess *ma = kv.first;
    ValueBVTreeMap vt = kv.second;
    llvmos << *ma << " : {\n" << ValueBVTreeMapToString(vt) << "}\n";
  }
  outs() << os << "\n";
}

std::string FunctionEncoder::stdVectorIntToString(std::vector<int> &vec) {
  std::stringstream strStream;
  std::copy(vec.begin(), vec.end(), std::ostream_iterator<int>(strStream, " "));
  return "[ " + strStream.str() + "]";
}

std::string
FunctionEncoder::GEPMapSingleElementToString(Value *v0, Value *v1,
                                             std::vector<int> *gepIndices) {

  std::string os;
  llvm::raw_string_ostream llvmos(os);
  llvmos << v0->getName() << ", " << v1->getName() << ", [";
  for (int i = 0; i < gepIndices->size(); i++) {
    llvmos << gepIndices->at(i);
    if (i < gepIndices->size() - 1) {
      llvmos << ", ";
    }
  }
  llvmos << "]";
  return llvmos.str();
}

void FunctionEncoder::printGEPMap() {
  for (auto kv : GEPMap) {
    Value *v0 = kv.first;
    Value *v1 = kv.second.first;
    std::vector<int> *gepIndices = kv.second.second;
    outs() << GEPMapSingleElementToString(v0, v1, gepIndices);
    outs() << "\n";
  }
}

void FunctionEncoder::printPhiResolutionMap() {
  for (auto &bbPair : phiResolutionMap) {
    outs() << "<" << std::get<0>(bbPair).first->getName() << ", "
           << std::get<0>(bbPair).second->getName() << "> :";
    z3::expr_vector Z3ExprVec = std::get<1>(bbPair);
    for (auto Z3Expr : Z3ExprVec) {
      outs() << "\n  " << Z3Expr.to_string().c_str();
    }
    outs() << "\n";
  }
}

std::string Z3ExprVecToString(z3::expr_vector &v) {
  std::ostringstream oss;
  oss << "[";
  for (z3::expr e : v) {
    oss << e << "\n";
  }
  oss << "]";
  return oss.str();
}

// -----------------------------------------------------------------------------

void FunctionEncoder::handleCastInst(CastInst &i) {
  outs() << "[handleCastInst]\n";

  if (isa<BitCastInst>(&i)) {
    throw std::runtime_error("[handleCallInst]"
                             "bitcast instruction not supported\n");
  }

  auto BBAsstVecIter = BBAssertionsMap.find(currentBB);
  Value *op0Val = i.getOperand(0);
  Value *opResVal = dyn_cast<Value>(&i);

  z3::expr op0BV = BitVecHelper::getBitVecSingValType(op0Val);
  z3::expr opResBV = BitVecHelper::getBitVecSingValType(opResVal);
  unsigned op0BVWidth = op0BV.get_sort().bv_size();
  unsigned opResBVWidth = opResBV.get_sort().bv_size();
  z3::expr resultExpr(ctx);

  if (isa<TruncInst>(&i)) {
    outs() << "[handleCastInst] "
           << "TRUNC instruction\n";
    resultExpr = (opResBV == op0BV.extract(opResBVWidth - 1, 0));
  } else if (isa<ZExtInst>(&i)) {
    outs() << "[handleCastInst]"
           << "ZEXT instruction\n";
    resultExpr = (opResBV == z3::zext(op0BV, opResBVWidth - op0BVWidth));
  } else if (isa<SExtInst>(&i)) {
    outs() << "[handleCastInst]"
           << "SEXT instruction\n";
    resultExpr = (opResBV == z3::sext(op0BV, opResBVWidth - op0BVWidth));
  } else {
    errs() << "[handleCastInst]"
           << "Unknown CAST instruction: " << i << "\n";
  }

  outs() << resultExpr.to_string().c_str() << "\n";
  BBAsstVecIter->second.push_back(resultExpr);
}

void FunctionEncoder::handleBinaryOperatorInst(BinaryOperator &i) {
  outs() << "[handleBinaryOperatorInst]\n";

  auto BBAsstVecIter = BBAssertionsMap.find(currentBB);
  Value *op0Val = i.getOperand(0);
  Value *op1Val = i.getOperand(1);
  Value *opResVal = dyn_cast<Value>(&i);
  outs() << "[handleBinaryOperatorInst] "
         << "op0Val: " << *op0Val << "\n";
  outs() << "[handleBinaryOperatorInst] "
         << "op1Val: " << *op1Val << "\n";
  outs() << "[handleBinaryOperatorInst] "
         << "opResVal: " << *opResVal << "\n";

  z3::expr op0BV = BitVecHelper::getBitVecSingValType(op0Val);
  z3::expr op1BV = BitVecHelper::getBitVecSingValType(op1Val);
  z3::expr opResBV = BitVecHelper::getBitVecSingValType(opResVal);
  z3::expr resultExpr(ctx);

  switch (i.getOpcode()) {

  case Instruction::And: {
    outs() << "[handleBinaryOperatorInst] "
           << "AND instruction"
           << "\n";
    resultExpr = (opResBV == (op0BV & op1BV));
  } break;
  case Instruction::Or: {
    outs() << "[handleBinaryOperatorInst] "
           << "OR instruction"
           << "\n";
    resultExpr = (opResBV == (op0BV | op1BV));
  } break;
  case Instruction::Xor: {
    outs() << "[handleBinaryOperatorInst] "
           << "XOR instruction"
           << "\n";
    resultExpr = (opResBV == (op0BV ^ op1BV));
  } break;
  case Instruction::Add: {
    outs() << "[handleBinaryOperatorInst] "
           << "ADD instruction"
           << "\n";
    resultExpr = (opResBV == (op0BV + op1BV));
  } break;
  case Instruction::Sub: {
    outs() << "[handleBinaryOperatorInst] "
           << "SUB instruction"
           << "\n";
    resultExpr = (opResBV == (op0BV - op1BV));
  } break;
  case Instruction::Mul: {
    outs() << "[handleBinaryOperatorInst] "
           << "MUL instruction"
           << "\n";
    resultExpr = (opResBV == (op0BV * op1BV));
  } break;
  case Instruction::UDiv: {
    outs() << "[handleBinaryOperatorInst] "
           << "UDIV instruction"
           << "\n";
    resultExpr = (opResBV == (z3::udiv(op0BV, op1BV)));
  } break;
  case Instruction::Shl: {
    outs() << "[handleBinaryOperatorInst] "
           << "SHL instruction"
           << "\n";
    resultExpr = opResBV == z3::shl(op0BV, op1BV);
  } break;
  case Instruction::LShr: {
    outs() << "[handleBinaryOperatorInst] "
           << "LSHR instruction"
           << "\n";
    resultExpr = opResBV == z3::lshr(op0BV, op1BV);
  } break;
  case Instruction::AShr: {
    outs() << "[handleBinaryOperatorInst] "
           << "ASHR instruction"
           << "\n";
    resultExpr = opResBV == z3::ashr(op0BV, op1BV);
  } break;
  default:
    break;
  }
  outs() << resultExpr.to_string().c_str() << "\n";
  BBAsstVecIter->second.push_back(resultExpr);
}

/* If function has pointer arguments, construct new outputBitvectorTree(s)
 * corresponding to each pointer argument. These BVTrees will contain bitvectors
 * which are outputs to the function. Assert equivalences in the BBAssertionMap
 * to the bitvectors contained in the outputBitvectorTree(s), by looking at the
 * return instructions memoryDef.
 */
void FunctionEncoder::handleReturnInstPointerArgs(ReturnInst &i) {
  outs() << "[handleReturnInstPointerArgs] "
         << "\n";
  auto BBAsstVecIter = BBAssertionsMap.find(currentBB);
  outs() << "[handleReturnInstPointerArgs] "
         << "currentBB: " << currentBB->getName() << "\n";
  /* Return instruction will correspond to the mostRecentMemoryDef as we support
   * only single return instruction. */
  outs() << "[handleReturnInstPointerArgs] "
         << "mostRecentMemoryDef: " << *mostRecentMemoryDef << "\n";
  ValueBVTreeMap returnInstValueBVTreeMap =
      MemoryAccessValueBVTreeMap.at(mostRecentMemoryDef);

  /* For every pointer argument in the function, construct output equivalence z3
   * expressions. Note that we could have just updated outputValueBVTreeMap with
   * the BVTree for every arg from the mostRecentMemoryDef. But this doesn't
   * work if the function we are looking at has only one BasicBlock withs
   * statements that only update memory, and no updates are done to the
   * BBAssertionMap. Calling getEquivVector() constructs the bitvector
   * equivalences, and asserts them in the formula.
   */
  for (auto argIterator = currentFunction->arg_begin();
       argIterator != currentFunction->arg_end(); argIterator++) {
    Value *argVal = dyn_cast<Value>(argIterator);
    outs() << "[handleReturnInstPointerArgs] "
           << "argVal: " << *argVal << "\n";
    Type *argType = argIterator->getType();
    if (argType->isPointerTy()) {
      z3::expr_vector outputEqExprs(ctx);
      BVTree *outputBVTreeForArg =
          setupBVTreeForArg(argVal, argVal->getName().str());
      BVTree *originalBVTreeForArg = returnInstValueBVTreeMap.at(argVal);
      outs() << "[handleReturnInstPointerArgs] "
             << "originalBVTreeForArg: " << originalBVTreeForArg->toString()
             << "\n";
      BVTree::getEquivVector(originalBVTreeForArg, outputBVTreeForArg,
                             outputEqExprs);
      outs() << "[handleReturnInstPointerArgs] "
             << "outputEqExprs:\n";
      for (auto expr : outputEqExprs) {
        outs() << expr.to_string() << "\n";
        BBAsstVecIter->second.push_back(expr);
      }
      this->outputValueBVTreeMap->insert({argVal, outputBVTreeForArg});
    }
  }

  outs() << "[handleReturnInstPointerArgs] "
         << "outputValueBVTreeMap updated: \n";
  printValueBVTreeMap(*this->outputValueBVTreeMap);
  outs() << "[handleReturnInstPointerArgs] "
         << "currentBB AssertionsMap updated: \n";
  printBBAssertionsMap(currentBB);
}

bool FunctionEncoder::functionHasPointerArguments(Function &F) {
  outs() << "[functionHasPointerArguments]\n";
  for (auto argIterator = F.arg_begin(); argIterator != F.arg_end();
       argIterator++) {
    Type *t = argIterator->getType();
    if (t->isPointerTy()) {
      return true;
    }
  }
  return false;
}

void FunctionEncoder::handleReturnInst(ReturnInst &i) {
  outs() << "[handleReturnInst]\n";
  auto l = i.getReturnValue();
  if (functionReturnsVoid) {
    outs() << "[handleReturnInst]"
           << "return value: void\n";
  } else {
    outs() << "[handleReturnInst]"
           << "return value: " << *l << "\n";
  }

  /* We handle only cases where the last BasicBlock has a return instruction.
   * --mergereturn takes care of this. TODO confirm this. */
  if (i.getNumSuccessors() != 0) {
    throw std::logic_error("Function has multiple return statements \n");
  }

  bool allArgsReadOnlyAndNoCapture = true;
  for (auto argIterator = currentFunction->arg_begin();
       argIterator != currentFunction->arg_end(); argIterator++) {
    allArgsReadOnlyAndNoCapture &=
        argIterator->hasNoCaptureAttr() && argIterator->onlyReadsMemory();
  }

  outs() << "[handleReturnInst]"
         << "allArgsReadOnlyAndNoCapture: " << allArgsReadOnlyAndNoCapture
         << "\n";
  outs() << "[handleReturnInst]"
         << "mostRecentMemoryDef: " << *mostRecentMemoryDef << "\n";

  /* void foo(some_type* a) */
  if (functionReturnsVoid) {
    outs() << "[handleReturnInst]"
           << "Function returns void\n";
    if (functionHasPointerArguments(*currentFunction)) {
      FunctionEncoder::handleReturnInstPointerArgs(i);
    }
    return;
  } else {
    throw std::runtime_error("Function has non-void return type \n");
  }
}

/* TODO only handling unsigned predicates now, add signed */
void FunctionEncoder::handleICmpInst(ICmpInst &i) {
  outs() << "[handleICmpInst]\n";
  auto BBAsstVecIter = BBAssertionsMap.find(currentBB);

  Value *lhs = i.getOperand(0);
  Value *rhs = i.getOperand(1);
  Value *res = dyn_cast<Value>(&i);

  CmpInst::Predicate pred = i.getPredicate();

  auto z3_exp_lhs = BitVecHelper::getBitVecSingValType(lhs);
  auto z3_exp_rhs = BitVecHelper::getBitVecSingValType(rhs);
  auto z3_exp_res = BitVecHelper::getBitVecSingValType(res);

  z3::expr z3_exp_pred(ctx);

  if (pred == CmpInst::ICMP_UGT) {
    z3_exp_pred = z3::ugt(z3_exp_lhs, z3_exp_rhs);
  } else if (pred == CmpInst::ICMP_UGE) {
    z3_exp_pred = z3::uge(z3_exp_lhs, z3_exp_rhs);
  } else if (pred == CmpInst::ICMP_ULT) {
    z3_exp_pred = z3::ult(z3_exp_lhs, z3_exp_rhs);
  } else if (pred == CmpInst::ICMP_ULE) {
    z3_exp_pred = z3::ule(z3_exp_lhs, z3_exp_rhs);
  } else if (pred == CmpInst::ICMP_SGT) {
    z3_exp_pred = (z3_exp_lhs > z3_exp_rhs);
  } else if (pred == CmpInst::ICMP_SGE) {
    z3_exp_pred = (z3_exp_lhs >= z3_exp_rhs);
  } else if (pred == CmpInst::ICMP_SLT) {
    z3_exp_pred = z3::slt(z3_exp_lhs, z3_exp_rhs);
  } else if (pred == CmpInst::ICMP_SLE) {
    z3_exp_pred = z3::sle(z3_exp_lhs, z3_exp_rhs);
  } else if (pred == CmpInst::ICMP_NE) {
    z3_exp_pred = z3_exp_lhs != z3_exp_rhs;
  } else if (pred == CmpInst::ICMP_EQ) {
    z3_exp_pred = z3_exp_lhs == z3_exp_rhs;
  } else {
    throw std::invalid_argument(
        "[handleICmpInst] Unsupported icmp predicate \n");
  }
  z3::expr ICMPExpr = z3::ite(z3_exp_pred, z3_exp_res == 1, z3_exp_res == 0);
  outs() << "[handleICmpInst] " << ICMPExpr.to_string().c_str() << "\n";
  BBAsstVecIter->second.push_back(ICMPExpr);
  printBBAssertionsMap();
}

void FunctionEncoder::handleSelectInst(SelectInst &i) {
  outs() << "[handleSelectInst]\n";

  auto BBAsstVecIter = BBAssertionsMap.find(currentBB);
  Value *res = dyn_cast<Value>(&i);

  auto z3_exp_sel_op1 = BitVecHelper::getBitVecSingValType(i.getOperand(0));
  auto z3_exp_sel_op2 = BitVecHelper::getBitVecSingValType(i.getOperand(1));
  auto z3_exp_sel_op3 = BitVecHelper::getBitVecSingValType(i.getOperand(2));
  auto z3_exp_res = BitVecHelper::getBitVecSingValType(res);

  outs() << "[handleSelectInst] z3_exp_sel_op1: " << z3_exp_sel_op1.to_string()
         << "\n";
  outs() << "[handleSelectInst] z3_exp_sel_op2: " << z3_exp_sel_op2.to_string()
         << "\n";
  outs() << "[handleSelectInst] z3_exp_sel_op3: " << z3_exp_sel_op3.to_string()
         << "\n";
  outs() << "[handleSelectInst] z3_exp_res: " << z3_exp_res.to_string() << "\n";
  outs().flush();
  z3::expr selectEncoding =
      (z3::ite((z3_exp_sel_op1 == 1), (z3_exp_res == z3_exp_sel_op2),
               (z3_exp_res == z3_exp_sel_op3)));
  outs() << "[handleSelectInst]" << selectEncoding.to_string().c_str() << "\n";

  BBAsstVecIter->second.push_back(selectEncoding);
}

void FunctionEncoder::handleBranchInst(BranchInst &i) {
  outs() << "[handleBranchInst] "
         << "EdgeAssertionsMap:\n";
  printEdgeAssertionsMap();
  outs() << "[handleBranchInst] "
         << "PathConditionsMap:\n";
  printPathConditionsMap();

  if (i.isConditional()) {
    outs() << "[handleBranchInst] "
           << " conditional branch \n";

    /* Support only 2 successors for a conditional branch */
    assert(i.getNumSuccessors() == 2);

    z3::expr cond = BitVecHelper::getBitVecSingValType(i.getCondition());
    outs() << i.getNumSuccessors() << "\n";
    BasicBlock *destBB1 = i.getSuccessor(0);
    BasicBlock *destBB2 = i.getSuccessor(1);

    /* Create new path conditions for each destination BB */
    z3::expr newPathCond1 = (cond == 1);
    z3::expr newPathCond2 = (cond == 0);

    /* If there exists a path condition for currentBB, conjunct it*/
    if (pathConditionsMap.find(currentBB) != pathConditionsMap.end()) {
      newPathCond1 = (newPathCond1 && pathConditionsMap.at(currentBB));
      newPathCond2 = (newPathCond2 && pathConditionsMap.at(currentBB));
    }

    /* First update EdgeAssertionsMap */
    BBPair BBPair1 = std::make_pair(currentBB, destBB1);
    BBPair BBPair2 = std::make_pair(currentBB, destBB2);
    assert(EdgeAssertionsMap.find(BBPair1) == EdgeAssertionsMap.end());
    assert(EdgeAssertionsMap.find(BBPair2) == EdgeAssertionsMap.end());
    EdgeAssertionsMap.insert({BBPair1, newPathCond1});
    EdgeAssertionsMap.insert({BBPair2, newPathCond2});

    /* Now update PathConditionsMap. If there exists a path condition for the
     * destBB disjunct it and finally, update pathConditionsMap */
    auto PCIter1 = pathConditionsMap.find(destBB1);
    if (PCIter1 != pathConditionsMap.end()) {
      newPathCond1 = (newPathCond1 || pathConditionsMap.at(destBB1));
      PCIter1->second = newPathCond1;
    } else {
      pathConditionsMap.insert({destBB1, newPathCond1});
    }
    auto PCIter2 = pathConditionsMap.find(destBB2);
    if (PCIter2 != pathConditionsMap.end()) {
      newPathCond2 = (newPathCond2 || pathConditionsMap.at(destBB2));
      PCIter2->second = newPathCond2;
    } else {
      pathConditionsMap.insert({destBB2, newPathCond2});
    }

    outs() << "[handleBranchInst] " << destBB1->getName() << ": "
           << pathConditionsMap.at(destBB1).to_string().c_str() << "\n";
    outs() << "[handleBranchInst] " << destBB2->getName() << ": "
           << pathConditionsMap.at(destBB2).to_string().c_str() << "\n";
    outs() << "[handleBranchInst] "
           << "<" << BBPair1.first->getName() << ", "
           << BBPair1.second->getName()
           << "> :" << EdgeAssertionsMap.at(BBPair1).to_string().c_str()
           << "\n";
    outs() << "[handleBranchInst] "
           << "<" << BBPair2.first->getName() << ", "
           << BBPair2.second->getName()
           << "> :" << EdgeAssertionsMap.at(BBPair2).to_string().c_str()
           << "\n";

  } else {
    outs() << "[handleBranchInst] "
           << "unconditional branch \n";
    BasicBlock *destBB = i.getSuccessor(0);
    outs() << "[handleBranchInst] "
           << "destBB: " << destBB->getName() << "\n";

    /* TODO should this be "true" here?  */
    z3::expr newPathCond(ctx);
    if (pathConditionsMap.find(currentBB) == pathConditionsMap.end()) {
      newPathCond = ctx.bool_val(true);
    } else {
      newPathCond = pathConditionsMap.at(currentBB);
    }
    outs() << "[handleBranchInst] "
           << "newPathCond: " << newPathCond.to_string().c_str() << "\n";

    /* Update EdgeAssertionsMap */
    BBPair currentBBPair = std::make_pair(currentBB, destBB);
    assert(EdgeAssertionsMap.find(currentBBPair) == EdgeAssertionsMap.end());
    EdgeAssertionsMap.insert({currentBBPair, newPathCond});

    /* Update pathConditionsMap*/
    auto PCIter = pathConditionsMap.find(destBB);
    if (PCIter != pathConditionsMap.end()) {
      newPathCond = (newPathCond || pathConditionsMap.at(destBB));
      PCIter->second = newPathCond;
    } else {
      pathConditionsMap.insert({destBB, newPathCond});
    }
    outs() << "[handleBranchInst] " << destBB->getName() << ": "
           << pathConditionsMap.at(destBB).to_string().c_str() << "\n";
    outs() << "[handleBranchInst] "
           << "<" << currentBBPair.first->getName() << ", "
           << currentBBPair.second->getName()
           << "> :" << EdgeAssertionsMap.at(currentBBPair).to_string().c_str()
           << "\n";
  }
}

/* In the first pass, just create a bitvector for this Value. In the second
 * pass, figure out the path conditions */
void FunctionEncoder::handlePhiNode(PHINode &inst, int passID) {
  outs() << "[handlePhiNode]\n";
  if (passID == 1) {
    outs() << "[handlePhiNode] "
           << "Pass #" << passID << "\n";
    Value *res = dyn_cast<Value>(&inst);
    auto res_bv = BitVecHelper::getBitVecSingValType(res);
    outs() << "[handlePhiNode] " << res_bv.to_string().c_str() << "\n";
  } else if (passID == 3) {
    outs() << "[handlePhiNode] "
           << "Pass #" << passID << "\n";
    auto BBAsstVecIter = BBAssertionsMap.find(currentBB);
    Value *res = dyn_cast<Value>(&inst);
    auto res_bv = BitVecHelper::getBitVecSingValType(res);
    outs() << "[handlePhiNode] " << res_bv.to_string().c_str() << "\n";

    for (auto i = 0; i < inst.getNumIncomingValues(); i++) {
      Value *valI = inst.getIncomingValue(i);
      auto valI_bv = BitVecHelper::getBitVecSingValType(valI);
      outs() << "[handlePhiNode] "
             << "valI_bv:" << valI_bv.to_string().c_str() << "\n";
      BasicBlock *incomingBlockI = inst.getIncomingBlock(i);
      outs() << "[handlePhiNode] "
             << "incomingBlockI " << incomingBlockI->getName() << "\n";
      BBPair BBPairI = std::make_pair(incomingBlockI, currentBB);
      if (EdgeAssertionsMap.find(BBPairI) == EdgeAssertionsMap.end()) {
        throw std::runtime_error(
            "<incomingBlock, currentBB> pair not found in EdgeAssertionsMap\n");
      }
      z3::expr phiResolveI =
          z3::implies(EdgeAssertionsMap.at(BBPairI), res_bv == valI_bv);
      outs() << "[handlePhiNode] " << phiResolveI.to_string().c_str() << "\n";
      BBAsstVecIter->second.push_back(phiResolveI);
    }
  }
}

/*
GEP instructions are only used to update the GEPMap, which stores the base type
pointer of the GEP, and offset operands. Every GEP is resolved to be associated
with an offset into a pointer that is a function argument (like a
struct.bpf_reg_state* dst_reg). If the GEP pointer is not a function argument,
then it better be derived from a function argument (eg. struct.tnum* var_off
derived from dst_reg).

%i = getelementptr inbounds %struct.bpf_reg_state, %struct.bpf_reg_state*
%dst_reg, i64 0, i32 5, i32 0

Here, we store {%i: [%dst_reg, 5, 0]} in the GEPMap.

%j = getelementptr inbounds %struct.tnum, %struct.tnum* %dst_reg, i64 0, i32 5
%k = getelementptr inbounds %struct.tnum, %struct.tnum* %j, i64 0, i32 1

For the above two instructions we store, {%j: [%dst_reg, 5]}, and {%k:
[%dst_reg, 5, 1]} in the GEPMap respectively. Essentially, all GEP's have been
resolved to offset into dst_reg. 

*/
void FunctionEncoder::handleGEPInst(GetElementPtrInst &i) {
  outs() << "[handleGEPInst] "
         << "\n";
  Value *resVal = dyn_cast<Value>(&i);
  outs() << "[handleGEPInst] "
         << "resVal:" << *resVal << "\n";
  Value *argVal = i.getOperand(0);
  outs() << "[handleGEPInst] "
         << "argVal: " << *argVal << "\n";
  outs() << "[handleGEPInst] "
         << "getNumOperands:" << i.getNumOperands() << "\n";
  Value *offsetOperandValue = i.getOperand(1);
  outs() << "[handleGEPInst] "
         << "offsetOperandValue:" << *offsetOperandValue << "\n";
  outs().flush();

  /* Assert that the offset operand to GEP, offsets by 0 elements into the base
   * type, i.e offsets the base type directly */
  auto offsetOperandValueInt =
      BitVecHelper::getConstantIntValue(offsetOperandValue);
  assert(offsetOperandValueInt == 0);

  std::vector<int> *GEPIndices = new std::vector<int>;
  ValueIndicesPair valueIndicesPairGEP;

  /* If the GEP is looking into a pointer which isn't a function argument (e.g.
   * dst_reg), then it should be looking at a pointer which has been derived
   * from a function argument (e.g. dst_reg).
   */
  if (FunctionArgs.find(argVal) == FunctionArgs.end()) {
    assert(GEPMap.find(argVal) != GEPMap.end());
    Value *oldGEPMapValue = GEPMap.at(argVal).first;
    std::vector<int> *oldGEPIndices = GEPMap.at(argVal).second;
    for (int i : *oldGEPIndices) {
      GEPIndices->push_back(i);
    }
    valueIndicesPairGEP = std::make_pair(oldGEPMapValue, GEPIndices);
  } else {
    valueIndicesPairGEP = std::make_pair(argVal, GEPIndices);
  }

  GEPMap.insert({resVal, valueIndicesPairGEP});

  if (i.getNumOperands() == 3) {
    int idx;
    /* assume GEP index is 0 if it is not a constant */
    if (BitVecHelper::isValueConstantInt(i.getOperand(2))) {
      idx = BitVecHelper::getConstantIntValue(i.getOperand(2));
    } else {
      idx = 0;
    }
    GEPIndices->push_back(idx);
    outs() << "[handleGEPInst] "
           << "idx: " << idx << "\n";
  } else if (i.getNumOperands() == 4) {
    int idx0, idx1;
    /* assume GEP index is 0 if it is not a constant */
    if (BitVecHelper::isValueConstantInt(i.getOperand(2))) {
      idx0 = BitVecHelper::getConstantIntValue(i.getOperand(2));
    } else {
      idx0 = 0;
    }
    if (BitVecHelper::isValueConstantInt(i.getOperand(3))) {
      idx1 = BitVecHelper::getConstantIntValue(i.getOperand(3));
    } else {
      idx1 = 0;
    }
    GEPIndices->push_back(idx0);
    GEPIndices->push_back(idx1);
    outs() << "[handleGEPInst] "
           << "idx0: " << idx0 << ", idx1: " << idx1 << "\n";
  } else {
    throw std::invalid_argument("Unsupported number of GEP indices\n");
  }

  outs() << "[handleGEPInst] "
         << "MemoryAccessValueBVTreeMap\n";
  printMemoryAccessValueBVTreeMap();
  outs() << "[handleGEPInst] "
         << "GEPMap: \n";
  printGEPMap();
}

void FunctionEncoder::handleLoadInst(LoadInst &i) {
  outs() << "[handleLoadInst] "
         << "\n";
  Value *loadInstValue = dyn_cast<Value>(&i);
  outs() << "[handleLoadInst] "
         << "loadInstValue: " << *loadInstValue << "\n";
  Value *pointerValue = i.getOperand(0);
  outs() << "[handleLoadInst] "
         << "pointerValue: " << *pointerValue << "\n";
  Type *pointerType = pointerValue->getType();
  outs() << "[handleLoadInst] "
         << "pointerType: " << *pointerType << "\n";
  Type *pointerBaseType = pointerType->getPointerElementType();
  outs() << "[handleLoadInst] "
         << "pointerBaseType: " << *pointerBaseType << "\n";
  MemoryAccess *oldMemoryAccess =
      currentMemorySSA->getMemoryAccess(&i)->getDefiningAccess();
  outs() << "[handleLoadInst] "
         << "definingAccess: " << *oldMemoryAccess << "\n";

  /* Loads a pointer to pointer, treat this like a GEP instruction */
  if (pointerBaseType->isPointerTy()) {
    throw std::runtime_error("[handleCallInst]"
                             "load instruction with pointer that is a pointer "
                             "to a pointer is not supported\n");
    return;
  }

  if (loadInstValue->getType()->isAggregateType()) {
    throw std::runtime_error("[handleCallInst]"
                             "load instruction with pointer that is a pointer "
                             "to an aggregate type is not supported\n");
    return;
  }

  outs() << "[handleLoadInst] "
         << "GEPMap:\n";
  printGEPMap();
  z3::expr loadBV = BitVecHelper::getBitVecSingValType(loadInstValue);
  ValueBVTreeMap oldValueBVTreeMap =
      MemoryAccessValueBVTreeMap.at(oldMemoryAccess);
  outs() << "[handleLoadInst] "
         << "oldValueBVTreeMap:\n";
  printValueBVTreeMap(oldValueBVTreeMap);

  Value *GEPMapValue = GEPMap.at(pointerValue).first;
  outs() << "[handleLoadInst] "
         << "GEPMapValue: " << GEPMapValue->getName() << "\n";
  assert(FunctionArgs.find(GEPMapValue) != FunctionArgs.end());

  std::vector<int> *GEPMapIndices = GEPMap.at(pointerValue).second;
  outs() << "[handleLoadInst] "
         << "GEPMapIndices: " << stdVectorIntToString(*GEPMapIndices) << "\n";

  BVTree *parentBVTree = oldValueBVTreeMap.at(GEPMapValue);
  outs() << "[handleLoadInst] "
         << "parentBVTree: " << parentBVTree->toString() << "\n";
  BVTree *subTree;
  if (GEPMapIndices->size() == 1) {
    int idx = GEPMapIndices->at(0);
    subTree = parentBVTree->getSubTree(idx);
  } else if (GEPMapIndices->size() == 2) {
    int idx0 = GEPMapIndices->at(0);
    int idx1 = GEPMapIndices->at(1);
    subTree = parentBVTree->getSubTree(idx0)->getSubTree(idx1);
  } else {
    throw std::runtime_error("Unexpected GEPMapIndices size\n");
  }
  assert(subTree->bv);

  z3::expr loadEncoding = (subTree->bv == loadBV);
  outs() << "[handleLoadInst] " << loadEncoding.to_string().c_str() << "\n";
  auto BBAsstVecIter = BBAssertionsMap.find(currentBB);
  BBAsstVecIter->second.push_back(loadEncoding);
  printBBAssertionsMap();
}

void FunctionEncoder::handleStoreInst(StoreInst &i) {

  /* Syntax:
   * store i64 %value, i64* %dest
   */

  outs() << "[handleStoreInst] "
         << "\n";
  Value *valueStored = i.getValueOperand();
  z3::expr storeBV = BitVecHelper::getBitVecSingValType(valueStored);

  /* get MemoryAccess corresponding to this store */
  MemoryUseOrDef *storeMemoryAccess = currentMemorySSA->getMemoryAccess(&i);
  outs() << "[handleStoreInst] "
         << "storeMemoryAccess: " << *storeMemoryAccess << "\n";
  assert(isa<MemoryDef>(storeMemoryAccess));

  /* Get original MemoryAccess that this store eventually modifies */
  MemoryAccess *oldMemoryAccess = storeMemoryAccess->getDefiningAccess();
  outs() << "[handleStoreInst] "
         << "definingMemoryAccess: " << *oldMemoryAccess << "\n";

  /* Get ValueBVTreeMap corresponding to orignal MemoryAccess */
  ValueBVTreeMap oldValueBVTreeMap =
      MemoryAccessValueBVTreeMap.at(oldMemoryAccess);

  ValueBVTreeMap newValueBVTreeMap;
  /* First copy entire oldValueBVTreeMap to newValueBVTreeMap */
  for (std::pair<Value *, BVTree *> kv : oldValueBVTreeMap) {
    Value *v1 = kv.first;
    BVTree *oldTree = kv.second;
    BVTree *newTree = oldTree->copy();
    newValueBVTreeMap.insert({v1, newTree});
  }
  outs() << "[handleStoreInst] "
         << "newValueBVTreeMap (copied from oldValueBVTreeMap):\n"
         << ValueBVTreeMapToString(newValueBVTreeMap);

  /* Get location where value is stored */
  Value *destPointerValue = i.getPointerOperand();
  outs() << "[handleStoreInst] "
         << "destPointerValue: " << destPointerValue->getName() << "\n";
  outs().flush();

  Value *GEPMapValue = GEPMap.at(destPointerValue).first;
  outs() << "[handleStoreInst] "
         << "GEPMapValue: " << GEPMapValue->getName() << "\n";

  std::vector<int> *GEPMapIndices = GEPMap.at(destPointerValue).second;
  outs() << "[handleStoreInst] "
         << "GEPMapIndices: " << stdVectorIntToString(*GEPMapIndices) << "\n";

  BVTree *parentBVTree = newValueBVTreeMap.at(GEPMapValue);
  BVTree *subTree;
  if (GEPMapIndices->size() == 1) {
    int idx = GEPMapIndices->at(0);
    subTree = parentBVTree->getSubTree(idx);
  } else if (GEPMapIndices->size() == 2) {
    int idx0 = GEPMapIndices->at(0);
    int idx1 = GEPMapIndices->at(1);
    subTree = parentBVTree->getSubTree(idx0)->getSubTree(idx1);
  } else {
    throw std::runtime_error("Unexpected GEPMapIndices size\n");
  }

  outs() << "[handleStoreInst] "
         << "subTree: " << subTree->toString() << "\n";
  assert(subTree->bv);
  subTree->bv = storeBV;
  outs() << "[handleStoreInst] "
         << "subTree updated: " << subTree->toString() << "\n";

  MemoryAccessValueBVTreeMap.insert({storeMemoryAccess, newValueBVTreeMap});
  mostRecentMemoryDef = storeMemoryAccess;
  outs() << "[handleStoreInst] "
         << "MemoryAccessValueBVTreeMap:\n";
  printMemoryAccessValueBVTreeMap();
}

/* Note: variables defined in the given BB are visible from all BBs that are
 * dominated by the given one. */
void FunctionEncoder::handleMemoryPhiNode(MemoryPhi &mphi, int passID) {
  outs() << "[handleMemoryPhiNode] "
         << "Pass #" << passID << "\n";

  mostRecentMemoryDef = &mphi;

  /* In pass 1, we populate phiResolutionMap. */
  if (passID == 1) {

    /* Create new Value:BVTree Map for this MemoryPhi node, and populate it
     * with BVTrees for only those Value(s) which are function arguments. */
    ValueBVTreeMap phiBVTreeMap;

    for (auto argIterator = currentFunction->arg_begin();
         argIterator != currentFunction->arg_end(); argIterator++) {
      Value *argVal = dyn_cast<Value>(argIterator);
      Type *argType = argIterator->getType();
      if (!argType->isPointerTy())
        continue;
      BVTree *BVTreeForArg = setupBVTreeForArg(argVal, argVal->getName().str());
      phiBVTreeMap.insert({argVal, BVTreeForArg});
    }

    outs() << "[handleMemoryPhiNode] "
           << "phiBVTreeMap: "
           << "\n";
    printValueBVTreeMap(phiBVTreeMap);

    /* Iterate over all incoming BasicBlocks to a MemoryPhi block and populate
     * phiResolutionMap. phiResolutionMap contains BBPairs, one pair for each
     * edge incoming to the memoryPhi BasicBlock. Associated to each BBpair is a
     * list of z3 expressions that assert the bitvector equivalences for that
     * particular edge. */
    for (auto i = 0; i < mphi.getNumIncomingValues(); i++) {

      BasicBlock *incomingBBI = mphi.getIncomingBlock(i);
      outs() << "[handleMemoryPhiNode] "
             << "incomingBBI: " << incomingBBI->getName() << "\n";
      BBPair BBPairI = std::make_pair(incomingBBI, currentBB);
      MemoryAccess *incomingAccessI = mphi.getIncomingValue(i);
      outs() << "[handleMemoryPhiNode] "
             << "incomingAccessI: " << *incomingAccessI << "\n";
      ValueBVTreeMap oldVBVTreeMapI =
          MemoryAccessValueBVTreeMap.at(incomingAccessI);
      outs() << "[handleMemoryPhiNode] "
             << "oldVBVTreeMapI: "
             << "\n";
      printValueBVTreeMap(oldVBVTreeMapI);

      z3::expr_vector BBExprsI(ctx);
      phiResolutionMap.insert({BBPairI, BBExprsI});

      for (std::pair<Value *, BVTree *> kv : phiBVTreeMap) {
        Value *argValue = kv.first;
        if (oldVBVTreeMapI.find(argValue) != oldVBVTreeMapI.end()) {
          BVTree *oldTreeArgI = oldVBVTreeMapI.at(argValue);
          outs() << "[handleMemoryPhiNode] "
                 << "oldTreeArgI: " << oldTreeArgI->toString() << "\n";
          BVTree *phiTreeArgI = phiBVTreeMap.at(argValue);
          outs() << "[handleMemoryPhiNode] "
                 << "phiTreeArgI: " << phiTreeArgI->toString() << "\n";
          BVTree::getEquivVector(oldTreeArgI, phiTreeArgI, BBExprsI);
        }
      }
      outs() << "[handleMemoryPhiNode] "
             << "getEquivVector: " << Z3ExprVecToString(BBExprsI) << "\n";
      /* Finally insert the phiBVTreeMap into the global
       * MemoryAccessValueBVTreeMap. */
      MemoryAccessValueBVTreeMap.insert({&mphi, phiBVTreeMap});
    }
    outs() << "[handleMemoryPhiNode] "
           << "PhiResolutionMap:\n";
    printPhiResolutionMap();

    /* In pass 3, we have the path conditions for each BBPair populated in
     * EdgeAssertionsMap. Use them, and the phiResolutionMap, to figure what is
     * the z3 expressions formed as a result of taking the particular edge. */
  } else if (passID == 3) {

    auto BBAsstVecIter = BBAssertionsMap.find(currentBB);

    for (auto i = 0; i < mphi.getNumIncomingValues(); i++) {
      BasicBlock *incomingBBI = mphi.getIncomingBlock(i);
      BBPair BBPairI = std::make_pair(incomingBBI, currentBB);
      assert(EdgeAssertionsMap.find(BBPairI) != EdgeAssertionsMap.end());
      z3::expr_vector BBIExprs = phiResolutionMap.at(BBPairI);
      z3::expr phiResolveI =
          z3::implies(EdgeAssertionsMap.at(BBPairI), z3::mk_and(BBIExprs));
      outs() << "phiResolveI (i=" << i << ") "
             << phiResolveI.to_string().c_str() << "\n";
      BBAsstVecIter->second.push_back(phiResolveI);
    }
  }
}

void FunctionEncoder::handleCallInst(CallInst &i) {
  throw std::runtime_error("[handleCallInst]"
                           "call instruction not supported\n");
}

// ----------------------------------------------------------------------------

/* Go instruction by instruction in the BasicBlock, and build BBAssertionsMap */
void FunctionEncoder::populateBBAssertionsMap(BasicBlock &B) {
  for (Instruction &I : B) {
    FunctionEncoder::currentInstruction = &I;
    outs() << "-------------------\n"
           << I << "\n"
           << "-------------------\n";
    if (I.isDebugOrPseudoInst()) {
      continue;
    }
    if (isa<BinaryOperator>(&I)) {
      handleBinaryOperatorInst(*(dyn_cast<BinaryOperator>(&I)));
    } else if (isa<CastInst>(&I)) {
      handleCastInst(*(dyn_cast<CastInst>(&I)));
    } else if (isa<ICmpInst>(&I)) {
      handleICmpInst(*(dyn_cast<ICmpInst>(&I)));
    } else if (isa<SelectInst>(&I)) {
      handleSelectInst(*(dyn_cast<SelectInst>(&I)));
    } else if (isa<PHINode>(&I)) {
      handlePhiNode(*(dyn_cast<PHINode>(&I)), 1);
    } else if (isa<GetElementPtrInst>(&I)) {
      handleGEPInst(*dyn_cast<GetElementPtrInst>(&I));
    } else if (isa<LoadInst>(&I)) {
      handleLoadInst(*dyn_cast<LoadInst>(&I));
    } else if (isa<StoreInst>(&I)) {
      handleStoreInst(*dyn_cast<StoreInst>(&I));
    } else if (isa<CallInst>(&I)) {
      handleCallInst(*dyn_cast<CallInst>(&I));
    } else {
      outs() << "Unknown instruction. Continuing...\n";
      continue;
    }
  }
}

void FunctionEncoder::populatePathConditionsMap(BasicBlock &B) {
  for (Instruction &I : B) {
    outs() << "-------------------\n"
           << I << "\n"
           << "-------------------\n";
    if (isa<BranchInst>(&I)) {
      handleBranchInst(*(dyn_cast<BranchInst>(&I)));
    } else {
      continue;
    }
  }
}

bool FunctionEncoder::isRelevantStruct(StructType *s) {
  outs() << "[isRelevantStruct] " << *s << "\n";
  if (s->isLiteral()) {
    outs() << "[isRelevantStruct] "
           << "literal struct, this is relevant\n";
    return true;
  }
  std::string structName = s->getStructName().str();
  auto relevant =
      std::find(std::begin(FunctionEncoder::relevantStructs),
                std::end(FunctionEncoder::relevantStructs),
                structName) != std::end(FunctionEncoder::relevantStructs);
  outs() << "[isRelevantStruct] " << structName << " " << relevant << "\n";
  return relevant;
}

/* Recursive function that looks inside structs, and converts them into
 * BVTrees (a tree of bitvectors that mimics the shape of the struct) */
void FunctionEncoder::convertAggregateTypeArgToBVTree(
    BVTree *parent, StructType *baseStructType, std::string prefix) {

  /* Iterate over struct internal members */
  for (auto internalTypeIterator = baseStructType->subtype_begin();
       internalTypeIterator != baseStructType->subtype_end();
       internalTypeIterator++) {
    Type *internalType = *internalTypeIterator;
    outs() << "[convertAggregateTypeArgToBVTree] "
           << "internalType: " << *internalType << "\n";

    while (internalType->isPointerTy()) {
      /* Treat pointers as their base type */
      internalType = internalType->getPointerElementType();
      outs() << "[convertAggregateTypeArgToBVTree] "
             << "internalType (updated): " << *internalType << "\n";
    }

    if (internalType == baseStructType) { /* This is a linked list pointer */
      BVTree *emptyTree = new BVTree();
      parent->children.push_back(emptyTree);
      outs() << "[convertAggregateTypeArgToBVTree] "
             << "pointer to same type, continuing\n";
      continue;
    }

    /* TODO: if array types are need to be supported, change the ifdef to 1.
     * Arrays will also need to be supported in creating JSON dictionaries
     * in getJsonDictFromValueBVTree() and friends. */
    assert(!internalType->isArrayTy());

#if 0
    if (internalType->isArrayTy()) {
      ArrayType *arrayType = dyn_cast<ArrayType>(internalType);
      auto arrayInternalType = arrayType->getElementType();
      outs() << "[convertAggregateTypeArgToBVTree] "
             << "arrayInteralType " << *arrayInternalType << "\n";
      while (arrayInternalType->isPointerTy()) {
        /* treat pointers as their base type */
        arrayInternalType = arrayInternalType->getPointerElementType();
        outs() << "[convertAggregateTypeArgToBVTree] "
               << "argType (updated): " << *arrayInternalType << "\n";
      }

      /* since this is an arrayType, create another BVTree to hold the BVTree
       * for the arrayInternalType, for GEP indexing to work. */
      BVTree *child = new BVTree();
      parent->children.push_back(child);
      if (arrayInternalType->isStructTy()) {
        StructType *arrayInternalStructType =
            dyn_cast<StructType>(arrayInternalType);
        BVTree *grandChild = new BVTree();
        child->children.push_back(grandChild);
        if ((!arrayInternalStructType->isOpaque()) &&
            isRelevantStruct(arrayInternalStructType)) {
          lookInsideStruct(grandChild, arrayInternalStructType, prefix);
        }

      } else if (arrayInternalType->isSingleValueType()) {
        /* internal type is not a struct (i64, i32, etc.) */
        z3::expr inBV =
            BitVecHelper::getBitVec(arrayInternalType->getIntegerBitWidth(), prefix);
        outs() << "[convertAggregateTypeArgToBVTree] "
               << "arrayInternalType is singleValueType:"
               << inBV.to_string().c_str() << "\n";
        BVTree *inBVNode = new BVTree(inBV);
        child->children.push_back(inBVNode);
      }
      continue;
    }
#endif

    if (internalType->isStructTy()) { /* internal type is a struct */
      StructType *internalStructType = dyn_cast<StructType>(internalType);
      BVTree *child = new BVTree();
      parent->children.push_back(child);
      if ((!internalStructType->isOpaque()) &&
          isRelevantStruct(internalStructType)) {
        convertAggregateTypeArgToBVTree(child, internalStructType, prefix);
      }
      continue;
    }

    assert(internalType->isIntegerTy());
    if (internalType->isIntegerTy()) {
      /* internal type is not a struct (i64, i32, etc.) */
      z3::expr inBV =
          BitVecHelper::getBitVec(internalType->getIntegerBitWidth(), prefix);
      outs() << "[lookInsideStruct] "
             << "singleValueType:" << inBV.to_string().c_str() << "\n";
      BVTree *inBVNode = new BVTree(inBV);
      parent->children.push_back(inBVNode);
      continue;
    }
  }
}

#if 0
void FunctionEncoder::flattenArgToBVTree(BVTree *root, Type *argType,
                                         std::string prefix) {
  outs() << "[flattenArgToBVTree] "
         << "argType: " << *argType << "\n";
  if (argType->isPointerTy()) { /* argument is a pointer type */
    /* treat pointers as their base type */
    argType = argType->getPointerElementType();
    outs() << "[flattenArgToBVTree] "
           << "argType (updated): " << *argType << "\n";
  }
  /* Only flatten struct types */
  assert(argType->isStructTy());
  StructType *structArgType = dyn_cast<StructType>(argType);
  if ((!structArgType->isOpaque()) && isRelevantStruct(structArgType)) {
    lookInsideStructForBVTreeSetup(root, structArgType, prefix);
  }
}
#endif

BVTree *FunctionEncoder::setupBVTreeForArg(Value *argVal, std::string prefix) {
  BVTree *BVTreeForArg = new BVTree();
  Type *argType = argVal->getType();
  outs() << "[setupBVTreeForArg] "
         << "argVal: " << *argVal << "\n";
  outs() << "[setupBVTreeForArg] "
         << "argType: " << *argType << "\n";
  if (argType->isIntegerTy()) { /* argument is like i32, i64, etc. */
    outs() << "[setupBVTreeForArg] "
           << "IntegerTy "
           << "\n";
    z3::expr inBV = BitVecHelper::getBitVecSingValType(argVal);
    BVTreeForArg->bv = inBV;
  } else { /* argument is a struct type, array type or pointer to struct type */
    if (argType->isPointerTy()) { /* argument is a pointer type */
      /* treat pointers as their base type */
      argType = argType->getPointerElementType();
      outs() << "[setupBVTreeForArg] "
             << "argType (updated): " << *argType << "\n";
    }
    /* Only flatten struct types */
    if (!argType->isStructTy()) {
      throw std::invalid_argument(
          "[setupBVTreeForArg] argument is not a struct type\n");
    }
    StructType *structArgType = dyn_cast<StructType>(argType);
    if ((!structArgType->isOpaque()) && isRelevantStruct(structArgType)) {
      convertAggregateTypeArgToBVTree(BVTreeForArg, structArgType, prefix);
    }
  }
  outs() << "[setupBVTreeForArg] "
         << "returning BVTree: " << BVTreeForArg->toString() << "\n";
  return BVTreeForArg;
}

/* Main encoding loop: get an encoding of the llvm:Function F's body. Creates a
 * new vector of expressions (z3::expr_vector) and populates the vector with the
 * encoding of F. */
z3::expr_vector FunctionEncoder::encodeFunctionBody(Function &F) {

  /* First pass: populate BBAssertionsMap */
  outs()
      << "<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>\n"
      << "Pass #1: populateBBAssertionsMap\n"
      << "<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>\n";

  for (BasicBlock &BB : F) {
    /* Update current BasicBlock */
    currentBB = &BB;
    /* Make entry for BasicBlock in BBAssertionsMap if it doesn't exist*/
    z3::expr_vector BBAsstVec(ctx);
    if (BBAssertionsMap.find(currentBB) == BBAssertionsMap.end()) {
      BBAssertionsMap.insert({currentBB, BBAsstVec});
    }

    outs() << "=========================\n";
    outs() << currentBB->getName() << "\n";
    outs() << "=========================\n";

    /* check if current BB has a MemoryPhi associated with it*/
    MemoryPhi *memoryPhiCurrentBB =
        currentMemorySSA->getMemoryAccess(currentBB);
    if (memoryPhiCurrentBB) {
      FunctionEncoder::handleMemoryPhiNode(*memoryPhiCurrentBB, 1);
    }

    populateBBAssertionsMap(BB);
  }

  /* Second pass: populate pathConditionsMap */
  outs()
      << "<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>\n"
      << "Pass #2: populatePathConditionsMap\n"
      << "<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>\n";

  for (BasicBlock &BB : F) {
    // Update current BasicBlock
    currentBB = &BB;
    outs() << "================\n";
    outs() << currentBB->getName() << "\n";
    outs() << "================\n";

    /* Nothing really happens to memoryPhiNodes in this pass. This is just a
     * placeholder to maintain the invariant that whenever we are iterating a
     * basicblock, the mostRecentMemoryDef stays updated. */
    MemoryPhi *memoryPhiCurrentBB =
        currentMemorySSA->getMemoryAccess(currentBB);
    if (memoryPhiCurrentBB) {
      FunctionEncoder::handleMemoryPhiNode(*memoryPhiCurrentBB, 2);
    }
    populatePathConditionsMap(BB);
  }

  /* Third pass: FunctionEncoder::handlePhiNodes (including MemoryPhi) */
  outs()
      << "<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>\n"
      << "Pass #3: FunctionEncoder::handlePhiNodes\n"
      << "<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>\n";

  for (BasicBlock &BB : F) {
    currentBB = &BB; // update current BB

    outs() << "================\n";
    outs() << currentBB->getName() << "\n";
    outs() << "================\n";

    /* check if current BB has a MemoryPhi associated with it */
    MemoryPhi *memoryPhiCurrentBB = currentMemorySSA->getMemoryAccess(&BB);
    if (memoryPhiCurrentBB) {
      FunctionEncoder::handleMemoryPhiNode(*memoryPhiCurrentBB, 3);
    }

    for (Instruction &I : BB) {
      if (isa<PHINode>(&I)) {
        outs() << "-------------------\n"
               << I << "\n"
               << "-------------------\n";
        FunctionEncoder::handlePhiNode(*(dyn_cast<PHINode>(&I)), 3);
      }
    }
  }

  outs()
      << "<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>\n"
      << "Pass #4: FunctionEncoder::handleReturnInst\n"
      << "<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>\n";

  for (BasicBlock &BB : F) {
    currentBB = &BB; /* update current BB */
    MemoryPhi *memoryPhiCurrentBB = currentMemorySSA->getMemoryAccess(&BB);
    if (memoryPhiCurrentBB) {
      mostRecentMemoryDef = memoryPhiCurrentBB;
    }
    for (Instruction &I : BB) {
      if (isa<StoreInst>(&I)) {
        mostRecentMemoryDef = currentMemorySSA->getMemoryAccess(&I);
        continue;
      }
      if (isa<ReturnInst>(&I)) {
        FunctionEncoder::handleReturnInst(*(dyn_cast<ReturnInst>(&I)));
      }
    }
  }

  /* Print all global maps */
  outs() << "[encodeFunctionBody] "
         << "BBAssertionsMap:\n";
  printBBAssertionsMap();
  outs() << "[encodeFunctionBody] "
         << "PathConditionsMap:\n";
  printPathConditionsMap();
  outs() << "[encodeFunctionBody] "
         << "EdgeAssertionsMap:\n";
  printEdgeAssertionsMap();
  outs() << "[encodeFunctionBody] "
         << "MemoryAccessValueBVTreeMap:\n";
  printMemoryAccessValueBVTreeMap();

  /* Create final function formula */
  outs()
      << "<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>\n"
      << "Creating formula...\n"
      << "<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>\n";

  z3::expr_vector formula(ctx);
  for (auto KeyValue : BBAssertionsMap) {
    BasicBlock *BB = KeyValue.first;
    z3::expr_vector Z3ExprVec = KeyValue.second;
    /* If the assertions list is empty, likely the bb was composed of just one
     * unconditional jump. Nothing to encode. */
    if (Z3ExprVec.empty()) {
      continue;
    }
    bool pathCondExistsForBB =
        (pathConditionsMap.find(BB) != pathConditionsMap.end());
    if (!pathCondExistsForBB) {
      /* If there are no path conditions for this BB, directly add the list of
       * assertions associated with this BB to the solver (no implications) */
      for (z3::expr assertionExprs : Z3ExprVec) {
        formula.push_back(assertionExprs);
      }
    } else {
      /* If there are path conditions associated with this BasicBlock, add
       * (pathCond) ==> And(assertions)) */
      auto pathCond = pathConditionsMap.at(BB);
      formula.push_back(z3::implies(pathCond, z3::mk_and(Z3ExprVec)));
    }
  }

  return formula;
}

void FunctionEncoder::JsonRecursive(Json::Value *jsonRoot, BVTree *bvTreeRoot,
                                    StructType *baseStructType,
                                    int recursionDepth) {
  outs() << "[JsonRecursive] "
         << "jsonRoot: " << jsonRoot->toStyledString() << "\n";
  outs() << "[JsonRecursive] "
         << "bvTreeRoot: " << bvTreeRoot->toString() << "\n";
  outs() << "[JsonRecursive] "
         << "baseStructType: " << baseStructType->getName() << "\n";
  outs() << "[JsonRecursive] "
         << "recursionDepth: " << recursionDepth << "\n";

  int i = 0;
  for (auto internalTypeIterator = baseStructType->subtype_begin();
       internalTypeIterator != baseStructType->subtype_end();
       internalTypeIterator++) {
    Type *internalType = *internalTypeIterator;
    outs() << "[JsonRecursive] "
           << "internalType: " << *internalType << "\n";

    while (internalType->isPointerTy()) {
      /* treat pointers as their base type */
      internalType = internalType->getPointerElementType();
      outs() << "[JsonRecursive] "
             << "internalType (updated): " << *internalType << "\n";
    }

    if (internalType == baseStructType) { /* this is a linked list pointer */
      jsonRoot->append("");
      outs() << "[JsonRecursive] "
             << "pointer to same type (i.e. linked list), continuing\n";
      continue;
    }

    assert(!internalType->isArrayTy());

    if (internalType->isStructTy()) { /* internal type is a struct */
      StructType *internalStructType = dyn_cast<StructType>(internalType);
      outs() << "[JsonRecursive] "
             << "internalStructType:" << *internalStructType << "\n";
      Json::Value *childJsonValue = new Json::Value(Json::arrayValue);
      if (internalStructType->isOpaque() ||
          (!isRelevantStruct(internalStructType))) {
        outs() << "[JsonRecursive] "
               << "opaque or not relevant\n";
        childJsonValue->append("");
        outs() << "[JsonRecursive] "
               << "childJsonValue:" << childJsonValue->toStyledString() << "\n";
      } else {
        outs() << "[JsonRecursive] "
               << "relevant\n";
        BVTree *childBVTree = bvTreeRoot->getSubTree(i);
        outs() << "[JsonRecursive] "
               << "childBVTree:" << childBVTree->toString() << "\n";
        JsonRecursive(childJsonValue, childBVTree, internalStructType,
                      recursionDepth + 1);
      }
      jsonRoot->append(*childJsonValue);
      outs() << "[JsonRecursive] "
             << "jsonRoot:" << jsonRoot->toStyledString() << "\n";
    } else if (internalType->isIntegerTy()) {
      IntegerType *integerType = dyn_cast<IntegerType>(internalType);
      outs() << "[JsonRecursive] "
             << "isIntegerTy:" << *integerType << "\n";
      /* internal type is not a struct (i64, i32, etc.) */
      BVTree *internalBVTree = bvTreeRoot->getSubTree(i);
      z3::expr bv = internalBVTree->bv;
      outs() << "[JsonRecursive] "
             << "internalBVTree:" << internalBVTree->toString() << "\n";

      auto jsonVal = internalBVTree->bv.to_string() == "null"
                         ? ""
                         : internalBVTree->bv.to_string();
      jsonRoot->append(jsonVal);
      outs() << "[JsonRecursive] "
             << "jsonRoot:" << jsonRoot->toStyledString() << "\n";
    } else {
      throw std::runtime_error("[JsonRecursive] internalType is not a "
                               "struct type or integer type\n");
    }
    i++;
  }
}

/* https://en.wikibooks.org/wiki/JsonCpp */
Json::Value *FunctionEncoder::getJsonDictFromValueBVTree(Value *val,
                                                         BVTree *bvT) {

  Json::Value *jsonRoot = new Json::Value(Json::arrayValue);
  Type *type = val->getType();
  outs() << "[getJsonDictFromValueBVTree] "
         << "type: " << *type << "\n";
  if (type->isIntegerTy()) { /* argument is like i32, i64, etc. */
    outs() << "[getJsonDictFromValueBVTree] "
           << "IntegerTy "
           << "\n";
    jsonRoot->append(bvT->bv.to_string());
    outs() << "[getJsonDictFromValueBVTree] "
           << "jsonRoot:" << jsonRoot->toStyledString() << "\n";
  } else {
    if (type->isPointerTy()) {
      type = type->getPointerElementType();
      outs() << "[getJsonDictFromValueBVTree] "
             << "type (updated): " << *type << "\n";
    }
    if (!type->isStructTy()) {
      throw std::invalid_argument(
          "[getJsonDictFromValueBVTree] not a struct type\n");
    }
    StructType *structType = dyn_cast<StructType>(type);
    if (structType->isOpaque() || (!isRelevantStruct(structType))) {
      jsonRoot->append("");
    } else {
      JsonRecursive(jsonRoot, bvT, structType, 0);
    }
  }
  return jsonRoot;
}

void FunctionEncoder::populateInputAndOutputJsonDict() {

  this->inputJsonDict = new Json::Value(Json::objectValue);
  this->outputJsonDict = new Json::Value(Json::objectValue);

  outs() << "[populateInputAndOutputJsonDict] "
         << "Populating input json dict\n";

  /* Populate input json dict for from inputValueBVTreeMap only considering
   * those Values which were function arguments */
  for (auto argIterator = currentFunction->arg_begin();
       argIterator != currentFunction->arg_end(); argIterator++) {
    Value *argVal = dyn_cast<Value>(argIterator);
    outs() << "[populateInputAndOutputJsonDict] "
           << "argVal: " << *argVal << "\n";

    BVTree *argValInputBVTree = this->inputValueBVTreeMap->find(argVal)->second;
    outs() << "[populateInputAndOutputJsonDict] "
           << "argValInputBVTree: " << argValInputBVTree->toString() << "\n";
    Json::Value *argValJsonInput =
        getJsonDictFromValueBVTree(argVal, argValInputBVTree);
    (*this->inputJsonDict)[argVal->getName().str()] = *argValJsonInput;
  }
  outs() << "[populateInputAndOutputJsonDict] "
         << "Populating output json dict\n";

  /* Populate output json dict directly from outputValueBVTreeMap */
  for (auto ValueBVTreePair : *this->outputValueBVTreeMap) {
    Value *outputVal = ValueBVTreePair.first;
    BVTree *outputBVTree = ValueBVTreePair.second;
    outs() << "[populateInputAndOutputJsonDict] "
           << "outputBVTree: " << outputBVTree->toString() << "\n";
    Json::Value *argValJsonOutput =
        getJsonDictFromValueBVTree(outputVal, outputBVTree);
    (*this->outputJsonDict)[outputVal->getName().str()] = *argValJsonOutput;
  }
}

/* This method implements what the pass does */
void FunctionEncoder::buildSMT() {

  this->mostRecentMemoryDef = this->currentMemorySSA->getLiveOnEntryDef();

  outs()
      << "<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>\n"
      << "Setup input BVTrees \n"
      << "<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>\n";

  this->MemoryAccessValueBVTreeMap.insert(
      {this->mostRecentMemoryDef, *this->inputValueBVTreeMap});
  this->inputValueBVTreeMap =
      &this->MemoryAccessValueBVTreeMap.find(this->mostRecentMemoryDef)->second;
  this->currentBB = &this->currentFunction->getEntryBlock();
  outs() << "[buildSMT] "
         << "currentBB:" << this->currentBB->getName() << "\n";

  /* Create the first entry in BBAssertionsMap for entry BB */
  z3::expr_vector entryBBAsstVec(ctx);
  BBAssertionsMap.insert({this->currentBB, entryBBAsstVec});

  /* Iterate over all arguments of function F and build a
   * MemoryAccessValueBVTreeMap. The only key will be 0 (liveOnEntry). The value
   * in the map will be a vector of BVTrees corresponding to each input argument
   * to this function. */
  for (auto argIterator = this->currentFunction->arg_begin();
       argIterator != this->currentFunction->arg_end(); argIterator++) {
    Value *argVal = dyn_cast<Value>(argIterator);
    BVTree *BVTreeForArg =
        this->setupBVTreeForArg(argVal, argVal->getName().str());
    this->inputValueBVTreeMap->insert({argVal, BVTreeForArg});

    /* For each bitvector b in the BVTree, assert that (b == b) in entryBB's
     * asertions in BBAssertionsMap. This is mostly superflous, but is necessary
     * to have the output SMT contain the bitvectors corresponding to the
     * functions's input. It is particularly necessary when the function has
     * just one basic block (no phi block to merge two blocks using new
     * bitvectors)  */
    BVTreeForArg->addBVSelfEquivalencesToExprVec(entryBBAsstVec);

    /* Add arg to FunctionArgs list */
    this->FunctionArgs.insert(argVal);
  }
  printMemoryAccessValueBVTreeMap();

  if (this->currentFunction->getReturnType()->isVoidTy()) {
    this->functionReturnsVoid = true;
  }

  /* Call encodeFunctionBody to get encoding for function.  */
  this->functionEncodingZ3ExprVec =
      this->encodeFunctionBody(*this->currentFunction);

  outs()
      << "<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>\n"
      << "Finalizing JSON input and output dictionaries...\n"
      << "<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>\n";
  this->populateInputAndOutputJsonDict();

  outs()
      << "<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>\n"
      << "Printing Encoding...\n"
      << "<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>\n";
  outs() << this->toString().c_str();
}