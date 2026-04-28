import json, os, re, shutil
from pathlib import Path
base = Path('.')
backup_src = base / 'articles.json'
backup_dst = base / 'articles.json.bak'
if backup_src.exists():
    shutil.copyfile(backup_src, backup_dst)

file_exts = {'.html', '.css', '.md', '.toml', '.json'}
files = [p for p in base.rglob('*') if p.suffix.lower() in file_exts and p.is_file()]
main_pages = sum(1 for p in files if p.parent == base and p.suffix.lower() == '.html')
article_pages = sum(1 for p in files if 'article' in p.parts and p.suffix.lower() == '.html')
css_files = sum(1 for p in files if p.suffix.lower() in {'.css'})
package_files = sum(1 for p in files if p.name in {'package.json','package-lock.json'} or (p.parent.name == 'tools' and p.name in {'package.json','package-lock.json'}))
docs_files = sum(1 for p in files if p.name in {'AUTOMATION_README.md','GOOGLE_DRIVE_GUIDE.md','netlify.toml'})

replacements = [
    (r'\bFokus\s?Janten\b', 'Arah Berita'),
    (r'\bFokusjanten\b', 'ArahBerita'),
    (r'\bfokusjanten\b', 'Arahberita'),
    (r'\bFokusJanten\b', 'ArahBerita'),
    (r'fokusjanten@gmail\.com', 'ArahBerita@gmail.com'),
]
encodings = {
    '\u201c': '"', '\u201d': '"', '\u2018': "'", '\u2019': "'",
    '\u2013': '-', '\u2014': '-', '\uFFFD': ' ', '\u00A0': ' '
}
color_map = {
    '#0EA5E9': '#166534',
    '#22C55E': '#2D5016',
    '#0F172A': '#052E16',
    '#0F766E': '#052E16',
    '#ffc107': '#166534',
    '#FFC107': '#166534',
    '#ffcc00': '#166534',
    '#FFCC00': '#166534',
    '#fc0': '#166534',
    '#b38f00': '#2D5016',
    '#ba8b00': '#2D5016',
    '#13191d': '#052E16',
    '#134E4A': '#052E16',
    '#19692c': '#052E16',
}
file_changes = set()
for p in files:
    text = p.read_text(encoding='utf-8', errors='replace')
    original = text
    for old, new in replacements:
        text = re.sub(old, new, text)
    for old, new in encodings.items():
        text = text.replace(old, new)
    for old, new in color_map.items():
        text = text.replace(old, new)
    if p.name in {'style.css','style.min.css'}:
        text = text.replace('  --primary: #0EA5E9;', '  --primary: #166534;')
        text = text.replace('  --secondary: #22C55E;', '  --secondary: #2D5016;')
        text = text.replace('  --dark: #0F172A;', '  --dark: #052E16;')
    text = text.replace('color: #0EA5E9;', 'color: #166534;')
    text = text.replace('color: #22C55E;', 'color: #2D5016;')
    text = text.replace('FOKUS<span style="color: #22C55E; font-weight: normal; font-size: 18px; margin-left: 2px;">JANTEN</span>', 'ARAH<span style="color: #2D5016; font-weight: normal; font-size: 18px; margin-left: 2px;">BERITA</span>')
    if p.name == 'package.json' and p.parent == base:
        text = text.replace('"name": "fokusjanten"', '"name": "arahberita"')
    if p.name == 'package.json' and p.parent.name == 'tools':
        text = text.replace('"description": "Generator artikel otomatis dari Google Sheets untuk Fokus Janten"', '"description": "Generator artikel otomatis dari Google Sheets untuk Arah Berita"')
        text = text.replace('"author": "Fokus Janten Team"', '"author": "Arah Berita Team"')
        text = text.replace('"fokusjanten"', '"arahberita"')
    if p.name == 'netlify.toml':
        text = text.replace('Deploy configuration for Fokus Janten', 'Deploy configuration for Arah Berita')
        text = text.replace('/fokusjanten/', '/arahberita/')
    if p.name == 'deploycPanel.yml':
        text = text.replace('/fokusjanten/', '/arahberita/')
    if p.name == 'sites-config.json':
        text = text.replace('"siteName": "Fokus Janten"', '"siteName": "Arah Berita"')
        text = text.replace('"email": "fokusjanten@gmail.com"', '"email": "ArahBerita@gmail.com"')
        text = text.replace('"socialHandle": "fokusjanten"', '"socialHandle": "Arahberita"')
        text = text.replace('"primary": "#0EA5E9"', '"primary": "#166534"')
        text = text.replace('"dark": "#0F172A"', '"dark": "#052E16"')
        text = text.replace('"secondary": "#22C55E"', '"secondary": "#2D5016"')
    if p.suffix.lower() in {'.md', '.html', '.toml', '.json'}:
        text = text.replace('Fokus Janten', 'Arah Berita')
        text = text.replace('fokusjanten', 'Arahberita')
        text = text.replace('Fokusjanten', 'ArahBerita')
        text = text.replace('FokusJanten', 'ArahBerita')
    if text != original:
        p.write_text(text, encoding='utf-8')
        file_changes.add(str(p))
for p in files:
    if p.suffix.lower() == '.html':
        content = p.read_text(encoding='utf-8', errors='replace')
        updated = content.replace('src="../img/logo.png"', '')
        updated = updated.replace('src="img/logo.png"', '')
        updated = updated.replace('alt="logo"', 'alt="Arahberita"')
        updated = updated.replace('alt="Logo"', 'alt="Arahberita"')
        if updated != content:
            p.write_text(updated, encoding='utf-8')
            file_changes.add(str(p))
with open('rebrand_summary.json', 'w', encoding='utf-8') as out:
    json.dump({
        'files_changed': len(file_changes),
        'main_pages': main_pages,
        'article_pages': article_pages,
        'css': css_files,
        'package': package_files,
        'docs': docs_files,
        'changed_files': sorted(file_changes)
    }, out, indent=2)
print('Rebrand script done')
