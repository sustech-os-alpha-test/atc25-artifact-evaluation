#!/bin/bash

if [ -d "$HOME/theseus" ]; then
    rm -rf $HOME/theseus
fi

ROOT_DIRECTORY=$(pwd)

git clone --recurse-submodules https://github.com/theseus-os/Theseus.git ~/theseus
pushd ~/theseus
git reset --hard ffb5e8b360fff655767b5ed13e6122db9a583857

sudo apt-get install -y make gcc nasm pkg-config grub-pc-bin mtools xorriso qemu qemu-kvm wget

# Replace "--release" to "" in Makefile
sed -i 's/--release//g' ~/theseus/Makefile

# Replace "release" to "debug" in Makefile
sed -i 's/release/debug/g' ~/theseus/Makefile

# Replace "BUILD_MODE ?= release" to "BUILD_MODE ?= debug" in cfg/Config.mk
sed -i 's/BUILD_MODE ?= release/BUILD_MODE ?= debug/g' ~/theseus/cfg/Config.mk

# Replace "--release" to "" in scripts/build_server.sh
sed -i 's/--release//g' ~/theseus/scripts/build_server.sh

RUSTFLAGS="--emit=llvm-ir" make full

popd

# Kernel and domains prepared, generated llvm files

rustup install nightly-2024-06-20
rustup +nightly-2024-06-20 component add llvm-tools

mkdir -p ./tmp/
find ~/theseus/target/x86_64-unknown-theseus/debug/deps -type f -name "*.ll" >./tmp/llvm_files_theseus.txt

python link_all_ll/dep_theseus.py
python count_tcb/tcb_theseus.py

# Clean up...
rm -rf $HOME/theseus
