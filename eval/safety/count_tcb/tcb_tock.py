import re
import os


all_unsafe_crates = [
    "nrf52840dk_thread_tutorial",
    "capsules_core",
    "enum_primitive",
    "kernel",
    "tock_cells",
    "tock_registers",
    "tock_tbf",
    "tickv",
    "capsules_extra",
    "capsules_system",
    "components",
    "segger",
    "nrf52840",
    "cortexm4",
    "cortexm",
    "cortexv7m",
    "nrf52",
    "nrf5x",
    "nrf52840dk",
    "nrf52_components",
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
    ll_file_set = {}
    sum = 0
    sum_kernel = 0
    sum_tcb = 0
    sum_detail = {}
    for lls in range(0, 1):
        file_path = folder_path
        if os.path.isfile(file_path):
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
            # if "/library/core/src" in file_name or "/library/alloc/src" in file_name:
            #     continue
            key = extract_path(file_name + str(info[0]))
            if key in count_set:
                continue
            count_set[key] = 1
            sum += 1
            # if "/capsules/" in file_name:
            #     sum_tcb += 1
            if scope["func"] != None:
                file_name = file_name + " " + scope["func"]
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
            # if "/capsules/" in file_name:
            #     sum_tcb += 1
            sum_detail[file_name] = sum_detail.get(file_name, 0) + 1

    for i in sum_detail.items():
        for j in all_unsafe_crates:
            if (j + "/src") in i[0] or ("/" + j + "-") in i[0]:
                sum_tcb += i[1]
                # print(j, ";", i[0], ":", i[1])
                break

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
    # for i in sum_detail.items():
    #     print(i[0], ":", i[1])


if __name__ == "__main__":
    # Get home directory
    home_dir = os.path.expanduser("~")
    folder_path = f"tmp/all_nrf52840dk-thread-tutorial.ll"
    parse_llvm_ir(folder_path)
