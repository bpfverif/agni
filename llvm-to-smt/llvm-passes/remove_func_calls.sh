#!/bin/bash

if [ $# -ne 4 ]; then
    echo "$0: Usage: remove_func_calls.sh path_to_llvm_file function_to_start_remove output_dir output_filename.ll"
    exit 1
fi

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
source ${SCRIPT_DIR}/.config
PASS_DIR="${BASE_DIR}/RemoveFunctionCalls"
BUILD_DIR="${PASS_DIR}/build"

oldpwd=$(pwd)
inputllfile=$(readlink -f $1)
functiontostart=$2
outfile_final_dir=$(readlink -f $3)
outfile_final_name=$4
outfile_final="${outfile_final_dir}/${outfile_final_name}"

functions_json="${PASS_DIR}/config.json"

echo "--------------------------------------"
echo "build RemoveFunctionCalls pass"
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
echo "running pass remove-func-calls"
echo "--------------------------------------"
export FUNCTIONS_TO_REMOVE_TXT=${functions_json}
export FUNCTION_TO_START_REMOVE=${functiontostart}
echo "FUNCTIONS_TO_REMOVE_TXT: ${FUNCTIONS_TO_REMOVE_TXT}"
echo "FUNCTION_TO_START_REMOVE: ${FUNCTION_TO_START_REMOVE}"

cmd="$LLVM_DIR/bin/opt -load-pass-plugin ${BUILD_DIR}/libRemoveFunctionCalls.so --passes=\"remove-func-calls\" ${inputllfile} -S -o ${outfile_final}"

echo $cmd
eval $cmd || exit 1

# echo "--------------------------------------"
# echo "running --instnamer, --verify, and --strip-debug pass "
# echo "--------------------------------------"
# cmd="${LLVM_DIR}/bin/opt -S --instnamer --strip-debug --verify $2 -o  $2.ll"
# cmd="${cmd} && mv $2.ll $2"

# echo $cmd
# eval $cmd || exit 1

echo "--------------------------------------"
echo "done. output file: ${outfile_final}"
echo "--------------------------------------"
