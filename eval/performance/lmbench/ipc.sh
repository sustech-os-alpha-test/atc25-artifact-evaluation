#!/bin/bash

source ../utils/bench_utils.sh

BASE_DIR="lmbench"

declare -a BENCH_NAMES=(
    $BASE_DIR"/pipe_lat"
    $BASE_DIR"/pipe_bw"
    $BASE_DIR"/fifo_lat"
    $BASE_DIR"/unix_lat"
    $BASE_DIR"/unix_bw"
)

declare -a BENCH_METHODS=(
    "guest_only"
    "guest_only"
    "guest_only"
    "guest_only"
    "guest_only"
)

runInputBenchs
