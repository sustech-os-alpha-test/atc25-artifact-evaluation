import subprocess
import json
import os

# Get home directory
home_dir = os.path.expanduser("~")

metadata = json.loads(
    subprocess.check_output(
        [
            "cargo",
            "metadata",
            "--format-version=1",
        ]
    )
)

deps = {}
for package in metadata["packages"]:
    deps[package["name"]] = [dep["name"] for dep in package["dependencies"]]

folders = ["aster-nix"]


def topological_sort(deps_name):
    visited = {}
    result = []

    def visit(name):
        if name in visited:
            return
        visited[name] = True
        for dep in deps.get(name, []):
            visit(dep)
        result.append(name)

    visit(deps_name)
    return result


for folder in folders:
    result = topological_sort(folder)[::-1]
    sorted_files = []
    for crate in result:
        crate = crate.replace("-", "_")
        sorted_files.extend(
            [
                f.strip()
                for f in open("tmp/llvm_files_asterinas.txt")
                if crate in f.split("deps/")[1]
            ]
        )
    unique_list = list(dict.fromkeys(sorted_files))
    print(unique_list)
    print(len(unique_list))
    print()

    result_dir = "tmp/"
    # Make directory if it doesn't exist
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)

    output_file = f"{result_dir}all_{folder}.bc"
    final_file = f"{result_dir}all_{folder}.ll"

    command = [
        f"{home_dir}/.rustup/toolchains/nightly-2025-02-01-x86_64-unknown-linux-gnu/lib/rustlib/x86_64-unknown-linux-gnu/bin/llvm-link",
        "--only-needed",
        *sorted_files,
        "-o",
        output_file,
    ]

    try:
        subprocess.run(command, check=True)
        print(f"Successfully created {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to create {output_file}: {e}")

    command = [
        f"{home_dir}/.rustup/toolchains/nightly-2025-02-01-x86_64-unknown-linux-gnu/lib/rustlib/x86_64-unknown-linux-gnu/bin/llvm-dis",
        output_file,
        "-o",
        final_file,
    ]

    try:
        subprocess.run(command, check=True)
        print(f"Successfully created {final_file}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to create {final_file}: {e}")


# sorted_crates = topological_sort(deps)

# sorted_files = []
# for crate in sorted_crates:
#     crate = crate.replace("-", "_")
#     print(crate)
#     sorted_files.extend([f for f in open('llvm_files.txt') if crate in f.split("deps/")[1]])

# for f in open('llvm_files.txt'):
#     flag0 = True
#     for i in sorted_files:
#         if f in i:
#             flag0 = False
#     if flag0:
#         print(f)

# with open('sorted_llvm_files.txt', 'w') as f:
#     f.writelines(sorted_files)
