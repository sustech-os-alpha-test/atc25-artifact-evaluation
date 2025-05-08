import re
import os

all_unsafe_crates = [
    "ascii",
    "ostd",
    "acpi",
    "bit_field",
    "align_ext",
    "bitvec",
    "funty",
    "radium",
    "tap",
    "wyz",
    "buddy_system_allocator",
    "cfg_if",
    "const_assert",
    "fdt",
    "gimli",
    "iced_x86",
    "lazy_static",
    "spin",
    "lock_api",
    "autocfg",
    "scopeguard",
    "id_alloc",
    "inherit_methods_macro",
    "darling",
    "darling_core",
    "fnv",
    "ident_case",
    "proc_macro2",
    "unicode_ident",
    "quote",
    "strsim",
    "darling_macro",
    "int_to_c_enum",
    "int_to_c_enum_derive",
    "intrusive_collections",
    "memoffset",
    "linux_boot_params",
    "multiboot2",
    "derive_more",
    "derive_more_impl",
    "unicode_xid",
    "multiboot2_common",
    "ptr_meta",
    "ptr_meta_derive",
    "uefi_raw",
    "uguid",
    "num",
    "num_complex",
    "num_traits",
    "num_integer",
    "num_iter",
    "num_rational",
    "num_derive",
    "ostd_macros",
    "rand",
    "libc",
    "rand_chacha",
    "ppv_lite86",
    "zerocopy",
    "byteorder",
    "zerocopy_derive",
    "rand_core",
    "getrandom",
    "wasi",
    "ostd_pod",
    "ostd_pod_derive",
    "ostd_test",
    "riscv",
    "critical_section",
    "embedded_hal",
    "sbi_rt",
    "sbi_spec",
    "smallvec",
    "static_assertions",
    "tdx_guest",
    "raw_cpuid",
    "unwinding",
    "volatile",
    "x86",
    "xarray",
    "serde",
    "serde_derive",
    "memchr",
    "inventory",
    "ctor",
    "ghost",
    "bytes",
    "generic_array",
    "typenum",
    "version_check",
    "cpufeatures",
    "ctr",
    "cipher",
    "subtle",
    "bittle",
    "polonius_the_crab",
    "lru",
    "postcard",
    "cobs",
    "core2",
    "fixed",
    "az",
    "bytemuck",
    "bytemuck_derive",
    "half",
    "crunchy",
    "dary_heap",
    "rle_decode_fast",
    "time",
    "deranged",
    "powerfmt",
    "num_conv",
    "time_core",
    "vte",
    "arrayvec",
    "utf8parse",
    "vte_generate_state_changes",
]


def extract_path(input_str):
    pattern = r"index\.crates\.io-[^/]*(.*)"
    match = re.search(pattern, input_str)

    if match:
        return match.group(1)
    return input_str


def parse_llvm_ir(folder_path):
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
    count_set = {}
    sum = 0
    sum_detail = {}
    # for file_name in os.listdir(folder_path):
    #     file_path = os.path.join(folder_path, file_name)
    #     if os.path.isfile(file_path) and file_name.endswith('.ll'):
    #         with open(file_path, 'r') as f:
    #             ir_code = f.read()
    #     else:
    #         continue
    for i in range(0, 1):
        file_path = folder_path
        with open(file_path, "r") as f:
            ir_code = f.read()
        print(file_path)
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
            # if "/library/core/src" in file_name or "/library/alloc/src" in file_name:
            #     continue
            key = extract_path(file_name + str(info[0]))
            if key in count_set:
                continue
            count_set[key] = 1
            sum += 1
            # if scope['func'] != None:
            #     file_name = file_name + ' ' + scope['func']
            sum_detail[file_name] = sum_detail.get(file_name, 0) + 1

        for scope in scopes.items():
            if scope[0] in black_scopes:
                continue
            if scope[1]["line"] == None:
                continue
            file_name = files[scope[1]["file"]]
            # if "/library/core/src" in file_name or "/library/alloc/src" in file_name:
            #     continue
            key = extract_path(file_name + str(scope[1]["line"]))
            if key in count_set:
                continue
            count_set[key] = 1
            sum += 1
            # if scope[1]['func'] != None:
            #     file_name = file_name + ' ' + scope[1]['func']
            sum_detail[file_name] = sum_detail.get(file_name, 0) + 1

    print()
    print("----------------------------------")
    print("Total: ", sum)
    print("----------------------------------")

    # total = 0
    # file_path_set = {}
    # for key, value in sum_detail.items():
    #     file_path = key.rsplit("/src/", 1)
    #     file_path_set[file_path[0]] = 1

    #     total += value
    #     print(f"{key} : {value}")

    # for key in file_path_set.keys():
    #     print(key)
    # print(total)

    # sorted_dict = dict(sorted(sum_detail.items(), key=lambda x: x[1], reverse=True))

    ostd_sum = 0
    # ostd_set = {}
    # with open("ostd_ll_list", "r") as f:
    #     ll_list = f.read().splitlines()

    # for i in sum_detail.items():
    #     print(i[0],":", i[1])

    for i in sum_detail.items():
        for j in all_unsafe_crates:
            if (j + "/src") in i[0] or ("/" + j + "-") in i[0]:
                if "asterinas/kernel/" in i[0]:
                    continue
                ostd_sum += i[1]
                #  print(j, ";", i[0],":", i[1])
                break
        # contain_flag = False
        # for path in ll_list:
        #     if path in i[0]:
        #         contain_flag = True
        #         break
        # if contain_flag:
        #     ostd_sum += i[1]
        #     ostd_set[i[0]] = i[1]

    # print("----------------------------------")
    print("TCB: ", ostd_sum)
    print("----------------------------------")
    # for i in ostd_set.items():
    #     print(i[0],":", i[1])


if __name__ == "__main__":
    # ir_file_path = "byteorder-8616c27afe6d549e.ll"  # Replace with the actual file path

    # folder_path = '/root/asterinas/target/x86_64-unknown-none/debug/deps'

    folder_path = "tmp/all_aster-nix.ll"

    parse_llvm_ir(folder_path)
