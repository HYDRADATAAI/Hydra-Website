$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$Index = Join-Path $Root 'index.html'

Write-Host '============================================================' -ForegroundColor Cyan
Write-Host 'HYDRA WEBSITE V7 - LOCAL PREVIEW' -ForegroundColor Cyan
Write-Host '============================================================' -ForegroundColor Cyan
Write-Host "ROOT=$Root"

$Python = Get-Command python -ErrorAction SilentlyContinue
if (-not $Python) { $Python = Get-Command py -ErrorAction SilentlyContinue }

if ($Python) {
    Write-Host 'Starting local server at http://localhost:8080/' -ForegroundColor Green
    Start-Process 'http://localhost:8080/'
    Push-Location $Root
    try {
        if ($Python.Name -eq 'py.exe' -or $Python.Name -eq 'py') {
            & $Python.Source -m http.server 8080
        } else {
            & $Python.Source -m http.server 8080
        }
    }
    finally { Pop-Location }
} else {
    Write-Host 'Python not found. Opening static site directly.' -ForegroundColor Yellow
    Start-Process $Index
}
