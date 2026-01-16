#!/usr/bin/env python3
"""Traverse actions/ and create annotated YAML copies under desc-actions/.
Adds a <field>_info map after each field with description, type and required.
"""
import sys
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
ACTIONS = ROOT / 'actions'
OUT = ROOT / 'desc-actions'

if not ACTIONS.exists():
    print('No actions directory found at', ACTIONS)
    sys.exit(1)


def infer_type(v):
    if isinstance(v, bool):
        return 'boolean'
    if isinstance(v, int) and not isinstance(v, bool):
        return 'integer'
    if isinstance(v, float):
        return 'number'
    if isinstance(v, dict):
        return 'object'
    if isinstance(v, list):
        return 'array'
    if v is None:
        return 'null'
    return 'string'


def annotate(node):
    if isinstance(node, dict):
        new = {}
        for k, v in node.items():
            new[k] = annotate(v)
            info = {
                'description': f'{k} field',
                'type': infer_type(v),
                'required': True if k in ('apiVersion','kind','metadata','spec') else False
            }
            new[f'{k}_info'] = info
        return new
    elif isinstance(node, list):
        return [annotate(i) for i in node]
    else:
        return node


created = []
errors = []
for src in ACTIONS.rglob('*.yaml'):
    rel = src.relative_to(ACTIONS)
    stem = src.stem
    out_dir = OUT / rel.parent / stem
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / src.name

    text = src.read_text(encoding='utf-8')
    try:
        docs = list(yaml.safe_load_all(text))
    except Exception as e:
        # write original content if parsing fails
        out_file.write_text(text, encoding='utf-8')
        errors.append((str(src), str(e)))
        created.append(str(out_file))
        continue

    annotated = []
    for d in docs:
        if d is None:
            annotated.append(None)
        else:
            annotated.append(annotate(d))

    out_file.write_text(yaml.safe_dump_all(annotated, sort_keys=False, default_flow_style=False), encoding='utf-8')
    created.append(str(out_file))

print(f'Created {len(created)} files under {OUT}')
if errors:
    print('\nErrors:')
    for s,e in errors:
        print('-', s, e)
