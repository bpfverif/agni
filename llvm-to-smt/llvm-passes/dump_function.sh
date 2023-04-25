#!/bin/bash

if [ $# -ne 3 ]; then
    echo "$0: Usage: dump_function.sh path_to_llvm_file.ll function_to_dump file_to_dump.ll"
    exit 1
fi

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
source ${SCRIPT_DIR}/.config
DUMP_FUNCTION_PASS_DIR="${BASE_DIR}/DumpFunction"
BUILD_DIR="${DUMP_FUNCTION_PASS_DIR}/build"

oldpwd=$(pwd)

echo "--------------------------------------"
echo "build DumpFunction pass"
echo "--------------------------------------"
cmd="cd ${BUILD_DIR}"
cmd="${cmd} && export CC=${LLVM_DIR}/bin/clang"
cmd="${cmd} && export CXX=${LLVM_DIR}/bin/clang++"
cmd="${cmd} && cmake -DCMAKE_EXPORT_COMPILE_COMMANDS=1 -DLT_LLVM_INSTALL_DIR=${LLVM_DIR} ${DUMP_FUNCTION_PASS_DIR}"
cmd="${cmd} && make"
echo $cmd
eval $cmd || exit 1

echo "--------------------------------------"
echo "running pass to dump function ${FUNCTION_TO_DUMP}"
echo "--------------------------------------"
export FUNCTION_TO_DUMP=$2
export FUNCTION_TO_DUMP_FILE=$3
cmd="cd ${oldpwd}"
cmd="${cmd} && $LLVM_DIR/bin/opt -load-pass-plugin ${BUILD_DIR}/libDumpFunction.so --passes=\"print<dump-function>\" $1 -o /dev/null"

echo $cmd
eval $cmd || exit 1

num_lines=($(wc -l ${FUNCTION_TO_DUMP_FILE}))

echo "--------------------------------------"
echo "done. output file: $3 (${num_lines} lines)."
echo "--------------------------------------"
