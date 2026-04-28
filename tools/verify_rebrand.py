from pathlib import Path
import re

root = Path(__file__).resolve().parent.parent
patterns = [r'Warta Janten', r'WartaJanten', r'wartajanten', r'WartaJanten33@gmail.com', r'#065F46', r'#1E3A5F', r'#022C22', r'logo\.png']
regexes = [re.compile(p) for p in patterns]
exclude_dirs = {'node_modules', '.git'}

for path in sorted(root.rglob('*')):
    if not path.is_file():
        continue
    if any(part in exclude_dirs for part in path.parts):
        continue
    try:
        text = path.read_text(encoding='utf-8', errors='ignore')
    except Exception:
        continue
    for pat, regex in zip(patterns, regexes):
        for i, line in enumerate(text.splitlines(), start=1):
            if regex.search(line):
                print(f'{path.relative_to(root)}: {pat} @ {i}: {line.strip()}')
                break
