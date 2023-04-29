#!/bin/bash

if [ $# -ne 4 ]; then
    echo "$0: Usage: inline_verifier.sh path_to_llvm_file function_to_start_inline output_dir output_filename.ll"
    exit 1
fi

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
source ${SCRIPT_DIR}/.config
INLINE_FUNCTION_CALLS_PASS_DIR="${BASE_DIR}/InlineFunctionCalls"
BUILD_DIR="${INLINE_FUNCTION_CALLS_PASS_DIR}/build"

oldpwd=$(pwd)
inputllfile=$(readlink -f $1)
function_name=$2
outfile_final_dir=$(readlink -f $3)
outfile_final_name=$4
outfile_final="${outfile_final_dir}/${outfile_final_name}"
echo "outfile_final ${outfile_final}"

echo "--------------------------------------"
echo "build InlineFunctionCalls pass"
echo "--------------------------------------"
cmd="cd ${BUILD_DIR}"
cmd="${cmd} && export CC=${LLVM_DIR}/bin/clang"
cmd="${cmd} && export CXX=${LLVM_DIR}/bin/clang++"
cmd="${cmd} && cmake -DCMAKE_EXPORT_COMPILE_COMMANDS=1 -DLT_LLVM_INSTALL_DIR=${LLVM_DIR} ${INLINE_FUNCTION_CALLS_PASS_DIR}"
cmd="${cmd} && make"
echo $cmd
eval $cmd || exit 1

echo "--------------------------------------"
echo "running pass inline-func-calls"
echo "--------------------------------------"
export FUNCTION_TO_INLINE=$2
echo "FUNCTION_TO_INLINE: ${FUNCTION_TO_INLINE}"

cmd="$LLVM_DIR/bin/opt -load-pass-plugin ${BUILD_DIR}/libInlineFunctionCalls.so --passes=\"inline-func-calls\" ${inputllfile} -S -o ${outfile_final}"

echo $cmd
eval $cmd || exit 1

# cmd="${LLVM_DIR}/bin/opt -S --strip-debug ${outfile_final} -o ${outfile_final}.ll"
# cmd="${cmd} && mv ${outfile_final}.ll ${outfile_final}"

# echo $cmd
# eval $cmd || exit 1

# echo "--------------------------------------"
# echo "running verify pass "
# echo "--------------------------------------"
# cmd="${LLVM_DIR}/bin/opt -S --verify ${outfile_final} -o  ${outfile_final}.ll"
# cmd="${cmd} && mv ${outfile_final}.ll ${outfile_final}"

# echo $cmd
# eval $cmd || exit 1

echo "--------------------------------------"
echo "done. output file: ${outfile_final}"
echo "--------------------------------------"
