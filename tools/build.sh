#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p printable
# Invalidate stale success evidence before replacing exported geometry.
rm -f docs/validation.json
for part in g7_mount box lid lock_key universal_receiver male_fit_coupon hook_fit_coupon; do
    QT_QPA_PLATFORM=offscreen openscad --hardwarnings -o "printable/G7_Modular_v23_${part}.stl" -D "part=\"${part}\"" cad/G7_Pro_Modular_v23.scad
done
python tools/package_and_validate.py
