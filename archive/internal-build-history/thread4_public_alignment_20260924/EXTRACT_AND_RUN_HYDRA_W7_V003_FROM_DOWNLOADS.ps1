$ErrorActionPreference = "Stop"
$Downloads = Join-Path $HOME "Downloads"
$Zip = Join-Path $Downloads "HYDRA_W7_V003_DOM_TRUTH_AND_DEPLOYMENT_SEAL_READY.zip"
$Expected = "ddadf27d37ecc0011f5fbc5ebfbbfdacb32ec9450ef46fe381a9c825774f0412"
if (-not (Test-Path $Zip)) { throw "READY ZIP not found: $Zip" }
$Actual = (Get-FileHash $Zip -Algorithm SHA256).Hash.ToLowerInvariant()
Write-Host "ZIP_FOUND=$Zip"
Write-Host "ZIP_SHA256=$Actual"
if ($Actual -ne $Expected) { throw "READY ZIP hash mismatch. Expected $Expected" }
Write-Host "ZIP_HASH_VERIFIED=PASS" -ForegroundColor Green
$Stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$Dest = "D:\HYDRA_W7_RELEASE_SEAL\V003_$Stamp"
New-Item -ItemType Directory -Force -Path $Dest | Out-Null
Expand-Archive -Path $Zip -DestinationPath $Dest -Force
$Runner = Get-ChildItem $Dest -Recurse -File -Filter "RUN_HYDRA_W7_V003_DOM_TRUTH_AND_DEPLOYMENT_SEAL.ps1" | Select-Object -First 1
if (-not $Runner) { throw "V003 runner not found." }
Write-Host "RUNNER=$($Runner.FullName)"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File $Runner.FullName
exit $LASTEXITCODE
