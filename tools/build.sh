#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
version="${1:-29}"
case "$version" in 23|24|25|26|27|28|29) ;; *) exit 2 ;; esac
mkdir -p printable
# Invalidate stale success evidence before replacing exported geometry.
if [[ "$version" == 23 ]]; then rm -f docs/validation.json; else rm -f "docs/validation_v${version}.json"; fi
for part in g7_mount box lid lock_key universal_receiver male_fit_coupon hook_fit_coupon; do
    if [[ "$version" == 29 && "$part" == g7_mount ]]; then
        python tools/build_v29_mount.py
        continue
    fi
    format_args=()
    if [[ "$version" == 29 ]]; then format_args=(--export-format binstl); fi
    QT_QPA_PLATFORM=offscreen openscad --hardwarnings "${format_args[@]}" -o "printable/G7_Modular_v${version}_${part}.stl" -D "part=\"${part}\"" "cad/G7_Pro_Modular_v${version}.scad"
done
python tools/package_and_validate.py --design-version "$version"
