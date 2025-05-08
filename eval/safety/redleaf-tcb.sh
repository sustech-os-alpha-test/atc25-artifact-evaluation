#!/bin/bash

if [ -d "$HOME/redleaf" ]; then
    rm -rf $HOME/redleaf
fi

ROOT_DIRECTORY=$(pwd)

git clone https://github.com/mars-research/redleaf.git ~/redleaf
pushd ~/redleaf
git reset --hard 7194295d1968c8013ae6b3d104a9192f03516449
git submodule init && git submodule update

./setup.sh

pushd ~
cargo install cargo-expand
popd

RUSTFLAGS="--emit=llvm-ir" make kernel

pushd interface
make clean
popd

RUSTFLAGS="--emit=llvm-ir" make domains

popd

# Kernel and domains prepared, generated llvm files

mkdir -p ./tmp/
find ~/redleaf/kernel/target/x86_64-unknown-none/debug/deps -type f -name "*.ll" >./tmp/llvm_files_redleaf_kernel.txt
find ~/redleaf/domains/target/x86_64-unknown-redleaf/debug/deps -type f -name "*.ll" >./tmp/llvm_files_redleaf_domains.txt

pip3 install toml
sudo apt-get install -y llvm-13

python link_all_ll/dep_redleaf_domains.py
python link_all_ll/dep_redleaf_kernel.py
python count_tcb/tcb_redleaf.py

# Clean up...
rm -rf $HOME/redleaf
