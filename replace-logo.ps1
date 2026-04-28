# Script untuk mengganti logo image dengan text-based logo di semua HTML files

$WorkspaceRoot = "c:\KULIAH\MAGANG\Magang di Perhutani\Indonesia Daily"
$htmlFiles = Get-ChildItem -Path $WorkspaceRoot -Recurse -Include "*.html" -File

$textBasedLogo = @"
<span style="font-weight: bold; color: #0F766E; font-size: 24px; letter-spacing: -0.5px;">INDONESIA<span style="color: #7F1F1F; font-weight: normal; font-size: 18px; margin-left: 2px;">DAILY</span></span>
"@

$replaceCount = 0

foreach ($file in $htmlFiles) {
    try {
        $content = Get-Content -Path $file.FullName -Raw -Encoding UTF8
        $originalContent = $content
        
        # Replace image-based logo with text-based logo in navbar-brand
        # Pattern 1: <img src="img/logo.png" ...> inside navbar-brand
        $pattern1 = '<img src="img/logo\.png"[^>]*>'
        $pattern2 = '<img[^>]*src="img/logo\.png"[^>]*>'
        
        $newContent = $content -replace $pattern1, $textBasedLogo
        $newContent = $newContent -replace $pattern2, $textBasedLogo
        
        # Also replace src="../img/logo.png" for articles
        $pattern3 = '<img[^>]*src="\.\.\/img\/logo\.png"[^>]*>'
        $newContent = $newContent -replace $pattern3, $textBasedLogo
        
        if ($newContent -ne $content) {
            Set-Content -Path $file.FullName -Value $newContent -Encoding UTF8 -NoNewline
            $replaceCount++
            Write-Host "Updated logo in: $($file.Name)"
        }
    } catch {
        Write-Host "Error processing $($file.FullName): $_" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "Logo replacement complete!"
Write-Host "Total files updated: $replaceCount"



