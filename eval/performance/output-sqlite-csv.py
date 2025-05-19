import os
import re
import csv
from collections import defaultdict

def parse_result_file(filepath):
    """解析结果文件，提取测试数据"""
    with open(filepath, 'r') as f:
        content = f.read()
    
    # 查找SQLite版本信息后的内容
    version_match = re.search(r'SQLite \d+\.\d+\.\d+ \d{4}-\d{2}-\d{2} [0-9a-f]+', content)
    if not version_match:
        return {}
    
    start_pos = version_match.end()
    total_match = re.search(r'TOTAL.*?([\d\.]+)s', content[start_pos:])
    if not total_match:
        return {}
    
    data_block = content[start_pos:start_pos+total_match.start()]
    
    # 提取每行数据
    pattern = re.compile(r'^\s*(\d+)\s*-\s*(.+?)[\. ]+\s*([\d\.]+)s', re.MULTILINE)
    results = {}
    
    for match in pattern.finditer(data_block):
        test_value = match.group(1)
        test_name = match.group(2).strip()
        time = match.group(3)
        results[(test_value, test_name)] = time
    
    # 添加TOTAL结果
    total_time = total_match.group(1)
    results[('999', 'TOTAL')] = total_time  # 使用999作为TOTAL的编号，确保它排在最后
    
    return results

def collect_all_results(base_path):
    """收集所有结果目录中的数据"""
    aster_results = defaultdict(dict)
    linux_results = defaultdict(dict)
    
    # 遍历所有result-*目录
    for dir_name in os.listdir(base_path):
        if not dir_name.startswith('result-'):
            continue
        
        try:
            result_num = int(dir_name.split('-')[1])
        except (IndexError, ValueError):
            continue
        
        sqlite_dir = os.path.join(base_path, dir_name, 'sqlite')
        
        # 解析Asterinas结果
        aster_file = os.path.join(sqlite_dir, 'aster_output.txt')
        if os.path.exists(aster_file):
            aster_data = parse_result_file(aster_file)
            for key, value in aster_data.items():
                aster_results[key][f'Asterinas-{result_num}'] = value
        
        # 解析Linux结果
        linux_file = os.path.join(sqlite_dir, 'linux_output.txt')
        if os.path.exists(linux_file):
            linux_data = parse_result_file(linux_file)
            for key, value in linux_data.items():
                linux_results[key][f'Linux-{result_num}'] = value
    
    return aster_results, linux_results

def write_to_csv(output_file, aster_results, linux_results):
    """将结果写入CSV文件"""
    # 收集所有测试用例
    all_tests = set(aster_results.keys()).union(set(linux_results.keys()))
    # 按测试编号排序，确保TOTAL(999)在最后
    all_tests = sorted(all_tests, key=lambda x: int(x[0]))
    
    # 收集所有结果列
    all_columns = set()
    for test_data in aster_results.values():
        all_columns.update(test_data.keys())
    for test_data in linux_results.values():
        all_columns.update(test_data.keys())
    all_columns = sorted(all_columns)
    
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        
        # 写入标题行
        header = ['test_value', 'test_name'] + all_columns
        writer.writerow(header)
        
        # 写入每行数据
        for test_key in all_tests:
            test_value, test_name = test_key
            row = [test_value, test_name]
            
            for col in all_columns:
                # 先查找Asterinas结果，再查找Linux结果
                value = aster_results.get(test_key, {}).get(col, 
                       linux_results.get(test_key, {}).get(col, ''))
                row.append(value)
            
            writer.writerow(row)

def main():
    base_path = 'result-all-no-iommu'  # 根据需要修改路径
    output_file = 'sqlite_benchmark_results.csv'
    
    aster_results, linux_results = collect_all_results(base_path)
    write_to_csv(output_file, aster_results, linux_results)
    
    print(f"结果已保存到 {output_file}")

if __name__ == '__main__':
    main()
