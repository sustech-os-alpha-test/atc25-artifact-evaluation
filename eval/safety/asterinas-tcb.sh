#!/bin/bash

pushd ../../
# Do cleanup first, make sure it will generate all .ll files
make clean
RUSTFLAGS="--emit=llvm-ir" make build
popd

mkdir -p ./tmp/
find ../../target/x86_64-unknown-none/debug/deps -type f -name "*.ll" >./tmp/llvm_files_asterinas.txt

python link_all_ll/dep_asterinas.py
python count_tcb/tcb_asterinas.py

# Clean up...
cd ../../
make clean
