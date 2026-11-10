#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
version="${1:-32}"
case "$version" in 23|24|25|26|27|28|29|30|31|32) ;; *) exit 2 ;; esac
mkdir -p printable
# Invalidate stale success evidence before replacing exported geometry.
if [[ "$version" == 23 ]]; then rm -f docs/validation.json; else rm -f "docs/validation_v${version}.json"; fi
if [[ "$version" == 32 ]]; then
    python tools/build_v32.py
    python tools/package_and_validate.py --design-version 32
    exit
fi
if [[ "$version" == 31 ]]; then
    # V31 changes only disposable supports in the slicer project.
    for part in g7_mount box lid lock_key universal_receiver male_fit_coupon hook_fit_coupon; do
        cp "printable/G7_Modular_v30_${part}.stl" "printable/G7_Modular_v31_${part}.stl"
    done
    python tools/package_and_validate.py --design-version 31
    exit
fi
for part in g7_mount box lid lock_key universal_receiver male_fit_coupon hook_fit_coupon; do
    if [[ "$version" -ge 29 && "$part" == g7_mount ]]; then
        python tools/build_v29_mount.py --design-version "$version"
        continue
    fi
    format_args=()
    if [[ "$version" -ge 29 ]]; then format_args=(--export-format binstl); fi
    QT_QPA_PLATFORM=offscreen openscad --hardwarnings "${format_args[@]}" -o "printable/G7_Modular_v${version}_${part}.stl" -D "part=\"${part}\"" "cad/G7_Pro_Modular_v${version}.scad"
done
python tools/package_and_validate.py --design-version "$version"
