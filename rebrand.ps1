# Rebrand script for Fokus Janten
# Backup articles.json
Copy-Item "articles.json" "articles.json.bak.$(Get-Date -Format 'yyyyMMddHHmmss')"

# Update sites-config.json
$sitesConfigPath = "tools\sites-config.json"
$content = Get-Content $sitesConfigPath -Raw
$content = $content -replace '"siteName": "Arah Berita"', '"siteName": "Fokus Janten"'
$content = $content -replace '"email": "arahberita@gmail.com"', '"email": "fokusjanten@gmail.com"'
$content = $content -replace '"socialHandle": "arahberita"', '"socialHandle": "fokusjanten"'
$content = $content -replace '"primary": "#1D4ED8"', '"primary": "#0EA5E9"'
$content = $content -replace '"dark": "#1E3A8A"', '"dark": "#0F172A"'
$content = $content -replace '"secondary": "#7F2F4F"', '"secondary": "#22C55E"'
$content | Set-Content $sitesConfigPath -Encoding UTF8

# Regenerate articles
& node "tools\generate.js"

# Function to replace in file
function Replace-InFile {
    param($file, $old, $new)
    $content = Get-Content $file -Raw -Encoding UTF8
    if ($content -match [regex]::Escape($old)) {
        $content -replace [regex]::Escape($old), $new | Set-Content $file -Encoding UTF8
        return $true
    }
    return $false
}

# Counters
$mainPagesChanged = 0
$articlePagesChanged = 0
$cssChanged = 0
$packageChanged = 0
$docsChanged = 0

# Replacements for branding
$replacements = @{
    "Arah Berita" = "Fokus Janten"
    "arahberita" = "fokusjanten"
    "arah.berita@gmail.com" = "fokusjanten@gmail.com"
    "ARAH<span style=`"color: #7F2F4F; font-weight: normal; font-size: 18px; margin-left: 2px;`">BERITA</span>" = "FOKUS<span style=`"color: #22C55E; font-weight: normal; font-size: 18px; margin-left: 2px;`">JANTEN</span>"
    "#1D4ED8" = "#0EA5E9"
    "#7F2F4F" = "#22C55E"
    "#1E3A8A" = "#0F172A"
    "Arah Berita - " = "Fokus Janten - "
    " - Arah Berita" = " - Fokus Janten"
    "twitter.com/arahberita" = "twitter.com/fokusjanten"
    "facebook.com/arahberita" = "facebook.com/fokusjanten"
    "linkedin.com/company/arahberita" = "linkedin.com/company/fokusjanten"
    "instagram.com/arahberita" = "instagram.com/fokusjanten"
    "youtube.com/@arahberita" = "youtube.com/@fokusjanten"
    "arahberita@gmail.com" = "fokusjanten@gmail.com"
    "mail.google.com/mail/?view=cm&fs=1&to=arahberita@gmail.com" = "mail.google.com/mail/?view=cm&fs=1&to=fokusjanten@gmail.com"
}

# Process main HTML files (not in article/)
Get-ChildItem -Recurse -Include *.html | Where-Object { $_.FullName -notlike "*\article\*" } | ForEach-Object {
    $changed = $false
    foreach ($rep in $replacements.GetEnumerator()) {
        if (Replace-InFile $_.FullName $rep.Key $rep.Value) { $changed = $true }
    }
    if ($changed) { $mainPagesChanged++ }
}

# Process article HTML files (though regenerated, fix any remaining)
Get-ChildItem -Recurse -Include *.html | Where-Object { $_.FullName -like "*\article\*" } | ForEach-Object {
    $changed = $false
    foreach ($rep in $replacements.GetEnumerator()) {
        if (Replace-InFile $_.FullName $rep.Key $rep.Value) { $changed = $true }
    }
    if ($changed) { $articlePagesChanged++ }
}

# Process CSS files
Get-ChildItem -Recurse -Include *.css | ForEach-Object {
    $changed = $false
    foreach ($rep in $replacements.GetEnumerator()) {
        if (Replace-InFile $_.FullName $rep.Key $rep.Value) { $changed = $true }
    }
    if ($changed) { $cssChanged++ }
}

# Process package.json files
Get-ChildItem -Recurse -Include package.json | ForEach-Object {
    $changed = $false
    $content = Get-Content $_.FullName -Raw -Encoding UTF8
    if ($content -match '"name": "arahberita"') {
        $content -replace '"name": "arahberita"', '"name": "fokusjanten"' | Set-Content $_.FullName -Encoding UTF8
        $changed = $true
    }
    if ($content -match '"name": "arahberita-article-generator"') {
        $content -replace '"name": "arahberita-article-generator"', '"name": "fokusjanten-article-generator"' | Set-Content $_.FullName -Encoding UTF8
        $changed = $true
    }
    if ($changed) { $packageChanged++ }
}

# Process docs
Get-ChildItem -Recurse -Include *.md,*.toml | ForEach-Object {
    $changed = $false
    foreach ($rep in $replacements.GetEnumerator()) {
        if (Replace-InFile $_.FullName $rep.Key $rep.Value) { $changed = $true }
    }
    if ($changed) { $docsChanged++ }
}

# Output
Write-Host "Main pages changed: $mainPagesChanged"
Write-Host "Article pages changed: $articlePagesChanged"
Write-Host "CSS changed: $cssChanged"
Write-Host "Package changed: $packageChanged"
Write-Host "Docs changed: $docsChanged"
Write-Host "Rebrand Fokus Janten selesai ✅"