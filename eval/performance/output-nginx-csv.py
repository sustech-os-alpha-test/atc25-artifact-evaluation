import os
import json
import csv
from collections import defaultdict


def process_nginx_results(root_dir="result-all-no-iommu"):
    # Initialize data structure to store all results
    results = defaultdict(lambda: defaultdict(dict))
    linux_counts = defaultdict(int)
    aster_counts = defaultdict(int)

    # Get and sort all result directories numerically
    result_dirs = [d for d in os.listdir(root_dir) if d.startswith("result-")]
    result_dirs.sort(key=lambda x: int(x.split("-")[1]))

    # First pass: collect all unique file names and determine max counts
    for result_dir in result_dirs:
        if not result_dir.startswith("result-"):
            continue

        nginx_path = os.path.join(root_dir, result_dir, "nginx")
        if not os.path.exists(nginx_path):
            continue

        for json_file in os.listdir(nginx_path):
            if not json_file.endswith(".json"):
                continue
            if json_file.startswith("Ratio-summary"):
                continue

            with open(os.path.join(nginx_path, json_file)) as f:
                data = json.load(f)

            for entry in data:
                if "linux" in entry["extra"].lower():
                    linux_counts[json_file] += 1
                elif "aster" in entry["extra"].lower():
                    aster_counts[json_file] += 1

    max_linux = max(linux_counts.values()) if linux_counts else 0
    max_aster = max(aster_counts.values()) if aster_counts else 0
    print(f"Max Linux runs: {max_linux}, Max Asterinas runs: {max_aster}")

    # Second pass: collect all data
    for result_dir in result_dirs:
        if not result_dir.startswith("result-"):
            continue

        run_number = result_dir.split("-")[1]
        nginx_path = os.path.join(root_dir, result_dir, "nginx")
        if not os.path.exists(nginx_path):
            continue

        for json_file in os.listdir(nginx_path):
            if not json_file.endswith(".json"):
                continue
            if json_file.startswith("Ratio-summary"):
                continue

            with open(os.path.join(nginx_path, json_file)) as f:
                data = json.load(f)

            for entry in data:
                key = f"{json_file},{entry['unit']}"
                print(f"Processing {key} for run {run_number}")
                if "linux" in entry["extra"].lower():
                    results[key][f"Linux-{run_number}"] = entry["value"]
                elif "aster" in entry["extra"].lower():
                    results[key][f"Asterinas-{run_number}"] = entry["value"]

    # Prepare CSV output
    output_file = "nginx_results.csv"
    aster_headers = [f"Asterinas-{i+1}" for i in range(max_aster)]
    linux_headers = [f"Linux-{i+1}" for i in range(max_linux)]
    headers = ["file_name", "unit"] + aster_headers + linux_headers

    with open(output_file, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)

        # Output with sorted keys

        for key in sorted(results.keys()):
            file_name, unit = key.split(",", 2)
            row = [file_name, unit]

            print(f"Processing row for {key}")

            # Add Asterinas values in order
            for header in aster_headers:
                print(f"Adding Asterinas value for {header}")
                print(f"Adding Asterinas value for {results[key][header]}")
                row.append(results[key].get(header, ""))

            # Add Linux values in order
            for header in linux_headers:
                row.append(results[key].get(header, ""))

            writer.writerow(row)

    print(f"Results saved to {output_file}")


if __name__ == "__main__":
    process_nginx_results()

# process_getppid_lat, process_ctx_lat, process_fork_lat, process_exec_lat, process_shell_lat, mem_pagefault_lat, mem_mmap_lat, mem_mmap_bw, pipe_lat, pipe_bw, fifo_lat, unix_lat, unix_bw, vfs_open_lat, vfs_read_lat, vfs_write_lat, vfs_stat_lat, vfs_fstat_lat, vfs_read_pagecache_bw, ramfs_copy_files_bw, ramfs_copy_to_ext2_files_bw, ext2_copy_to_ramfs_files_bw, ext2_copy_files_bw, udp_loopback_lat, tcp_loopback_lat, tcp_loopback_bw_128, tcp_loopback_bw_64k, udp_virtio_lat, tcp_virtio_lat, tcp_virtio_bw_128, tcp_virtio_bw_64k

