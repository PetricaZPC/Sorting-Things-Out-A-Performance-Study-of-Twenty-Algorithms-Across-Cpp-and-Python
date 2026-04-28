from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CPP_DIR = ROOT / "cpp_algorithms"
BIN_DIR = CPP_DIR / "bin"
BIN_DIR.mkdir(exist_ok=True)

CPP_SOURCES = list(CPP_DIR.glob("*.cpp"))

COMPILER = shutil.which("g++") or shutil.which("clang++") or shutil.which("cl")
if COMPILER is None:
    raise SystemExit("No supported C++ compiler found. Install g++, clang++, or cl.")

IS_MSVC = COMPILER.lower().endswith("cl")
IS_MINGW = os.name == "nt" and "mingw" in COMPILER.lower()


def compile_source(source: Path) -> None:
    output = BIN_DIR / (source.stem + (".exe" if os.name == "nt" else ""))
    if IS_MSVC:
        flags = ["/O2", "/std:c++17", "/openmp"]
        cmd = [COMPILER, str(source), "/Fe:" + str(output)] + flags
    else:
        flags = ["-O3", "-std=c++17", "-march=native"]
        if not IS_MINGW:
            flags.append("-fopenmp")
        else:
            print("Warning: MinGW detected. Building without OpenMP to avoid missing pthread/openmp libraries.")
        cmd = [COMPILER, str(source), "-o", str(output)] + flags
    print("Compiling", source.name)
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr)
        raise SystemExit(f"Compilation failed for {source.name}")


def main() -> None:
    print(f"Using compiler: {COMPILER}")
    for source in CPP_SOURCES:
        compile_source(source)
    print(f"Compiled {len(CPP_SOURCES)} C++ sources into {BIN_DIR}")


if __name__ == "__main__":
    main()
