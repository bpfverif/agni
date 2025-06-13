#!/bin/bash

if [ $# -ne 5 ]; then
    echo $0: usage: llvm_to_smt.sh input_dir input_file function_name global_bv_suffix output_smt_filename
    exit 1
fi

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
source ${SCRIPT_DIR}/.config
PASS_DIR="${BASE_DIR}/LLVMToSMT"
BUILD_DIR="${PASS_DIR}/build"

oldpwd=$(pwd)
directory=$(readlink -f $1)
inputllfile=$2
outputsmtfile=$5

echo "------------------"
echo "compile llvm-to-smt pass"
echo "------------------"
cmd="mkdir -p ${BUILD_DIR}"
cmd="${cmd} && cd ${BUILD_DIR}"
cmd="${cmd} && CC=${LLVM_DIR}/bin/clang"
cmd="${cmd} && CXX=${LLVM_DIR}/bin/clang++"
cmd="${cmd} && cmake -DCMAKE_EXPORT_COMPILE_COMMANDS=1 -DLT_LLVM_INSTALL_DIR=${LLVM_DIR} ${PASS_DIR}"
cmd="${cmd} && make"
echo $cmd
eval $cmd || exit 1

echo "-------------------------------------------"
echo "cd back"
echo "-------------------------------------------"
cd ${oldpwd}

echo "-------------------------------------------"
echo "running llvm pass on file ${llfile}"
echo "-------------------------------------------"
llfile="${directory}/${inputllfile}"
smtfile="${directory}/${outputsmtfile}"
export SMT2LIB_OUTPUT_FILEPATH=$smtfile
export GLOBAL_BITVECTOR_SUFFIX=$4
export FUNCTION_UNDER_EVAL=$3

echo "SMT2LIB_OUTPUT_FILEPATH: ${SMT2LIB_OUTPUT_FILEPATH}"
echo "FUNCTION_UNDER_EVAL: ${FUNCTION_UNDER_EVAL}"
echo "GLOBAL_BITVECTOR_SUFFIX: ${GLOBAL_BITVECTOR_SUFFIX}"

e="${LLVM_DIR}/bin/opt -load-pass-plugin ${BUILD_DIR}/libLLVMToSMT.so --passes=\"print<llvm-to-smt>\" --disable-output ${llfile}"
echo $e
eval $e || exit 1

echo "-------------------------------------------"
echo "smt2 output file path: ${smtfile}"
echo "-------------------------------------------"
