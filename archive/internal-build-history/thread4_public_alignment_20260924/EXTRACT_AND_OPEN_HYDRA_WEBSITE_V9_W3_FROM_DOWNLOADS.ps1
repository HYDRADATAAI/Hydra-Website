$ErrorActionPreference = 'Stop'
$zip = Get-ChildItem "$HOME\Downloads\HYDRA_WEBSITE_V9_W3_FINAL_INTEGRATION_READY*.zip" -File | Sort-Object LastWriteTime -Descending | Select-Object -First 1
if (-not $zip) { throw 'HYDRA V9 W3 READY ZIP not found in Downloads.' }
$dest = Join-Path $HOME 'Downloads\HYDRA_WEBSITE_V9_W3_FINAL_INTEGRATION_READY_EXTRACTED'
if (Test-Path $dest) { Remove-Item $dest -Recurse -Force }
Expand-Archive -LiteralPath $zip.FullName -DestinationPath $dest -Force
$index = Get-ChildItem $dest -Recurse -File -Filter index.html | Select-Object -First 1
if (-not $index) { throw 'index.html not found after extraction.' }
Write-Host "ZIP=$($zip.FullName)" -ForegroundColor Cyan
Write-Host "SHA256=$((Get-FileHash $zip.FullName -Algorithm SHA256).Hash.ToLowerInvariant())" -ForegroundColor Cyan
Write-Host "OPENING=$($index.FullName)" -ForegroundColor Green
Start-Process $index.FullName
