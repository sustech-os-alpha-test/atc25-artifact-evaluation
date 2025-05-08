#!/bin/bash

source ../utils/bench_utils.sh

BASE_DIR="lmbench"

declare -a BENCH_NAMES=(
    $BASE_DIR"/vfs_open_lat"
    $BASE_DIR"/vfs_read_lat"
    $BASE_DIR"/vfs_write_lat"
    $BASE_DIR"/vfs_stat_lat"
    $BASE_DIR"/vfs_fstat_lat"
    $BASE_DIR"/vfs_read_pagecache_bw"
    $BASE_DIR"/ramfs_copy_files_bw"
    $BASE_DIR"/ramfs_copy_to_ext2_files_bw"
    $BASE_DIR"/ext2_copy_to_ramfs_files_bw"
    $BASE_DIR"/ext2_copy_files_bw"
)

declare -a BENCH_METHODS=(
    "guest_only"
    "guest_only"
    "guest_only"
    "guest_only"
    "guest_only"
    "guest_only"
    "guest_only"
    "guest_only"
    "guest_only"
    "guest_only"
)

runInputBenchs
