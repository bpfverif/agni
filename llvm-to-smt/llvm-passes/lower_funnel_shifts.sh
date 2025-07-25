#!/bin/bash

if [ $# -ne 4 ]; then
    echo "$0: Usage: lower_funnel_shifts.sh path_to_llvm_file.ll function_to_lower_funnel_shifts out_dir output_file.ll"
    exit 1
fi

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
source ${SCRIPT_DIR}/.config
PASS_DIR="${BASE_DIR}/LowerFunnelShifts"
BUILD_DIR="${PASS_DIR}/build"

oldpwd=$(pwd)
inputllfile=$(readlink -f $1)
function_name=$2
outfile_final_dir=$(readlink -f $3)
outfile_final_name=$4
outfile_final="${outfile_final_dir}/${outfile_final_name}"
echo "outfile_final ${outfile_final}"

echo "--------------------------------------"
echo "build LowerFunnelShifts pass"
echo "--------------------------------------"
cmd="mkdir -p ${BUILD_DIR}"
cmd="${cmd} && cd ${BUILD_DIR}"
cmd="${cmd} && export CC=${LLVM_DIR}/bin/clang"
cmd="${cmd} && export CXX=${LLVM_DIR}/bin/clang++"
cmd="${cmd} && cmake -DCMAKE_EXPORT_COMPILE_COMMANDS=1 -DLT_LLVM_INSTALL_DIR=${LLVM_DIR} ${PASS_DIR}"
cmd="${cmd} && make"
echo $cmd
eval $cmd || exit 1

export FUNCTION_TO_LOWER_FUNNEL_SHIFTS=${function_name}
echo "FUNCTION_TO_LOWER_FUNNEL_SHIFTS: ${FUNCTION_TO_LOWER_FUNNEL_SHIFTS}"
echo "--------------------------------------"
echo "running pass lower-funnel-shifts"
echo "--------------------------------------"
cmd="$LLVM_DIR/bin/opt -opaque-pointers=0 -load-pass-plugin ${BUILD_DIR}/libLowerFunnelShifts.so --passes=\"lower-funnel-shifts\" ${inputllfile} -S -o ${outfile_final}"

echo $cmd
eval $cmd || exit 1

echo "--------------------------------------"
echo "done. output file: ${outfile_final}"
echo "--------------------------------------"

