$ErrorActionPreference = 'Stop'

$ExpectedHash = '208d14c00f0b4168d487be8987087c2b4bb366c9bef96e4d23fc83011b9e8072'
$Zip = Get-ChildItem "$HOME\Downloads\HYDRA_WEBSITE_V3_RECRUITER_READY*.zip" -File -ErrorAction SilentlyContinue |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1

if (-not $Zip) {
    throw 'HYDRA_WEBSITE_V3_RECRUITER_READY.zip was not found in Downloads.'
}

$ActualHash = (Get-FileHash -LiteralPath $Zip.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
Write-Host '============================================================' -ForegroundColor Cyan
Write-Host 'HYDRA WEBSITE V3 RECRUITER PASS - EXTRACT + OPEN' -ForegroundColor Cyan
Write-Host '============================================================' -ForegroundColor Cyan
Write-Host "ZIP_FOUND=$($Zip.FullName)"
Write-Host "ZIP_SHA256=$ActualHash"

if ($ActualHash -ne $ExpectedHash) {
    throw "ZIP hash mismatch. Expected $ExpectedHash"
}
Write-Host 'ZIP_HASH_VERIFIED=PASS' -ForegroundColor Green

$SiteRoot = if (Test-Path 'D:\') { 'D:\HYDRA_SITE' } else { Join-Path $HOME 'HYDRA_SITE' }
New-Item -ItemType Directory -Path $SiteRoot -Force | Out-Null

$Target = Join-Path $SiteRoot 'V3_RECRUITER'
if (Test-Path $Target) {
    $Target = Join-Path $SiteRoot ("V3_RECRUITER_PREVIEW_{0}" -f (Get-Date -Format 'yyyyMMdd_HHmmss'))
}

New-Item -ItemType Directory -Path $Target -Force | Out-Null
Expand-Archive -LiteralPath $Zip.FullName -DestinationPath $Target -Force

$Index = Join-Path $Target 'index.html'
if (-not (Test-Path $Index)) { throw "index.html missing after extraction: $Index" }

Write-Host "EXTRACTED_TO=$Target" -ForegroundColor Green
Write-Host 'SITE_PACKAGE_TEST=PASS' -ForegroundColor Green
Write-Host 'BASELINE_MUTATED=NO' -ForegroundColor Green
Write-Host 'Opening HYDRA website...' -ForegroundColor Cyan
Start-Process $Index
