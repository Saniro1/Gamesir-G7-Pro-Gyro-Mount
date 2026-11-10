"""Package source, tested models, docs and unchanged originals; omit local tools."""
from pathlib import Path
import zipfile,argparse

parser=argparse.ArgumentParser()
parser.add_argument('--design-version',type=int,choices=[23,24,25,26],default=26)
args=parser.parse_args()
root = Path(__file__).resolve().parents[1]
paths = [root/'README.md', root/'.gitignore']
for name in ('cad', 'printable', 'assemblies', 'docs', 'tools', 'originals', 'slicer'):
    paths.extend(p for p in (root/name).rglob('*') if p.is_file() and '__pycache__' not in p.parts)
(root/'releases').mkdir(exist_ok=True)
out = root/'releases'/f'G7_Pro_Modular_Reversible_Box2_V{args.design_version}_Complete.zip'
with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
    for p in sorted(paths):
        z.write(p, p.relative_to(root))
with zipfile.ZipFile(out) as z:
    assert z.testzip() is None
print(out)
