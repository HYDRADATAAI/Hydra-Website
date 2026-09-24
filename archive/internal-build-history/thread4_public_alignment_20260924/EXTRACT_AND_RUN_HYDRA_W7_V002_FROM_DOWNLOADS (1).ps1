$ErrorActionPreference = "Stop"
$Downloads = Join-Path $HOME "Downloads"
$Zip = Join-Path $Downloads "HYDRA_W7_V002_CORRECT_SITE_ROOT_RECOVERY_AND_RELEASE_SEAL_READY.zip"
$Expected = "af86600920dc88d33fed6af17a72bc3d3dc6c2ccf6d6ed9192855418ac973e24"
if (-not (Test-Path $Zip)) { throw "READY ZIP not found: $Zip" }
$Actual = (Get-FileHash $Zip -Algorithm SHA256).Hash.ToLowerInvariant()
Write-Host "ZIP_FOUND=$Zip"
Write-Host "ZIP_SHA256=$Actual"
if ($Actual -ne $Expected) { throw "READY ZIP hash mismatch. Expected $Expected" }
Write-Host "ZIP_HASH_VERIFIED=PASS" -ForegroundColor Green
$Stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$Dest = "D:\HYDRA_W7_RELEASE_SEAL\V002_$Stamp"
New-Item -ItemType Directory -Force -Path $Dest | Out-Null
Expand-Archive -Path $Zip -DestinationPath $Dest -Force
$Runner = Get-ChildItem $Dest -Recurse -File -Filter "RUN_HYDRA_W7_V002_CORRECT_SITE_RECOVERY_AND_SEAL.ps1" | Select-Object -First 1
if (-not $Runner) { throw "V002 runner not found." }
Write-Host "RUNNER=$($Runner.FullName)"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File $Runner.FullName
exit $LASTEXITCODE
