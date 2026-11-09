#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
version="${1:-24}"
case "$version" in 23|24) ;; *) exit 2 ;; esac
mkdir -p printable
# Invalidate stale success evidence before replacing exported geometry.
if [[ "$version" == 24 ]]; then rm -f docs/validation_v24.json; else rm -f docs/validation.json; fi
for part in g7_mount box lid lock_key universal_receiver male_fit_coupon hook_fit_coupon; do
    QT_QPA_PLATFORM=offscreen openscad --hardwarnings -o "printable/G7_Modular_v${version}_${part}.stl" -D "part=\"${part}\"" "cad/G7_Pro_Modular_v${version}.scad"
done
python tools/package_and_validate.py --design-version "$version"
