# Q-FRONTIER: One-Click YouTube Thumbnail Viewer
Write-Host "==========================================================================" -ForegroundColor Cyan
Write-Host " Opening Q-FRONTIER YouTube Thumbnail (1280x720 16:9)" -ForegroundColor Green
Write-Host "==========================================================================" -ForegroundColor Cyan

$thumbPath = Join-Path $PSScriptRoot "..\docs\YOUTUBE_THUMBNAIL.png"
$fullPath = (Resolve-Path $thumbPath).Path

Write-Host "`n[+] Opening Thumbnail:" -ForegroundColor White
Write-Host "    $fullPath" -ForegroundColor DarkCyan
Write-Host "==========================================================================`n" -ForegroundColor Cyan

Start-Process $fullPath
