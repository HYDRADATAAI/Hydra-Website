$ErrorActionPreference = 'Stop'
$Expected = '8eeb2e312ea81bdcfd53229f88db42143e9001aac9cee60a0adc9d9c6dff8bef'
$Zip = Get-ChildItem "$HOME\Downloads\HYDRA_WEBSITE_V5_CONSTRAINT_INTELLIGENCE_READY*.zip" -File |
  Sort-Object LastWriteTime -Descending |
  Select-Object -First 1
if (-not $Zip) { throw 'HYDRA V5 website ZIP not found in Downloads.' }
$Actual = (Get-FileHash $Zip.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
Write-Host "ZIP_FOUND=$($Zip.FullName)"
Write-Host "ZIP_SHA256=$Actual"
if ($Actual -ne $Expected) { throw "ZIP hash mismatch. Expected $Expected" }
Write-Host 'ZIP_HASH_VERIFIED=PASS' -ForegroundColor Green
$Root = 'D:\HYDRA_SITE\V5_CONSTRAINT_INTELLIGENCE'
if (Test-Path $Root) { Remove-Item $Root -Recurse -Force }
New-Item -ItemType Directory -Path $Root -Force | Out-Null
Expand-Archive -LiteralPath $Zip.FullName -DestinationPath $Root -Force
Write-Host "EXTRACTED_TO=$Root" -ForegroundColor Cyan
$Test = Join-Path $Root 'TEST_HYDRA_SITE.ps1'
if (Test-Path $Test) { powershell.exe -NoProfile -ExecutionPolicy Bypass -File $Test }
$Open = Join-Path $Root 'OPEN_HYDRA_SITE.ps1'
if (Test-Path $Open) {
  powershell.exe -NoProfile -ExecutionPolicy Bypass -File $Open
} else {
  Start-Process (Join-Path $Root 'index.html')
}
