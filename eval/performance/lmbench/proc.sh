#!/bin/bash

source ../utils/bench_utils.sh

BASE_DIR="lmbench"

declare -a BENCH_NAMES=(
    $BASE_DIR"/process_getppid_lat"
    $BASE_DIR"/process_ctx_lat"
    $BASE_DIR"/process_fork_lat"
    $BASE_DIR"/process_exec_lat"
    $BASE_DIR"/process_shell_lat"
)

declare -a BENCH_METHODS=(
    "guest_only"
    "guest_only"
    "guest_only"
    "guest_only"
    "guest_only"
)

runInputBenchs
