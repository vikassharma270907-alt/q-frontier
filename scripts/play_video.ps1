# Q-FRONTIER: One-Click Demo Video Player
Write-Host "==========================================================================" -ForegroundColor Cyan
Write-Host " Playing Q-FRONTIER 1080p Demo Video (2m 46s)" -ForegroundColor Green
Write-Host " Intermountain Quantum Competition (IQC) 2026 — BYU Physics" -ForegroundColor Yellow
Write-Host "==========================================================================" -ForegroundColor Cyan

$videoPath = Join-Path $PSScriptRoot "..\docs\Q_FRONTIER_DEMO_VIDEO.mp4"
$fullPath = (Resolve-Path $videoPath).Path

Write-Host "`n[+] Launching Video Player:" -ForegroundColor White
Write-Host "    $fullPath" -ForegroundColor DarkCyan
Write-Host "==========================================================================`n" -ForegroundColor Cyan

Start-Process $fullPath
