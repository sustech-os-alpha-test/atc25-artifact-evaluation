#!/bin/bash

source ../utils/bench_utils.sh

declare -a BENCH_NAMES=(
    "redis/set_100k_conc20_rps"
    "redis/get_100k_conc20_rps"
    "redis/lpush_100k_conc20_rps"
    "redis/lpop_100k_conc20_rps"
    "redis/all_100k_conc20_rps"
)

declare -a BENCH_METHODS=(
    "host_guest"
    "host_guest"
    "host_guest"
    "host_guest"
    "host_guest"
)

runInputBenchs

collectResults "redis"

mv ../../../all-*.csv ../result/redis/
