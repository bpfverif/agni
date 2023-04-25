#include "BVTree.hpp"

extern z3::context ctx;

BVTree *dummyTree() {
  BVTree *root = new BVTree();

  // first child is a
  z3::expr a = ctx.bv_const("a", 64);
  BVTree *aNode = new BVTree(a);
  root->children.push_back(aNode);

  // second child is b, but has more children
  BVTree *bNode = new BVTree();
  root->children.push_back(bNode);

  // b's chilren are c and d
  // c has more children
  BVTree *cNode = new BVTree();
  bNode->children.push_back(cNode);
  z3::expr d = ctx.bv_const("d", 64);
  BVTree *dNode = new BVTree(d);
  bNode->children.push_back(dNode);

  // c's children are e and f
  z3::expr e = ctx.bv_const("e", 64);
  BVTree *eNode = new BVTree(e);
  cNode->children.push_back(eNode);
  z3::expr f = ctx.bv_const("f", 64);
  BVTree *fNode = new BVTree(f);
  cNode->children.push_back(fNode);

  return root;
}

void toStringTest() {
  // should print: [ a [ [ e f ] d ] ]
  std::cout << dummyTree()->toString() << std::endl;
}

void copyTest() {
  BVTree *oldt = dummyTree();
  BVTree *newt = oldt->copy();
  std::cout << newt->toString() << std::endl;
  z3::expr g = ctx.bv_const("g", 64);
  newt->children[1]->children[0]->children[1]->bv = g;
  std::cout << newt->toString() << std::endl;
  std::cout << oldt->toString() << std::endl;
}

void emptyCopyTest() {
  BVTree *t = dummyTree();
  std::cout << t->toString() << std::endl;
  BVTree *copyt = t->emptyCopy();
  std::cout << copyt->toString() << std::endl;
}

void mergeTest() {
  BVTree *treea = dummyTree();
  BVTree *treeb = treea->copy();
  z3::expr g = ctx.bv_const("g", 64);
  z3::expr h = ctx.bv_const("h", 64);
  treeb->children[1]->children[0]->children[1]->bv = g;
  treeb->children[1]->children[0]->children[0]->bv = h;
  std::cout << treea->toString() << std::endl;
  std::cout << treeb->toString() << std::endl;
  z3::expr_vector gv(ctx);
  z3::expr_vector hv(ctx);
  BVTree *merget = BVTree::merge(treea, treeb, gv, hv);
  std::cout << merget->toString() << std::endl;
  std::cout << gv << std::endl;
  std::cout << hv << std::endl;
}

void subTreeTest() {
  BVTree *treea = dummyTree();
  std::cout << treea->toString() << std::endl;
  BVTree *subtree0 = treea->getSubTree(0);
  std::cout << subtree0->toString() << std::endl;
  BVTree *subtree1 = treea->getSubTree(1);
  std::cout << subtree1->toString() << std::endl;
  BVTree *subtree10 = subtree1->getSubTree(0);
  std::cout << subtree10->toString() << std::endl;
  BVTree *subtree11 = subtree1->getSubTree(1);
  std::cout << subtree11->toString() << std::endl;
  BVTree *subtree101 = subtree10->getSubTree(0);
  std::cout << subtree101->toString() << std::endl;
  BVTree *subtree102 = subtree10->getSubTree(1);
  std::cout << subtree102->toString() << std::endl;
}

void replaceTest() {
  BVTree *treea = dummyTree();
  std::cout << treea->toString() << std::endl;
  z3::expr oldbv = treea->children[0]->bv;
  BVTree *treeb = treea->copy();
  z3::expr newbv = ctx.bv_const("newbv", 64);
  treeb->replaceBV(oldbv, newbv);
  std::cout << treeb->toString() << std::endl;
  z3::expr oldbv2 = treea->children[1]->children[1]->bv;
  treeb->replaceBV(oldbv2, newbv);
  std::cout << treeb->toString() << std::endl;
}

void getOutputEquivalenceZ3ExprVectorTest() {
  BVTree *treea = dummyTree();
  std::cout << treea->toString() << std::endl;
  std::cout << treea->getOutputEquivalenceZ3ExprVector() << std::endl;
}


void deepCopyTest() {
  BVTree *treeOld = dummyTree();
  BVTree *treeNew = treeOld->deepCopy();
  std::cout << treeOld->toString() << std::endl;
  std::cout << treeNew->toString() << std::endl;
}

void getEquivVectorTest() {
  BVTree *treeOld = dummyTree();
  BVTree *treeNew = treeOld->deepCopy();
  std::cout << treeOld->toString() << std::endl;
  std::cout << treeNew->toString() << std::endl;
  z3::expr_vector v(ctx);
  BVTree::getEquivVector(treeOld, treeNew, v);
  std::cout << v << std::endl;
}

void setAllBVsToValueTest(){
  BVTree *treeOld = dummyTree();
  std::cout << treeOld->toString() << std::endl;;
  treeOld->setAllBVsToValue(0);
  std::cout << treeOld->toString() << std::endl;;
}

void setAllBVsUntilIndexToValueTest(){
  BVTree *treeOld = dummyTree();
  std::cout << treeOld->toString() << std::endl;;
  treeOld->setAllBVsUntilIndexToValue(1, 2, 0);
  std::cout << treeOld->toString() << std::endl;;
}

int main() {
  std::cout << "++++++++++++++++++\n";
  std::cout << "toStringTest\n";
  std::cout << "++++++++++++++++++" << std::endl;
  toStringTest();

  std::cout << "++++++++++++++++++\n";
  std::cout << "copyTest\n";
  std::cout << "++++++++++++++++++" << std::endl;
  copyTest();

  std::cout << "++++++++++++++++++\n";
  std::cout << "emptyCopyTest\n";
  std::cout << "++++++++++++++++++" << std::endl;
  emptyCopyTest();

  std::cout << "++++++++++++++++++\n";
  std::cout << "mergeTest\n";
  std::cout << "++++++++++++++++++" << std::endl;
  mergeTest();

  std::cout << "++++++++++++++++++\n";
  std::cout << "subTreeTest\n";
  std::cout << "++++++++++++++++++" << std::endl;
  subTreeTest();

  std::cout << "++++++++++++++++++\n";
  std::cout << "replaceTest\n";
  std::cout << "++++++++++++++++++" << std::endl;
  replaceTest();

  std::cout << "++++++++++++++++++\n";
  std::cout << "getOutputEquivalenceZ3ExprVectorTest\n";
  std::cout << "++++++++++++++++++" << std::endl;
  getOutputEquivalenceZ3ExprVectorTest();

  std::cout << "++++++++++++++++++\n";
  std::cout << "deepCopyTest\n";
  std::cout << "++++++++++++++++++" << std::endl;
  deepCopyTest();

  std::cout << "++++++++++++++++++\n";
  std::cout << "getEquivVectorTest\n";
  std::cout << "++++++++++++++++++" << std::endl;
  getEquivVectorTest();

  std::cout << "++++++++++++++++++\n";
  std::cout << "setAllBVsToValueTest\n";
  std::cout << "++++++++++++++++++" << std::endl;
  setAllBVsToValueTest();

  std::cout << "++++++++++++++++++\n";
  std::cout << "setAllBVsUntilIndexToValueTest\n";
  std::cout << "++++++++++++++++++" << std::endl;
  setAllBVsUntilIndexToValueTest();

  return 0;
}