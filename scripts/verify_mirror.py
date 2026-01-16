from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
ACTIONS = ROOT / 'actions'
OUT = ROOT / 'desc-actions'
missing = []
for src in ACTIONS.rglob('*.yaml'):
    rel = src.relative_to(ACTIONS)
    stem = src.stem
    out_file = OUT / rel.parent / stem / src.name
    if not out_file.exists():
        missing.append(str(rel))
print(f'Total actions YAMLs: {len(list(ACTIONS.rglob("*.yaml")))}')
print(f'Total desc-actions YAMLs: {len(list(OUT.rglob("*.yaml")))}')
if missing:
    print('Missing annotated files for:')
    for m in missing:
        print('-', m)
else:
    print('All action YAMLs have annotated copies under desc-actions.')
