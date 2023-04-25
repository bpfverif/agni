#include "BVTree.hpp"

BVTree::BVTree() : bv(z3::expr(ctx)), children(std::vector<BVTree *>()) {}
BVTree::BVTree(z3::expr &bv_) : bv(bv_), children(std::vector<BVTree *>()) {}

std::ostringstream BVTree::toString_() {
  std::ostringstream os;
  os << "[ ";
  if (this->bv) {
    os << this->bv << " ";
  } else {
    for (BVTree *c : this->children) {
      os << c->toString_().str();
    }
  }
  os << "] ";
  return os;
}

std::string BVTree::toString() { return this->toString_().str(); }

BVTree *BVTree::copy() {
  BVTree *newT = new BVTree(this->bv);
  if (this->children.empty()) {
    return newT;
  } else {
    for (BVTree *childT : this->children) {
      newT->children.push_back(childT->copy());
    }
    return newT;
  }
}

BVTree *BVTree::emptyCopy() {
  BVTree *newT = new BVTree();
  if (this->children.empty()) {
    return newT;
  } else {
    for (BVTree *childT : this->children) {
      newT->children.push_back(childT->emptyCopy());
    }
    return newT;
  }
}

void BVTree::merge(BVTree *t1, BVTree *t2, BVTree *tMerge, z3::expr_vector &v1,
                   z3::expr_vector &v2) {
  if (t1->children.empty()) {
    if (Z3_get_ast_id(ctx, t1->bv) == Z3_get_ast_id(ctx, t2->bv)) {
      tMerge->bv = t1->bv;
    } else {
      tMerge->bv = BitVecHelper::getBitVec(t1->bv.get_sort().bv_size());
      v1.push_back(t1->bv == tMerge->bv);
      v2.push_back(t2->bv == tMerge->bv);
    }
  } else {
    for (auto i = 0; i < t1->children.size(); i++) {
      BVTree *aChildI = t1->children[i];
      BVTree *bChildI = t2->children[i];
      BVTree *nChildI = tMerge->children[i];
      merge(aChildI, bChildI, nChildI, v1, v2);
    }
  }
}

BVTree *BVTree::merge(BVTree *t1, BVTree *t2, z3::expr_vector &v1,
                      z3::expr_vector &v2) {
  BVTree *tMerge = t1->emptyCopy();
  BVTree::merge(t1, t2, tMerge, v1, v2);
  return tMerge;
}

void BVTree::deepCopy(BVTree *tNew) {
  if (this->children.empty()) {
    tNew->bv = BitVecHelper::getBitVec(this->bv.get_sort().bv_size());
  } else {
    for (auto i = 0; i < this->children.size(); i++) {
      BVTree *t1ChildI = this->children[i];
      BVTree *t2ChildT = tNew->children[i];
      t1ChildI->deepCopy(t2ChildT);
    }
  }
}

BVTree *BVTree::deepCopy() {
  BVTree *tNew = this->emptyCopy();
  BVTree::deepCopy(tNew);
  return tNew;
}

bool BVTree::hasSubTree() { return (this->children.size() > 0); }

BVTree *BVTree::getSubTree(int idx) {
  assert(this->children.size() > idx);
  return this->children[idx];
}

void BVTree::replaceBV(unsigned int oldbv_ast_id, z3::expr &newbv) {
  if (this->bv) {
    if (Z3_get_ast_id(ctx, this->bv) == oldbv_ast_id) {
      outs() << "[replaceBV] replaced: " << this->bv.to_string();
      this->bv = newbv;
      outs() << " with " << this->bv.to_string() << "\n";
      return;
    }
  }
  for (BVTree *c : this->children) {
    c->replaceBV(oldbv_ast_id, newbv);
  }
}

void BVTree::setAllBVsToValue(int value) {
  if (this->bv) {
    this->bv = ctx.bv_val(value, this->bv.get_sort().bv_size());
    return;
  }
  for (auto i = 0; i < this->children.size(); i++) {
    BVTree *subTree = getSubTree(i);
    subTree->setAllBVsToValue(value);
  }
}

void BVTree::setAllBVsUntilIndexToValue(int startidx, int endidx, int value) {
  if (this->bv) {
    this->bv = ctx.bv_val(value, this->bv.get_sort().bv_size());
    return;
  }
  for (auto i = startidx; i < endidx; i++) {
    auto subTree = this->getSubTree(i);
    subTree->setAllBVsToValue(value);
  }
}

void BVTree::getEquivVector(BVTree *t1, BVTree *t2, z3::expr_vector &v) {
  if (t1->children.empty()) {
    assert(t2->children.empty());
    /* If both trees nodes don't contain children, then BOTH the nodes
     * themselves should either contain bitvectors, or not contain bitvectors.
     */
    bool t1hasBV = bool(t1->bv);
    bool t2hasBV = bool(t2->bv);
    if (t1hasBV && t2hasBV) {
      v.push_back(t1->bv == t2->bv);
    } else {
      /* BVTrees are not equivalent in shape */
      assert(!t1hasBV && !t2hasBV);
    }
  } else {
    for (auto i = 0; i < t1->children.size(); i++) {
      BVTree *t1childI = t1->children[i];
      BVTree *t2childI = t2->children[i];
      getEquivVector(t1childI, t2childI, v);
    }
  }
}

void BVTree::getOutputEquivalenceZ3ExprVector(z3::expr_vector &v) {
  if (this->bv) {
    z3::expr outBV =
        BitVecHelper::getBitVec(this->bv.get_sort().bv_size(), "out");
    v.push_back(outBV == this->bv);
  }
  for (BVTree *c : this->children) {
    c->getOutputEquivalenceZ3ExprVector(v);
  }
}

z3::expr_vector BVTree::getOutputEquivalenceZ3ExprVector() {
  z3::expr_vector v(ctx);
  BVTree::getOutputEquivalenceZ3ExprVector(v);
  return v;
}

void BVTree::addBVSelfEquivalencesToExprVec(z3::expr_vector &v) {
  if (this->bv) {
    v.push_back(this->bv == this->bv);
  }
  for (BVTree *c : this->children) {
    c->addBVSelfEquivalencesToExprVec(v);
  }
}