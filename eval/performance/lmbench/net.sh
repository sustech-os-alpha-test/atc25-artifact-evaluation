#!/bin/bash

source ../utils/bench_utils.sh

BASE_DIR="lmbench"

declare -a BENCH_NAMES=(
    $BASE_DIR"/udp_loopback_lat"
    $BASE_DIR"/tcp_loopback_lat"
    $BASE_DIR"/tcp_loopback_bw_128"
    $BASE_DIR"/tcp_loopback_bw_64k"
    $BASE_DIR"/udp_virtio_lat"
    $BASE_DIR"/tcp_virtio_lat"
    $BASE_DIR"/tcp_virtio_bw_128"
    $BASE_DIR"/tcp_virtio_bw_64k"
)

declare -a BENCH_METHODS=(
    "guest_only"
    "guest_only"
    "guest_only"
    "guest_only"
    "host_guest"
    "host_guest"
    "host_guest"
    "host_guest"
)

runInputBenchs
