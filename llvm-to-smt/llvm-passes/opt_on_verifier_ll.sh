#!/bin/bash

if [ $# -ne 5 ]; then
    echo "$0: Usage: opt_on_verifier.sh input_file output_dir output_file Olevel(O1|O0_custom) strip_debug(Y|N)"
    exit 1
fi

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
source ${SCRIPT_DIR}/.config

oldpwd=$(pwd)
input_llfile=$(readlink -f $1)
output_finaldir=$(readlink -f $2)
output_finalfilename=$3
output_llfile="${output_finaldir}/${output_finalfilename}"
olevel=$4
strip_debug=$5


if [ "$olevel" = "O1" ]; then
    echo "--------------------------------------"
    echo "run opt O1 pass on ${input_llfile}"
    echo "--------------------------------------"
    cmd="${LLVM_DIR}/bin/opt -O1 --strip-debug --instnamer --stats -S  ${input_llfile} -o ${output_llfile}"
    # -mno-memcpy 
elif [ "$olevel" = "O0_custom" ]; then
    echo "--------------------------------------"
    echo "run specific OPT passes on ${input}"
    echo "--------------------------------------"
    cmd="${LLVM_DIR}/bin/opt -S --instnamer --simplifycfg --sroa --mergereturn --dce --deadargelim --memoryssa --always-inline --function-attrs --argpromotion --instcombine ${input_llfile} -o ${output_llfile}.ll"
    cmd="${cmd} && mv ${output_llfile}.ll ${output_llfile}"
else 
    echo "------------------"
    echo "[ERROR] incorrect Olevel. Choose from (O1|O0_custom)".
    echo "------------------"
    exit 1
fi

echo $cmd
eval $cmd || exit 1

echo $strip_debug
if [ "$strip_debug" = "Y" ]; then
    echo "--------------------------------------"
    echo "running strip-debug ${output_llfile}"
    echo "--------------------------------------"
    cmd="${LLVM_DIR}/bin/opt -S --strip-debug ${output_llfile} -o ${output_llfile}.ll"
    cmd="${cmd} && mv ${output_llfile}.ll ${output_llfile}"
    echo $cmd
    eval $cmd || exit 1
fi

ret=$(echo $?)
echo "--------------------------------------"
echo "success? ${ret}"
echo "done. output file: ${output_llfile}"
echo "--------------------------------------"
