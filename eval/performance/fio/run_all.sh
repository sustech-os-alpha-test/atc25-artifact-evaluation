#!/bin/bash

source ../utils/bench_utils.sh

declare -a BENCH_NAMES=(
    "fio/ext2_seq_read_bw"
    "fio/ext2_seq_write_bw"
)

declare -a BENCH_METHODS=(
    "guest_only"
    "guest_only"
)

runInputBenchs

collectResults "fio"
