#!/bin/bash

source ../utils/bench_utils.sh

declare -a BENCH_NAMES=(
    "lmbench/tcp_virtio_bw_128"
    "lmbench/tcp_virtio_bw_64k"
)

declare -a BENCH_METHODS=(
    "host_guest"
    "host_guest"
)

runInputBenchs

collectResults "gap_iommu"
