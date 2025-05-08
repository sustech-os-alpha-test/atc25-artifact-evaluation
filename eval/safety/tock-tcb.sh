#!/bin/bash

if [ -d "$HOME/tock" ]; then
    rm -rf $HOME/tock
fi

ROOT_DIRECTORY=$(pwd)

git clone https://github.com/tock/tock ~/tock
pushd ~/tock
git reset --hard e1a744a4bb01f3f865616d9d5c31e1db9001bba9

sudo apt install -y git wget zip curl python3 python3-pip python3-venv

# Add "-- --emit=llvm-ir" to "$(Q)$(CARGO) rustc $(VERBOSE_FLAGS) --bin $(PLATFORM) " in boards/Makefile.common
sed -i 's/$(Q)$(CARGO) rustc $(VERBOSE_FLAGS) --bin $(PLATFORM)/$(Q)$(CARGO) rustc $(VERBOSE_FLAGS) --bin $(PLATFORM) -- --emit=llvm-ir/g' ~/tock/boards/Makefile.common

# Remove panic if setting Rust flags
sed -i '/            panic!(/d' ~/tock/boards/build_scripts/src/default.rs
sed -i '/"Incorrect build configuration. Verify you are using unstable cargo and have not unintentionally set the RUSTFLAGS environment variable."/d' ~/tock/boards/build_scripts/src/default.rs
sed -i '/            );/d' ~/tock/boards/build_scripts/src/default.rs

pushd boards/tutorials/nrf52840dk-thread-tutorial

RUSTFLAGS="--emit=llvm-ir" make debug

popd

popd

# Kernel and domains prepared, generated llvm files

mkdir -p ./tmp/
find ~/tock/target/thumbv7em-none-eabi/debug/deps -type f -name "*.ll" >./tmp/llvm_files_tock.txt

python link_all_ll/dep_tock.py
python count_tcb/tcb_tock.py

# Clean up...
rm -rf $HOME/tock
