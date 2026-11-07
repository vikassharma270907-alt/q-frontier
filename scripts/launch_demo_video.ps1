# Q-FRONTIER: One-Click Animated Video Demo Launcher
Write-Host "==========================================================================" -ForegroundColor Cyan
Write-Host " Q-FRONTIER: 3-Minute Animated Video Demo & Wispr Flow Studio Audio" -ForegroundColor Green
Write-Host " Intermountain Quantum Competition (IQC) 2026 — Brigham Young University" -ForegroundColor Yellow
Write-Host "==========================================================================" -ForegroundColor Cyan

$demoPath = Join-Path $PSScriptRoot "..\docs\video_demo_player.html"
$fullPath = (Resolve-Path $demoPath).Path

Write-Host "`n[+] Opening Animated Video Demo Player in default browser:" -ForegroundColor White
Write-Host "    $fullPath" -ForegroundColor DarkCyan
Write-Host "`n[*] Press Play in the dashboard to start the animated 2:46 demo with neural audio narration." -ForegroundColor Gray
Write-Host "==========================================================================`n" -ForegroundColor Cyan

Start-Process $fullPath
