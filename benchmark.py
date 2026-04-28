from __future__ import annotations

import argparse
import csv
import gc
import os
import platform
import random
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import traceback
from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:
    import psutil
except ImportError:
    psutil = None

from py_algorithms import SORT_ALGORITHMS, get_algorithm_names
from py_algorithms.structures import LinkedList

ROOT = Path(__file__).resolve().parent
CPP_DIR = ROOT / "cpp_algorithms"
CPP_BIN_DIR = CPP_DIR / "bin"
EXEC_SUFFIX = ".exe" if os.name == "nt" else ""
TIMEOUT_SECONDS = 120  # 2 minutes

CSV_FIELDS = [
    "algorithm",
    "language",
    "size",
    "element_type",
    "distribution",
    "structure",
    "duration_seconds",
    "cpu_time_seconds",
    "memory_mb",
    "cpu_usage_percent_avg",
    "ram_usage_percent_avg",
    "repetition_count",
    "status",
    "notes",
]

SYSTEM_INFO_FIELDS = [
    "system_platform",
    "system_processor",
    "system_cores_logical",
    "system_cores_physical",
    "system_ram_gb",
    "benchmark_date",
]

SMALL_SIZES = [20, 30, 50, 100]
MEDIUM_SIZES = [1000, 5000, 10000, 50000]
LARGE_SIZES = [100000, 500000, 1000000, 5000000, 10000000]
EXTRA_LARGE_SIZES = [50000000, 100000000]
DEFAULT_SIZES = SMALL_SIZES + MEDIUM_SIZES + LARGE_SIZES
DISTRIBUTIONS = ["random", "sorted", "reverse", "almost_sorted", "half_sorted", "flat"]
ELEMENT_TYPES = ["int", "float", "string"]
STRUCTURES = ["array", "linked_list"]

CPP_ONLY_TYPES = {"int"}
CPP_ONLY_STRUCTURES = {"array"}

FAST_CPP_ALGORITHMS = {
    "bubble_sort": 5000,
    "gnome_sort": 5000,
    "comb_sort": 20000,
    "cocktail_shaker_sort": 20000,
    "odd_even_sort": 20000,
    "pancake_sort": 10000,
    "pigeonhole_sort": 50000,
    "stooge_sort": 50,
}

FAST_PY_ALGORITHMS = {
    "bubble_sort": 2000,
    "gnome_sort": 2000,
    "comb_sort": 5000,
    "cocktail_shaker_sort": 5000,
    "odd_even_sort": 5000,
    "pancake_sort": 2000,
    "pigeonhole_sort": 5000,
    "stooge_sort": 50,
}


def get_system_info() -> dict[str, Any]:
    """Collect detailed system information."""
    info = {
        "system_platform": f"{platform.system()} {platform.release()}",
        "system_processor": platform.processor() or "Unknown",
        "system_cores_logical": os.cpu_count() or 1,
        "system_cores_physical": psutil.cpu_count(logical=False) if psutil else os.cpu_count() or 1,
        "system_ram_gb": f"{psutil.virtual_memory().total / (1024**3):.2f}" if psutil else "Unknown",
    }
    return info


@dataclass
class AlgorithmConfig:
    name: str
    language: str
    max_size: int
    element_types: set[str]
    structures: set[str]
    cpp_executable: Path | None = None
    function: callable | None = None


@dataclass
class ResourceMonitor:
    """Monitors CPU and RAM usage during execution."""
    cpu_samples: list[float]
    ram_samples: list[float]
    stop_flag: threading.Event

    def start_monitoring(self, process: Any = None):
        """Start monitoring resources in background thread."""
        def monitor():
            while not self.stop_flag.is_set():
                if psutil:
                    try:
                        if process:
                            cpu_pct = process.cpu_percent(interval=0.1)
                            mem_info = process.memory_info()
                            allocated_mb = mem_info.rss / (1024 * 1024)
                        else:
                            cpu_pct = psutil.cpu_percent(interval=0.1)
                            allocated_mb = psutil.virtual_memory().percent
                        self.cpu_samples.append(cpu_pct)
                        self.ram_samples.append(allocated_mb)
                    except (psutil.NoSuchProcess, Exception):
                        pass
                time.sleep(0.1)

        thread = threading.Thread(target=monitor, daemon=True)
        thread.start()

    def get_averages(self) -> tuple[float, float]:
        """Get average CPU and RAM usage."""
        cpu_avg = sum(self.cpu_samples) / len(self.cpu_samples) if self.cpu_samples else 0.0
        ram_avg = sum(self.ram_samples) / len(self.ram_samples) if self.ram_samples else 0.0
        return cpu_avg, ram_avg

    def stop_monitoring(self):
        """Stop monitoring."""
        self.stop_flag.set()


def _safe_float(value: int) -> float:
    return float(value) if isinstance(value, int) else value


def _random_ints(size: int) -> list[int]:
    return [random.randint(-1_000_000, 1_000_000) for _ in range(size)]


def _random_floats(size: int) -> list[float]:
    return [random.uniform(-1_000_000.0, 1_000_000.0) for _ in range(size)]


def _random_strings(size: int) -> list[str]:
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    return ["".join(random.choices(alphabet, k=random.randint(3, 10))) for _ in range(size)]


def _almost_sorted(values: list[Any]) -> list[Any]:
    if not values:
        return []
    sorted_values = sorted(values)
    count_swaps = max(1, int(len(sorted_values) * 0.02))
    for _ in range(count_swaps):
        i = random.randrange(len(sorted_values))
        j = random.randrange(len(sorted_values))
        sorted_values[i], sorted_values[j] = sorted_values[j], sorted_values[i]
    return sorted_values


def _half_sorted(values: list[Any]) -> list[Any]:
    if not values:
        return []
    midpoint = len(values) // 2
    sorted_part = sorted(values[:midpoint])
    random_part = values[midpoint:]
    random.shuffle(random_part)
    return sorted_part + random_part


def _flat(values: list[Any]) -> list[Any]:
    if not values:
        return []
    palette = random.sample(values, min(8, len(values)))
    return [random.choice(palette) for _ in range(len(values))]


def generate_data(size: int, element_type: str, distribution: str) -> list[Any]:
    if element_type == "int":
        values = _random_ints(size)
    elif element_type == "float":
        values = _random_floats(size)
    else:
        values = _random_strings(size)

    if distribution == "sorted":
        values = sorted(values)
    elif distribution == "reverse":
        values = sorted(values, reverse=True)
    elif distribution == "almost_sorted":
        values = _almost_sorted(values)
    elif distribution == "half_sorted":
        values = _half_sorted(values)
    elif distribution == "flat":
        values = _flat(values)
    return values


def _measure_resources(process: Any = None) -> tuple[float, float]:
    if not psutil:
        return 0.0, 0.0
    if process is None:
        process = psutil.Process()
    try:
        times = process.cpu_times()
        memory = process.memory_info().rss / 1024 / 1024
        return times.user + times.system, memory
    except (psutil.NoSuchProcess, Exception):
        return 0.0, 0.0


def run_python_algorithm(func: callable, values: list[Any], structure: str) -> tuple[float, float, float, float, float, list[Any], str]:
    """Run Python algorithm with timeout and resource monitoring.

    Returns: (duration, cpu_time, memory_mb, cpu_usage_avg, ram_usage_avg, result, status)
    Status: "completed", "timeout", "error"
    """
    data = list(values)
    if structure == "linked_list":
        linked = LinkedList.from_list(data)
        data = linked.to_list()

    # Setup resource monitoring
    monitor = ResourceMonitor([], [], threading.Event())
    monitor.start_monitoring(psutil.Process() if psutil else None)

    start_cpu, start_mem = _measure_resources(None)
    start = time.perf_counter()
    result = None
    status = "completed"
    timeout_event = threading.Event()

    def run_func():
        nonlocal result
        try:
            result = func(data)
        except Exception as e:
            nonlocal status
            status = f"error: {str(e)[:50]}"

    thread = threading.Thread(target=run_func, daemon=False)
    thread.start()
    thread_alive = thread.join(timeout=TIMEOUT_SECONDS)

    if thread_alive is None and thread.is_alive():
        status = "timeout"
        result = []

    duration = time.perf_counter() - start
    end_cpu, end_mem = _measure_resources(None)
    cpu_time = max(0.0, end_cpu - start_cpu)
    memory_mb = max(start_mem, end_mem)

    monitor.stop_monitoring()
    cpu_usage_avg, ram_usage_avg = monitor.get_averages()

    return duration, cpu_time, memory_mb, cpu_usage_avg, ram_usage_avg, result or [], status


def run_cpp_algorithm(executable: Path, values: list[int]) -> tuple[float, float, float, float, float, list[int], str]:
    """Run C++ algorithm with timeout and resource monitoring.

    Returns: (duration, cpu_time, memory_mb, cpu_usage_avg, ram_usage_avg, result, status)
    Status: "completed", "timeout", "error"
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = Path(tmpdir) / "input.txt"
        output_path = Path(tmpdir) / "output.txt"
        input_path.write_text("\n".join(str(x) for x in values), encoding="utf-8")

        # Setup resource monitoring
        monitor = ResourceMonitor([], [], threading.Event())
        proc = None
        status = "completed"

        try:
            start = time.perf_counter()
            process = subprocess.Popen(
                [str(executable), str(input_path), str(output_path)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            if psutil:
                proc = psutil.Process(process.pid)
                monitor.start_monitoring(proc)

            stream_out, stream_err = process.communicate(timeout=TIMEOUT_SECONDS)
            duration = time.perf_counter() - start
        except subprocess.TimeoutExpired:
            process.kill()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
            duration = time.perf_counter() - start
            status = "timeout"
            stream_out, stream_err = b"", b""
        except Exception as e:
            status = f"error: {str(e)[:50]}"
            duration = time.perf_counter() - start
            stream_out, stream_err = b"", b""

        monitor.stop_monitoring()
        cpu_usage_avg, ram_usage_avg = monitor.get_averages()

        cpu_time = 0.0
        memory_mb = 0.0

        if proc and status == "completed":
            try:
                times = proc.cpu_times()
                cpu_time = times.user + times.system
                mem_info = proc.memory_info()
                memory_mb = mem_info.rss / (1024 * 1024)
            except (psutil.NoSuchProcess, Exception):
                pass

        if status != "completed":
            return duration, cpu_time, memory_mb, cpu_usage_avg, ram_usage_avg, [], status

        if process.returncode != 0 and status == "completed":
            return duration, cpu_time, memory_mb, cpu_usage_avg, ram_usage_avg, [], f"error: exit code {process.returncode}"

        try:
            raw = output_path.read_text(encoding="utf-8").strip()
            result = [int(x) for x in raw.split()] if raw else []
        except Exception:
            result = []

        return duration, cpu_time, memory_mb, cpu_usage_avg, ram_usage_avg, result, status


def collect_cpp_executables() -> dict[str, Path]:
    executables = {}
    search_paths = [CPP_BIN_DIR, CPP_DIR]
    for path in search_paths:
        if not path.exists():
            continue
        for exe in path.glob(f"*{EXEC_SUFFIX}"):
            if exe.is_file():
                name = exe.stem
                executables[name] = exe
    return executables


def make_algorithm_configs() -> list[AlgorithmConfig]:
    configs: list[AlgorithmConfig] = []
    cpp_executables = collect_cpp_executables()
    for name, func in SORT_ALGORITHMS.items():
        configs.append(
            AlgorithmConfig(
                name=name,
                language="python",
                max_size=1_000_000 if name not in FAST_PY_ALGORITHMS else FAST_PY_ALGORITHMS[name],
                element_types=set(ELEMENT_TYPES),
                structures=set(STRUCTURES),
                function=func,
            )
        )
    for name, exe in cpp_executables.items():
        if name in SORT_ALGORITHMS:
            configs.append(
                AlgorithmConfig(
                    name=name,
                    language="cpp",
                    max_size=50_000_000 if name not in FAST_CPP_ALGORITHMS else FAST_CPP_ALGORITHMS[name],
                    element_types=CPP_ONLY_TYPES,
                    structures=CPP_ONLY_STRUCTURES,
                    cpp_executable=exe,
                )
            )
    return configs


def write_csv_header(path: Path, system_info: dict[str, Any]) -> None:
    """Write CSV header with system info as comments."""
    with path.open("w", newline="", encoding="utf-8") as csvfile:
        # Write system info as comments
        csvfile.write("# SYSTEM INFORMATION\n")
        for key, value in system_info.items():
            csvfile.write(f"# {key}: {value}\n")
        csvfile.write("# END SYSTEM INFORMATION\n\n")

        writer = csv.DictWriter(csvfile, fieldnames=CSV_FIELDS)
        writer.writeheader()


def append_csv_row(path: Path, row: dict[str, Any]) -> None:
    with path.open("a", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=CSV_FIELDS)
        writer.writerow(row)


def estimate_size(name: str, requested_size: int) -> int:
    limit = FAST_PY_ALGORITHMS.get(name, 1_000_000)
    return min(requested_size, limit)


def get_benchmark_sizes(max_size: int) -> list[int]:
    sizes = [s for s in DEFAULT_SIZES if s <= max_size]
    if max_size >= EXTRA_LARGE_SIZES[0]:
        sizes.extend([s for s in EXTRA_LARGE_SIZES if s <= max_size])
    return sizes


def get_repeat_count(size: int, language: str) -> int:
    # Single run per configuration for speed
    return 1


def run_benchmark(csv_path: Path, keep_temp: bool, max_size: int) -> None:
    """Run benchmarks and track overall timing."""
    system_info = get_system_info()
    print("\n" + "=" * 80)
    print("SYSTEM INFORMATION")
    print("=" * 80)
    for key, value in system_info.items():
        print(f"  {key}: {value}")
    print("=" * 80 + "\n")

    configs = make_algorithm_configs()
    write_csv_header(csv_path, system_info)
    sizes = get_benchmark_sizes(max_size)

    benchmark_start = time.time()
    total_tests = 0
    completed_tests = 0
    timeout_tests = 0

    for config in configs:
        allowed_sizes = [s for s in sizes if s <= config.max_size]
        if not allowed_sizes:
            continue
        for size in allowed_sizes:
            for element_type in sorted(config.element_types):
                for distribution in DISTRIBUTIONS:
                    for structure in sorted(config.structures):
                        if config.language == "cpp" and element_type != "int":
                            continue
                        if config.language == "cpp" and structure != "array":
                            continue

                        repeat = get_repeat_count(size, config.language)
                        total_tests += repeat

                        total_duration = 0.0
                        total_cpu = 0.0
                        max_memory = 0.0
                        total_cpu_usage = 0.0
                        total_ram_usage = 0.0
                        verified_all = True
                        final_status = "completed"
                        run_completed = 0

                        test_start = time.time()

                        for run_index in range(repeat):
                            values = generate_data(size, element_type, distribution)

                            try:
                                if config.language == "python":
                                    duration, cpu_time, memory_mb, cpu_usage, ram_usage, result, status = run_python_algorithm(
                                        config.function, values, structure
                                    )
                                    verified = result == sorted(values) if status == "completed" else False
                                else:
                                    duration, cpu_time, memory_mb, cpu_usage, ram_usage, result, status = run_cpp_algorithm(
                                        config.cpp_executable, [int(x) for x in values]
                                    )
                                    verified = result == sorted(values) if status == "completed" else False

                                total_duration += duration
                                total_cpu += cpu_time
                                max_memory = max(max_memory, memory_mb)
                                total_cpu_usage += cpu_usage
                                total_ram_usage += ram_usage
                                verified_all = verified_all and verified
                                if status == "completed":
                                    run_completed += 1
                                    completed_tests += 1
                                elif status == "timeout":
                                    timeout_tests += 1
                                    final_status = "timeout"

                                if status != "completed":
                                    final_status = status

                            except Exception as e:
                                final_status = f"error: {str(e)[:50]}"
                                duration = 0.0
                                cpu_time = 0.0
                                memory_mb = 0.0
                                cpu_usage = 0.0
                                ram_usage = 0.0

                            if run_index < repeat - 1:
                                gc.collect()

                        test_end = time.time()
                        test_duration = test_end - test_start

                        average_duration = total_duration / repeat if repeat > 0 else 0.0
                        average_cpu = total_cpu / repeat if repeat > 0 else 0.0
                        average_cpu_usage = total_cpu_usage / repeat if repeat > 0 else 0.0
                        average_ram_usage = total_ram_usage / repeat if repeat > 0 else 0.0

                        notes = "verified" if (verified_all and final_status == "completed") else final_status
                        if run_completed < repeat:
                            notes = f"{run_completed}/{repeat} completed, {repeat - run_completed} failed/timeout"

                        append_csv_row(
                            csv_path,
                            {
                                "algorithm": config.name,
                                "language": config.language,
                                "size": size,
                                "element_type": element_type,
                                "distribution": distribution,
                                "structure": structure,
                                "duration_seconds": f"{average_duration:.6f}",
                                "cpu_time_seconds": f"{average_cpu:.6f}",
                                "memory_mb": f"{max_memory:.3f}",
                                "cpu_usage_percent_avg": f"{average_cpu_usage:.2f}",
                                "ram_usage_percent_avg": f"{average_ram_usage:.2f}",
                                "repetition_count": repeat,
                                "status": final_status,
                                "notes": notes,
                            },
                        )
                        status_symbol = "[OK]" if final_status == "completed" else "[FAIL]"
                        print(
                            f"{status_symbol} {config.language}:{config.name} size={size} type={element_type} dist={distribution} "
                            f"struct={structure} avg_time={average_duration:.4f}s cpu={average_cpu_usage:.1f}% ram={average_ram_usage:.1f}% "
                            f"runs={repeat} {final_status}"
                        )
                        gc.collect()

    benchmark_end = time.time()
    total_benchmark_time = benchmark_end - benchmark_start

    print("\n" + "=" * 80)
    print("BENCHMARK SUMMARY")
    print("=" * 80)
    print(f"  Total time: {total_benchmark_time:.2f} seconds ({total_benchmark_time/60:.2f} minutes)")
    print(f"  Total tests: {total_tests}")
    print(f"  Completed: {completed_tests}")
    print(f"  Timeouts: {timeout_tests}")
    print(f"  Success rate: {(completed_tests/total_tests*100):.1f}%")
    print("=" * 80 + "\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Benchmark Python and C++ sorting algorithms across data shapes and sizes."
    )
    parser.add_argument(
        "--csv",
        default="benchmark_results.csv",
        help="CSV file to write results into",
    )
    parser.add_argument(
        "--max-size",
        type=int,
        default=100000000,
        help="Maximum list size to generate for benchmarks",
    )
    parser.add_argument(
        "--keep-temp",
        action="store_true",
        help="Do not remove temporary files from C++ benchmark runs",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if psutil is None:
        print("[WARNING] psutil is not installed.")
        print("   Install it with: pip install psutil")
        print("   Resource monitoring will be unavailable.\n")
    run_benchmark(Path(args.csv), args.keep_temp, args.max_size)
    print(f"\n[SUCCESS] Benchmark complete. Results saved to {args.csv}")


if __name__ == "__main__":
    main()
