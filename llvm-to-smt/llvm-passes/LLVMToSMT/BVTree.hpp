#ifndef LLVM2SMT_BVTREE_H
#define LLVM2SMT_BVTREE_H

#include "BitvecHelper.hpp"
#include "z3++.h"
#include <z3_api.h>
#include <cassert>
#include <sstream>
#include <vector>

extern z3::context ctx;

class BVTree {
public:
  z3::expr bv;
  std::vector<BVTree *> children;

  BVTree();
  BVTree(z3::expr &bv_);
  std::string toString();
  BVTree *copy();
  BVTree *emptyCopy();
  static BVTree *merge(BVTree *, BVTree *, z3::expr_vector &,
                       z3::expr_vector &);
  BVTree *getSubTree(int idx);
  void replaceBV(unsigned int oldbv_ast_id, z3::expr &newbv);
  z3::expr_vector getOutputEquivalenceZ3ExprVector();
  BVTree *deepCopy();
  static void getEquivVector(BVTree *, BVTree *, z3::expr_vector &);
  void setAllBVsUntilIndexToValue(int, int, int);
  void setAllBVsToValue(int);
  bool hasSubTree();
  void addBVSelfEquivalencesToExprVec(z3::expr_vector &v);

private:
  std::ostringstream toString_();
  static void merge(BVTree *, BVTree *, BVTree *, z3::expr_vector &,
                    z3::expr_vector &);
  void deepCopy(BVTree *);
  void getOutputEquivalenceZ3ExprVector(z3::expr_vector &);
  
};

#endif // LLVM2SMT_BVTREE_H