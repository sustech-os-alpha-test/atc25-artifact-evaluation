import re
import os

all_unsafe_crates = [
    "bdev_shadow",
    "console",
    "libsyscalls",
    "pc_keyboard",
    "platform",
    "syscalls",
    "protocol",
    "bitfield",
    "interface",
    "bitflags",
    "byteorder",
    "num_derive",
    "proc_macro2",
    "unicode_xid",
    "quote",
    "syn",
    "num_traits",
    "pci_driver",
    "ahci",
    "unwind",
    "lazy_static",
    "libmembdev",
    "arrayvec",
    "array_init",
    "libbenchnet",
    "b2histogram",
    "fnv",
    "libtime",
    "sashstore_redleaf",
    "cfg_if",
    "twox_hash",
    "libbenchnvme",
    "libbenchtpm",
    "libtpm",
    "malloc",
    "slabmalloc",
    "sha2",
    "block_buffer",
    "generic_array",
    "typenum",
    "version_check",
    "cpuid_bool",
    "digest",
    "opaque_debug",
    "redhttpd",
    "smoltcp",
    "managed",
    "utils",
    "ixgbe",
    "ixgbe_device",
    "libdma",
    "smolnet",
    "membdev",
    "nvme_device",
    "pcidevice",
    "x86",
    "bit_field",
    "raw_cpuid",
    "cc",
    "rustc_version",
    "semver",
    "semver_parser",
    "tpm_device",
    "virtio_block_device",
    "virtio_device",
    "volatile_accessor",
    "virtio_network_device",
    "xv6net",
    "libusr",
    "sync",
    "tls",
]


def extract_path(input_str):
    pattern = r"index\.crates\.io-[^/]*(.*)"
    match = re.search(pattern, input_str)

    if match:
        return match.group(1)
    return input_str


count_set = {}
sum_tcb = 0
sum = 0


def parse_llvm_ir(folder_path):
    global sum, sum_tcb
    file_regex = re.compile(
        r'!(?P<id>\d+) = !DIFile\(filename:\s*"(?P<filename>[^"]+)",\s*directory:\s*"(?P<directory>[^"]*)".*?\)'
    )

    debug_info_regex_loc = re.compile(
        r"!(?P<id>\d+)\s*=.*?line:\s*(?P<line>\d+),.*?scope:\s*!(?P<scope>\d+)\)"
    )
    debug_info_regex_func = re.compile(
        r'!(?P<id>\d+)\s*= distinct !DISubprogram\(name:\s*"(?P<name>[^"]+)",.*?scope:\s*!(?P<scope>\d+),.*?file:\s*!(?P<file>\d+),.*?line:\s*(?P<line>\d+).*?\)'
    )
    debug_info_regex_other = re.compile(
        r"!(?P<id>\d+)\s*=.*?scope:\s*!(?P<scope>\d+),.*?file:\s*!(?P<file>\d+),.*?(?:line:\s*(?P<line>\d+),)?.*?\)"
    )
    ll_file_set = {}
    sum_kernel = 0
    sum_app = 0
    sum_detail = {}
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path) and file_name.endswith(".ll"):
            with open(file_path, "r") as f:
                ir_code = f.read()
        else:
            continue

        # print(file_path)
        debug_infos = []
        scopes = {}
        files = {}
        black_scopes = {}
        lines = ir_code.splitlines()
        for line in reversed(lines):
            debug_info_match = debug_info_regex_loc.search(line)
            if debug_info_match:
                dbg_id = int(debug_info_match.group("id"))
                line_number = int(debug_info_match.group("line"))
                scope_number = int(debug_info_match.group("scope"))

                debug_infos.append((line_number, scope_number))
                if dbg_id == 0:
                    break
                continue

            debug_info_match = debug_info_regex_func.search(line)
            if debug_info_match:
                dbg_id = int(debug_info_match.group("id"))
                name = debug_info_match.group("name")
                line_number = int(debug_info_match.group("line"))
                file_number = int(debug_info_match.group("file"))
                # if name == 'fmt':
                #     black_scopes[dbg_id] = 1
                scopes[dbg_id] = {
                    "func": name,
                    "line": line_number,
                    "file": file_number,
                }
                if dbg_id == 0:
                    break
                continue

            debug_info_match = debug_info_regex_other.search(line)
            if debug_info_match:
                dbg_id = int(debug_info_match.group("id"))
                line_number = None
                tmp = debug_info_match.group("line")
                if tmp != None:
                    line_number = int(tmp)
                file_number = int(debug_info_match.group("file"))

                scopes[dbg_id] = {
                    "func": None,
                    "line": line_number,
                    "file": file_number,
                }
                if dbg_id == 0:
                    break
                continue

            file_info_match = file_regex.search(line)
            if file_info_match:
                dbg_id = int(file_info_match.group("id"))
                filename = file_info_match.group("filename")
                directory = file_info_match.group("directory")
                if len(directory) > 0:
                    directory += "/"
                files[dbg_id] = directory + filename

        for info in debug_infos:
            if info[1] in black_scopes:
                continue
            scope = scopes[info[1]]
            file_name = files[scope["file"]]
            if "bench" in file_name:
                continue
            key = extract_path(file_name + str(info[0]))
            if key in count_set:
                continue
            count_set[key] = 1
            sum += 1
            if scope["func"] != None:
                file_name = file_name + " " + scope["func"]
            sum_detail[file_name] = sum_detail.get(file_name, 0) + 1

        for scope in scopes.items():
            if scope[0] in black_scopes:
                continue
            if scope[1]["line"] == None:
                continue
            file_name = files[scope[1]["file"]]
            if "bench" in file_name:
                continue
            key = extract_path(file_name + str(scope[1]["line"]))
            if key in count_set:
                continue
            count_set[key] = 1
            sum += 1
            # if scope[1]['func'] != None:
            #     file_name = file_name + ' ' + scope[1]['func']
            sum_detail[file_name] = sum_detail.get(file_name, 0) + 1

    for i in sum_detail.items():
        if "redleaf/lib/core" in i[0]:
            sum_tcb += i[1]
            # print(i[0], ":", i[1])
            continue
        for j in all_unsafe_crates:
            if (j + "/src") in i[0] or ("/" + j + "-") in i[0]:
                if "12-15/lib/rustlib/src/rust/library/alloc/src/vec/" in i[0]:
                    print("!!!!!!!", j)
                sum_tcb += i[1]
                # print("kind2---", i[0], ":", i[1])
                break


def parse_llvm_ir2(folder_path):
    global sum, sum_tcb
    file_regex = re.compile(
        r'!(?P<id>\d+) = !DIFile\(filename:\s*"(?P<filename>[^"]+)",\s*directory:\s*"(?P<directory>[^"]*)".*?\)'
    )

    debug_info_regex_loc = re.compile(
        r"!(?P<id>\d+)\s*=.*?line:\s*(?P<line>\d+),.*?scope:\s*!(?P<scope>\d+)\)"
    )
    debug_info_regex_func = re.compile(
        r'!(?P<id>\d+)\s*= distinct !DISubprogram\(name:\s*"(?P<name>[^"]+)",.*?scope:\s*!(?P<scope>\d+),.*?file:\s*!(?P<file>\d+),.*?line:\s*(?P<line>\d+).*?\)'
    )
    debug_info_regex_other = re.compile(
        r"!(?P<id>\d+)\s*=.*?scope:\s*!(?P<scope>\d+),.*?file:\s*!(?P<file>\d+),.*?(?:line:\s*(?P<line>\d+),)?.*?\)"
    )
    ll_file_set = {}
    sum_kernel = 0
    sum_app = 0
    sum_detail = {}

    file_path = folder_path

    with open(file_path, "r") as f:
        ir_code = f.read()
    for i in range(0, 1):
        # print(file_path)
        debug_infos = []
        scopes = {}
        files = {}
        black_scopes = {}
        lines = ir_code.splitlines()
        for line in reversed(lines):
            debug_info_match = debug_info_regex_loc.search(line)
            if debug_info_match:
                dbg_id = int(debug_info_match.group("id"))
                line_number = int(debug_info_match.group("line"))
                scope_number = int(debug_info_match.group("scope"))

                debug_infos.append((line_number, scope_number))
                if dbg_id == 0:
                    break
                continue

            debug_info_match = debug_info_regex_func.search(line)
            if debug_info_match:
                dbg_id = int(debug_info_match.group("id"))
                name = debug_info_match.group("name")
                line_number = int(debug_info_match.group("line"))
                file_number = int(debug_info_match.group("file"))
                # if name == 'fmt':
                #     black_scopes[dbg_id] = 1
                scopes[dbg_id] = {
                    "func": name,
                    "line": line_number,
                    "file": file_number,
                }
                if dbg_id == 0:
                    break
                continue

            debug_info_match = debug_info_regex_other.search(line)
            if debug_info_match:
                dbg_id = int(debug_info_match.group("id"))
                line_number = None
                tmp = debug_info_match.group("line")
                if tmp != None:
                    line_number = int(tmp)
                file_number = int(debug_info_match.group("file"))

                scopes[dbg_id] = {
                    "func": None,
                    "line": line_number,
                    "file": file_number,
                }
                if dbg_id == 0:
                    break
                continue

            file_info_match = file_regex.search(line)
            if file_info_match:
                dbg_id = int(file_info_match.group("id"))
                filename = file_info_match.group("filename")
                directory = file_info_match.group("directory")
                if len(directory) > 0:
                    directory += "/"
                files[dbg_id] = directory + filename

        for info in debug_infos:
            if info[1] in black_scopes:
                continue
            scope = scopes[info[1]]
            file_name = files[scope["file"]]
            if "bench" in file_name:
                continue
            # if "/library/core/src" in file_name or "/library/alloc/src" in file_name or "bench" in file_name:
            #     continue
            key = extract_path(file_name + str(info[0]))
            if key in count_set:
                continue
            count_set[key] = 1
            sum += 1

            if not (
                "/library/core/src" in file_name or "/library/alloc/src" in file_name
            ):
                sum_tcb += 1

            if scope["func"] != None:
                file_name = file_name + " " + scope["func"]
            sum_detail[file_name] = sum_detail.get(file_name, 0) + 1

        for scope in scopes.items():
            if scope[0] in black_scopes:
                continue
            if scope[1]["line"] == None:
                continue
            file_name = files[scope[1]["file"]]
            if "bench" in file_name:
                continue
            key = extract_path(file_name + str(scope[1]["line"]))
            if key in count_set:
                continue
            count_set[key] = 1
            sum += 1
            if not (
                "/library/core/src" in file_name or "/library/alloc/src" in file_name
            ):
                sum_tcb += 1
            # if scope[1]['func'] != None:
            #     file_name = file_name + ' ' + scope[1]['func']
            sum_detail[file_name] = sum_detail.get(file_name, 0) + 1
            if "redleaf/domains" in file_name and "bench" not in file_name:
                fnames = file_path.split("/debug/deps/")
                ll_file_set[fnames[-1]] = 1

    print()
    # print("----------------------------------")
    # for i in ll_file_set:
    #     print(i)
    print("----------------------------------")
    print("Total: ", sum)
    print("----------------------------------")
    print("TCB: ", sum_tcb)
    print("----------------------------------")
    # sorted_dict = dict(sorted(sum_detail.items(), key=lambda x: x[1], reverse=True))


if __name__ == "__main__":
    folder_path = "tmp/redleaf_domains/"
    parse_llvm_ir(folder_path)

    folder_path = "tmp/all_redleaf-kernel.ll"
    parse_llvm_ir2(folder_path)
