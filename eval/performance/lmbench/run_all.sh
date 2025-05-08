#!/bin/bash

source ../utils/bench_utils.sh

./proc.sh
./mem.sh
./ipc.sh
./fs.sh
./net.sh

collectResults "lmbench"
