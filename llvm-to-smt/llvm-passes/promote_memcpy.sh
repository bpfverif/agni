#!/bin/bash

if [ $# -ne 4 ]; then
    echo "$0: Usage: promote_memcpy.sh path_to_llvm_file function_to_promote_memcpy output_dir output_filename.ll"
    exit 1
fi

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
source ${SCRIPT_DIR}/.config
PASS_DIR="${BASE_DIR}/PromoteMemcpy"
BUILD_DIR="${PASS_DIR}/build"

oldpwd=$(pwd)
inputllfile=$(readlink -f $1)
function_name=$2
outfile_final_dir=$(readlink -f $3)
outfile_final_name=$4
outfile_final="${outfile_final_dir}/${outfile_final_name}"
echo "outfile_final ${outfile_final}"

echo "--------------------------------------"
echo "build PromoteMemcpy pass"
echo "--------------------------------------"
cmd="mkdir -p ${BUILD_DIR}"
cmd="${cmd} && cd ${BUILD_DIR}"
cmd="${cmd} && export CC=${LLVM_DIR}/bin/clang"
cmd="${cmd} && export CXX=${LLVM_DIR}/bin/clang++"
cmd="${cmd} && cmake -DCMAKE_EXPORT_COMPILE_COMMANDS=1 -DLT_LLVM_INSTALL_DIR=${LLVM_DIR} ${PASS_DIR}"
cmd="${cmd} && make"
echo $cmd
eval $cmd || exit 1

export FUNCTION_TO_PROMOTE_MEMCPY=${function_name}
echo "FUNCTION_TO_PROMOTE_MEMCPY: ${FUNCTION_TO_PROMOTE_MEMCPY}"
echo "--------------------------------------"
echo "running pass promote-memcpy"
echo "--------------------------------------"
cmd="$LLVM_DIR/bin/opt -load-pass-plugin ${BUILD_DIR}/libPromoteMemcpy.so --passes=\"promote-memcpy\" ${inputllfile} -S -o ${outfile_final}"

echo $cmd
eval $cmd || exit 1

echo "--------------------------------------"
echo "done. output file: ${outfile_final}"
echo "--------------------------------------"

