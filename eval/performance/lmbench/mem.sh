#!/bin/bash

source ../utils/bench_utils.sh

BASE_DIR="lmbench"

declare -a BENCH_NAMES=(
    $BASE_DIR"/mem_pagefault_lat"
    $BASE_DIR"/mem_mmap_lat"
    $BASE_DIR"/mem_mmap_bw"
)

declare -a BENCH_METHODS=(
    "guest_only"
    "guest_only"
    "guest_only"
)

runInputBenchs
