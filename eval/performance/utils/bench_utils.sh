#!/bin/bash

function runBench() {
    local name=$1
    local how=$2

    pushd ../../../

    pushd test
    make clean
    popd

    ./test/benchmark/bench_linux_and_aster.sh $name $how
    popd
}

function runInputBenchs() {
    local i
    for ((i = 0; i < ${#BENCH_NAMES[@]}; i++)); do
        local name="${BENCH_NAMES[$i]}"
        local how="${BENCH_METHODS[$i]}"

        runBench $name $how
    done
}

function collectResults() {
    local BENCH_NAME=$1

    pushd ../

    mkdir -p ./result/$BENCH_NAME/
    mv ../../*.json ./result/$BENCH_NAME/

    python ./utils/output-ratio.py ./result/$BENCH_NAME ./result/$BENCH_NAME/Ratio-summary.json

    popd
}
