$ErrorActionPreference = "Stop"
$Downloads = Join-Path $HOME "Downloads"
$Zip = Join-Path $Downloads "HYDRA_W7_PUBLIC_SITE_RELEASE_SEAL_V001_READY.zip"
$Expected = "5e2526df5bc5779f9bfee5d49127a628b07e98dc05c2ff3520b2ccc218cd85c9"
if (-not (Test-Path $Zip)) { throw "READY ZIP not found: $Zip" }
$Actual = (Get-FileHash $Zip -Algorithm SHA256).Hash.ToLowerInvariant()
Write-Host "ZIP_FOUND=$Zip"
Write-Host "ZIP_SHA256=$Actual"
if ($Actual -ne $Expected) { throw "READY ZIP hash mismatch. Expected $Expected" }
Write-Host "ZIP_HASH_VERIFIED=PASS" -ForegroundColor Green
$Stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$Dest = "D:\HYDRA_W7_RELEASE_SEAL\RUN_$Stamp"
New-Item -ItemType Directory -Force -Path $Dest | Out-Null
Expand-Archive -Path $Zip -DestinationPath $Dest -Force
$Runner = Get-ChildItem $Dest -Recurse -File -Filter "RUN_HYDRA_W7_PUBLIC_SITE_RELEASE_SEAL.ps1" | Select-Object -First 1
if (-not $Runner) { throw "W7 runner not found after extraction." }
Write-Host "RUNNER=$($Runner.FullName)"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File $Runner.FullName
exit $LASTEXITCODE
