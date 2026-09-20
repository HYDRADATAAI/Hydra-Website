$ErrorActionPreference = 'Stop'
Write-Host '============================================================' -ForegroundColor DarkCyan
Write-Host ' HYDRA WEBSITE V1 - EXTRACT + OPEN' -ForegroundColor Cyan
Write-Host '============================================================' -ForegroundColor DarkCyan

$Downloads = Join-Path $HOME 'Downloads'
$Zip = Get-ChildItem -LiteralPath $Downloads -Filter 'HYDRA_WEBSITE_V1_READY*.zip' -File -ErrorAction SilentlyContinue |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1

if (-not $Zip) {
    throw "HYDRA_WEBSITE_V1_READY.zip was not found in $Downloads"
}

$TargetRoot = if (Test-Path 'D:\') { 'D:\HYDRA_SITE' } else { Join-Path $HOME 'Documents\HYDRA_SITE' }
$Target = Join-Path $TargetRoot 'V1'

if (Test-Path -LiteralPath $Target) {
    Remove-Item -LiteralPath $Target -Recurse -Force
}
New-Item -ItemType Directory -Path $Target -Force | Out-Null

Write-Host "ZIP_FOUND=$($Zip.FullName)" -ForegroundColor Green
Write-Host "ZIP_SHA256=$((Get-FileHash -LiteralPath $Zip.FullName -Algorithm SHA256).Hash.ToLowerInvariant())"
Expand-Archive -LiteralPath $Zip.FullName -DestinationPath $Target -Force

$Index = Get-ChildItem -LiteralPath $Target -Filter 'index.html' -File -Recurse | Select-Object -First 1
if (-not $Index) { throw 'Extracted package does not contain index.html' }

Write-Host "EXTRACTED_TO=$Target" -ForegroundColor Green
Write-Host "OPENING=$($Index.FullName)" -ForegroundColor Green
Start-Process $Index.FullName
