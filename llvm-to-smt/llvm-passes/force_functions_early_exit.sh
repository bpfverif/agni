#!/bin/bash

if [ $# -ne 3 ]; then
    echo "$0: Usage: force_functions_early_exit.sh path_to_llvm_file output_dir output_filename.ll"
    exit 1
fi

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
source ${SCRIPT_DIR}/.config
PASS_DIR="${BASE_DIR}/ForceFunctionEarlyExit"
BUILD_DIR="${PASS_DIR}/build"

oldpwd=$(pwd)
inputllfile=$(readlink -f $1)
outfile_final_dir=$(readlink -f $2)
outfile_final_name=$3
outfile_final="${outfile_final_dir}/${outfile_final_name}"
functions_retvalue_map="${PASS_DIR}/config.json"

echo "--------------------------------------"
echo "build ForceFunctionEarlyExit pass"
echo "--------------------------------------"
cmd="mkdir -p ${BUILD_DIR}"
cmd="${cmd} && cd ${BUILD_DIR}"
cmd="${cmd} && export CC=${LLVM_DIR}/bin/clang"
cmd="${cmd} && export CXX=${LLVM_DIR}/bin/clang++"
cmd="${cmd} && cmake -DCMAKE_EXPORT_COMPILE_COMMANDS=1 -DLT_LLVM_INSTALL_DIR=${LLVM_DIR} ${PASS_DIR}"
cmd="${cmd} && make"
echo $cmd
eval $cmd || exit 1

echo "--------------------------------------"
echo "running pass force-function-early-exit"
echo "--------------------------------------"
export FUNCTIONS_EARLY_RETVALUE_MAP_TXT=$functions_retvalue_map
echo "FUNCTIONS_EARLY_RETVALUE_MAP_TXT: ${FUNCTIONS_EARLY_RETVALUE_MAP_TXT}"

cmd="$LLVM_DIR/bin/opt -load-pass-plugin ${BUILD_DIR}/libForceFunctionEarlyExit.so --passes=\"force-function-early-exit\" ${inputllfile} -S -o ${outfile_final}"
cmd="${cmd} && $LLVM_DIR/bin/opt --verify ${outfile_final} -S -o ${outfile_final}.ll"
cmd="${cmd} && mv ${outfile_final}.ll ${outfile_final}"

echo $cmd
eval $cmd || exit 1

echo "--------------------------------------"
echo "done. output file: ${outfile_final}"
echo "--------------------------------------"

