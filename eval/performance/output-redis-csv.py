import os
import csv
from collections import defaultdict

def process_csv_files():
    # Find all all-{number}.csv files and sort them numerically
    csv_files = []
    for file in os.listdir('./redis-no-iommu-result'):
        if file.startswith('all-') and file.endswith('.csv'):
            try:
                num = int(file[4:-4])  # Extract number from "all-{number}.csv"
                csv_files.append((num, "./redis-no-iommu-result/"+file))
            except ValueError:
                continue
    
    # Sort files by their number
    csv_files.sort()
    
    # Collect data from all files
    data = defaultdict(dict)
    system_names = []
    
    for idx, (num, filename) in enumerate(csv_files):
        # Determine system name (alternating Asterinas/Linux)
        system = "Asterinas" if idx % 2 == 0 else "Linux"
        runtime = (idx // 2) + 1
        system_name = f"{system}-{runtime}"
        system_names.append(system_name)
        
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)  # Skip header
            
            for row in reader:
                test_name = row[0]
                rps = row[1]
                
                # Skip the unwanted row
                if "LPUSH (needed to benchmark LRANGE)" in test_name:
                    continue
                
                data[test_name][system_name] = rps
    
    # Prepare output CSV
    output_filename = "combined_results.csv"
    
    # Get all unique test names (sorted as they appear in the first file)
    test_names = []
    with open(csv_files[0][1], 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for row in reader:
            test_name = row[0]
            if "LPUSH (needed to benchmark LRANGE)" not in test_name:
                test_names.append(test_name)
    
    # Group system names by type (Asterinas first, then Linux)
    asterinas_systems = [name for name in system_names if "Asterinas" in name]
    linux_systems = [name for name in system_names if "Linux" in name]
    all_systems = asterinas_systems + linux_systems
    
    with open(output_filename, 'w', newline='') as f:
        writer = csv.writer(f)
        
        # Write header
        header = ["test"] + all_systems
        writer.writerow(header)
        
        # Write data rows
        for test_name in test_names:
            if test_name not in data:
                continue
                
            row = [test_name]
            for system in all_systems:
                row.append(data[test_name].get(system, ""))
            writer.writerow(row)
    
    print(f"Combined results saved to {output_filename}")

if __name__ == "__main__":
    process_csv_files()
