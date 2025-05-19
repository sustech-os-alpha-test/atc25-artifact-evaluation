#!/bin/bash

# 设置运行次数
RUN_TIMES=20  # 你可以根据需要修改运行次数
INIT_NUMBER=11  # 初始化的数字

# 需要进入的子目录
DIRS=("fio")

# 创建总结果目录
mkdir -p ./result-all-gap-iommu

for ((x=1; x<=RUN_TIMES; x++)); do
    for dir in "${DIRS[@]}"; do
        pushd "$dir" > /dev/null
        bash run_all.sh
        popd > /dev/null
    done

    # 复制结果到指定目录
    mkdir -p "./result-all-gap-iommu/result-${x}"
    cp -r ./result/* "./result-all-gap-iommu/result-${x}/"
    rm -rf ./result/*
done