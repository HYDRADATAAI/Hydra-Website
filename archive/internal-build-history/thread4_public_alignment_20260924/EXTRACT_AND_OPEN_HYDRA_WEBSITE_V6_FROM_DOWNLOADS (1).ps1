$ErrorActionPreference = 'Stop'

$ExpectedHash = 'ef6e1e7dd32e204a01a0202621331a6e67ff89b6e1497ce80bbe632bf43e358c'
$Pattern = 'HYDRA_WEBSITE_V6_ENGINEERING_PROOF_READY*.zip'
$Zip = Get-ChildItem "$HOME\Downloads" -Filter $Pattern -File -ErrorAction SilentlyContinue |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1

if (-not $Zip) { throw "HYDRA V6 ZIP not found in Downloads: $Pattern" }

$ActualHash = (Get-FileHash -LiteralPath $Zip.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
Write-Host '============================================================' -ForegroundColor Cyan
Write-Host 'HYDRA WEBSITE V6 - EXTRACT + OPEN' -ForegroundColor Cyan
Write-Host '============================================================' -ForegroundColor Cyan
Write-Host "ZIP_FOUND=$($Zip.FullName)"
Write-Host "ZIP_SHA256=$ActualHash"
if ($ActualHash -ne $ExpectedHash) {
    throw "ZIP hash mismatch. Expected $ExpectedHash but received $ActualHash"
}
Write-Host 'ZIP_HASH_VERIFIED=PASS' -ForegroundColor Green

$DestinationRoot = 'D:\HYDRA_SITE\V6'
if (Test-Path $DestinationRoot) {
    Remove-Item -LiteralPath $DestinationRoot -Recurse -Force
}
New-Item -ItemType Directory -Path $DestinationRoot -Force | Out-Null
Expand-Archive -LiteralPath $Zip.FullName -DestinationPath $DestinationRoot -Force

$Index = Get-ChildItem -LiteralPath $DestinationRoot -Filter 'index.html' -File -Recurse | Select-Object -First 1
if (-not $Index) { throw 'index.html not found after extraction' }

Write-Host "EXTRACTED_TO=$DestinationRoot"
Write-Host "INDEX=$($Index.FullName)"
Write-Host 'BASELINE_PROJECT_MUTATED=NO'
Write-Host 'Opening HYDRA Website V6...' -ForegroundColor Green
Start-Process -FilePath $Index.FullName
