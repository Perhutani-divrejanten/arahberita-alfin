from pathlib import Path
import re

root = Path(__file__).resolve().parent.parent
exts = {'.html', '.css', '.md', '.json', '.toml', '.yml', '.ps1'}
exclude_dirs = {'node_modules', '.git'}
exclude_files = {'rebrand-to-warta-janten.ps1', 'rebrand_indonesia_daily.py'}

replacements = [
    ('https://mail.google.com/mail/?view=cm&fs=1&to=WartaJanten33@gmail.com', 'https://mail.google.com/mail/?view=cm&fs=1&to=info@indonesiadaily.id'),
    ('WartaJanten33@gmail.com', 'info@indonesiadaily.id'),
    ('@WartaJanten', '@IndonesiaDaily'),
    ('facebook.com/WartaJanten', 'facebook.com/IndonesiaDaily'),
    ('twitter.com/WartaJanten', 'twitter.com/IndonesiaDaily'),
    ('instagram.com/WartaJanten', 'instagram.com/IndonesiaDaily'),
    ('linkedin.com/company/WartaJanten', 'linkedin.com/company/IndonesiaDaily'),
    ('youtube.com/@WartaJanten', 'youtube.com/@IndonesiaDaily'),
    ('WartaJanten', 'IndonesiaDaily'),
    ('wartajanten', 'indonesiadaily'),
    ('Warta Janten', 'Indonesia Daily'),
    ('#065F46', '#0F766E'),
    ('#1E3A5F', '#134E4A'),
    ('#022C22', '#7F1F1F'),
    ('‘', "'"),
    ('’', "'"),
    ('“', '"'),
    ('”', '"'),
    ('–', '-'),
    ('—', '-'),
]

logo_pattern = re.compile(r'<img[^>]*src=["\'](?:\.\./)?img/logo\.png["\'][^>]*>', flags=re.IGNORECASE)
logo_markup = '<span style="font-weight: bold; color: #0F766E; font-size: 24px; letter-spacing: -0.5px;">INDONESIA<span style="color: #7F1F1F; font-weight: normal; font-size: 18px; margin-left: 2px;">DAILY</span></span>'

script_updates = {
    Path('replace-logo.ps1'): [
        ('c:\\KULIAH\\MAGANG\\Magang di Perhutani\\Warta Janten', 'c:\\KULIAH\\MAGANG\\Magang di Perhutani\\Indonesia Daily'),
        ('WARTA<span style="color: #1E3A5F; font-weight: normal; font-size: 18px; margin-left: 2px;">JANTEN</span>', 'INDONESIA<span style="color: #7F1F1F; font-weight: normal; font-size: 18px; margin-left: 2px;">DAILY</span>'),
        ('color: #065F46;', 'color: #0F766E;'),
        ('color: #1E3A5F;', 'color: #134E4A;'),
    ],
    Path('final-verification.ps1'): [
        ('Write-Host "========== FINAL VERIFICATION - Indonesia Daily REBRAND =========="', 'Write-Host "========== FINAL VERIFICATION - Indonesia Daily REBRAND =========="'),
        ('"Indonesia Daily", "indonesiadaily", "IndonesiaDaily"', '"Warta Janten", "wartajanten", "WartaJanten"'),
        ('#065F46', '#0F766E'),
        ('#022C22', '#7F1F1F'),
        ('#1E3A5F', '#134E4A'),
    ],
}

modified_files = []
for path in root.rglob('*'):
    if path.is_file() and path.suffix.lower() in exts and path.name not in exclude_files and not any(part in exclude_dirs for part in path.parts):
        text = path.read_text(encoding='utf-8', errors='replace')
        orig = text
        if path.suffix.lower() == '.html':
            text = logo_pattern.sub(logo_markup, text)
        for old, new in replacements:
            text = text.replace(old, new)
        if path.name in {'replace-logo.ps1', 'final-verification.ps1'}:
            for old, new in script_updates.get(path.name, []):
                text = text.replace(old, new)
        if text != orig:
            path.write_text(text, encoding='utf-8')
            modified_files.append(str(path.relative_to(root)))
            print(f'Updated {path.relative_to(root)}')

print(f'\nTotal files modified: {len(modified_files)}')
