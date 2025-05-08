import re
import os


all_unsafe_crates = [
    "memory",
    "atomic_linked_list",
    "boot_info",
    "kernel_config",
    "memory_structs",
    "derive_more",
    "proc_macro2",
    "unicode_ident",
    "quote",
    "paste",
    "range_inclusive",
    "zerocopy",
    "byteorder",
    "zerocopy_derive",
    "synstructure",
    "unicode_xid",
    "multiboot2",
    "uefi_bootloader_api",
    "frame_allocator",
    "intrusive_collections",
    "static_assertions",
    "lazy_static",
    "memory_aarch64",
    "cortex_a",
    "tock_registers",
    "pte_flags",
    "memory_x86_64",
    "x86_64",
    "rustversion",
    "no_drop",
    "owned_borrowed_trait",
    "page_allocator",
    "page_table_entry",
    "sync_irq",
    "irq_safety",
    "sync",
    "xmas_elf",
    "zero",
    "crossbeam_utils",
    "apic",
    "msr",
    "pit_clock_basic",
    "port_io",
    "raw_cpuid",
    "pic",
    "cls_allocator",
    "cpu",
    "arm_boards",
    "crate_metadata",
    "cow_arc",
    "dereffer",
    "crate_metadata_serde",
    "serde",
    "serde_derive",
    "fs_node",
    "io",
    "core2",
    "memchr",
    "delegate",
    "lockable",
    "goblin",
    "plain",
    "scroll",
    "qp_trie",
    "new_debug_unreachable",
    "unreachable",
    "void",
    "str_ref",
    "local_storage_initializer",
    "rangemap",
    "sync_spin",
    "early_tls",
    "interrupts",
    "early_printer",
    "font",
    "page_attribute_table",
    "modular_bitfield",
    "modular_bitfield_impl",
    "vga_buffer",
    "exceptions_early",
    "gdt",
    "tss",
    "locked_idt",
    "mod_mgmt",
    "bincode",
    "bincode_derive",
    "virtue",
    "bootloader_modules",
    "const_format",
    "const_format_proc_macros",
    "cpio_reader",
    "crate_name_utils",
    "itertools",
    "either",
    "path",
    "root",
    "cstr_core",
    "cty",
    "lz4_flex",
    "memfs",
    "rustc_demangle",
    "vfs_node",
    "generic_timer_aarch64",
    "time",
    "gic",
    "interrupt_controller",
    "acpi",
    "acpi_table",
    "sdt",
    "acpi_table_handler",
    "dmar",
    "fadt",
    "hpet",
    "madt",
    "ioapic",
    "rsdt",
    "waet",
    "iommu",
    "rsdp",
    "task",
    "cls",
    "cls_macros",
    "preemption",
    "context_switch",
    "context_switch_avx",
    "context_switch_regular",
    "context_switch_sse",
    "environment",
    "stack",
    "sync_preemption",
    "task_struct",
    "waker_generic",
    "spawn",
    "catch_unwind",
    "unwind",
    "external_unwind_info",
    "fallible_iterator",
    "gimli",
    "debugit",
    "fault_crate_swap",
    "crate_swap",
    "by_address",
    "fault_log",
    "app_io",
    "logger",
    "serial_port_basic",
    "uart_pl011",
    "stdio",
    "keycodes_ascii",
    "num_enum",
    "num_enum_derive",
    "sync_block",
    "mpmc_queue",
    "scheduler",
    "sleep",
    "wait_queue",
    "tty",
    "sync_channel",
    "mpmc",
    "scheduler_epoch",
    "scheduler_priority",
    "scheduler_round_robin",
    "thread_local_macro",
    "ata",
    "pci",
    "storage_device",
    "downcast_rs",
    "block_allocator",
    "linked_list_allocator",
    "embedded_hal",
    "noline",
    "heapless",
    "atomic_polyfill",
    "critical_section",
    "cortex_m",
    "bitfield",
    "volatile_register",
    "vcell",
    "riscv",
    "riscv_target",
    "regex",
    "aho_corasick",
    "regex_syntax",
    "hash32",
    "stable_deref_trait",
    "rand",
    "rand_core",
    "rand_chacha",
    "ppv_lite86",
    "rdrand",
    "tsc",
    "ixgbe",
    "intel_ethernet",
    "net",
    "nic_buffers",
    "random",
    "smoltcp",
    "defmt",
    "defmt_macros",
    "defmt_parser",
    "proc_macro_error",
    "proc_macro_error_attr",
    "version_check",
    "managed",
    "nic_initialization",
    "nic_queues",
    "physical_nic",
    "virtual_nic",
    "keyboard",
    "event_types",
    "mouse_data",
    "shapes",
    "once_cell",
    "ps2",
    "libm",
    "mlx_ethernet",
    "dfqueue",
    "exceptions_full",
    "debug_info",
    "pmu_x86",
    "pit_clock",
    "signal_handler",
    "stack_trace",
    "tlb_shootdown",
    "qemu_exit",
    "multiple_heaps",
    "heap",
    "slabmalloc",
    "slabmalloc_safe",
    "slabmalloc_unsafe",
    "httparse",
    "percent_encoding",
    "block_buffer",
    "generic_array",
    "typenum",
    "simd_personality",
    "futures_channel",
    "futures_core",
    "futures_sink",
    "futures_task",
    "futures_util",
    "futures_macro",
    "pin_project_lite",
    "pin_utils",
    "nano_core",
    "captain",
    "console",
    "hull",
    "serial_port",
    "deferred_interrupt_tasks",
    "device_manager",
    "e1000",
    "fatfs",
    "mlx5",
    "mouse",
    "storage_manager",
    "first_application",
    "hello",
    "qemu_test",
    "shell",
    "libterm",
    "color",
    "displayable",
    "framebuffer",
    "multicore_bringup",
    "ap_start",
    "psci",
    "framebuffer_drawer",
    "framebuffer_printer",
    "text_display",
    "window",
    "window_inner",
    "window_manager",
    "compositor",
    "framebuffer_compositor",
    "ota_update_client",
    "http_client",
    "sha3",
    "digest",
    "crypto_common",
    "keccak",
    "task_fs",
    "memory_initialization",
    "panic_entry",
    "panic_wrapper",
    "stack_trace_frame_pointers",
    "state_store",
    "vte",
    "arrayvec",
    "utf8parse",
    "vte_generate_state_changes",
    "wasmi",
    "memory_units",
    "num_rational",
    "autocfg",
    "num_integer",
    "num_traits",
    "parity_wasm",
    "wasmi_validation",
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
    sum_kernel = 0
    sum_tcb = 0
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
            # if "/library/core/src" in file_name or "/library/alloc/src" in file_name:
            #     continue
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
            # if "/library/core/src" in file_name or "/library/alloc/src" in file_name:
            #     continue
            key = extract_path(file_name + str(scope[1]["line"]))
            if key in count_set:
                continue
            count_set[key] = 1
            sum += 1
            if scope[1]["func"] != None:
                file_name = file_name + " " + scope[1]["func"]
            sum_detail[file_name] = sum_detail.get(file_name, 0) + 1

    print()
    print("----------------------------------")

    print("Total: ", sum)
    # sorted_dict = dict(sorted(sum_detail.items(), key=lambda x: x[1], reverse=True))
    for i in sum_detail.items():
        # print(i[0],":", i[1])
        sum_kernel += i[1]
        for j in all_unsafe_crates:
            if (j + "/src") in i[0] or ("/" + j + "-") in i[0]:
                sum_tcb += i[1]
                break
    print("----------------------------------")
    print("TCB: ", sum_tcb)
    print("----------------------------------")


if __name__ == "__main__":
    folder_path = "tmp/theseus/"
    parse_llvm_ir(folder_path)
