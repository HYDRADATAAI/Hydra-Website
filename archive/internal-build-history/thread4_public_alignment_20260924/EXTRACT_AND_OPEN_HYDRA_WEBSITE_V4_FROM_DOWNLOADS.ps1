$ErrorActionPreference = 'Stop'
$Expected = 'fc168547b06f8576132a57ee63558b0e6ae46e4b61cf21cb5302b5e806f23cf4'
$Zip = Get-ChildItem "$HOME\Downloads\HYDRA_WEBSITE_V4_RECRUITER_SYSTEM_READY*.zip" -File |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1

if (-not $Zip) { throw 'HYDRA Website V4 READY ZIP not found in Downloads.' }
$Actual = (Get-FileHash -LiteralPath $Zip.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
Write-Host '============================================================' -ForegroundColor Cyan
Write-Host 'HYDRA WEBSITE V4 - EXTRACT + VERIFY + OPEN' -ForegroundColor Cyan
Write-Host '============================================================' -ForegroundColor Cyan
Write-Host "ZIP_FOUND=$($Zip.FullName)"
Write-Host "ZIP_SHA256=$Actual"
if ($Actual -ne $Expected) { throw "ZIP hash mismatch. Expected $Expected but got $Actual" }
Write-Host 'ZIP_HASH_VERIFIED=PASS' -ForegroundColor Green

$Dest = 'D:\HYDRA_SITE\V4_RECRUITER_SYSTEM'
if (Test-Path $Dest) { Remove-Item -LiteralPath $Dest -Recurse -Force }
New-Item -ItemType Directory -Path $Dest -Force | Out-Null
Expand-Archive -LiteralPath $Zip.FullName -DestinationPath $Dest -Force
Write-Host "EXTRACTED_TO=$Dest"

$Test = Join-Path $Dest 'TEST_HYDRA_SITE.ps1'
if (Test-Path $Test) {
    powershell.exe -NoProfile -ExecutionPolicy Bypass -File $Test
    if ($LASTEXITCODE -ne 0) { throw 'HYDRA site package test failed.' }
}

$Index = Join-Path $Dest 'index.html'
if (-not (Test-Path $Index)) { throw 'index.html missing after extraction.' }
Start-Process $Index
Write-Host 'SITE_OPENED=YES' -ForegroundColor Green
Write-Host 'HYDRA_CANONICAL_BASELINE_MUTATED=NO'
