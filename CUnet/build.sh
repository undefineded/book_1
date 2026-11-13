#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 || $# -gt 2 ]]; then
  echo "Usage: bash CUnet/build.sh /path/to/ncnn-sdk [build-directory]" >&2
  exit 2
fi

project_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
ncnn_root="$(cd -- "$1" && pwd)"
build_dir="${2:-$project_dir/build}"

[[ -f "$ncnn_root/include/ncnn/net.h" ]] || {
  echo "Missing ncnn header: $ncnn_root/include/ncnn/net.h" >&2
  exit 2
}
mkdir -p -- "$build_dir"
"${CXX:-c++}" -std=c++17 -O3 -fopenmp -pthread \
  "$project_dir/src/cpu_upscale.cpp" \
  -I"$ncnn_root/include/ncnn" -L"$ncnn_root/lib" \
  -Wl,-rpath,"$ncnn_root/lib" -lncnn \
  -o "$build_dir/cpu_upscale"
echo "Built $build_dir/cpu_upscale"
