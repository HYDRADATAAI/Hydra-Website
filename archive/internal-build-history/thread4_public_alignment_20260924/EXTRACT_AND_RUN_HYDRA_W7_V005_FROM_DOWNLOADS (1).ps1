$ErrorActionPreference = "Stop"
$Downloads = Join-Path $HOME "Downloads"
$Zip = Join-Path $Downloads "HYDRA_W7_V005_PUBLIC_DEPLOYMENT_PREFLIGHT_READY.zip"
$Expected = "5a1f6e8c68097d6fd962795edd3498e5e6cb2d48c0cec7997a5cdf43d00a27c2"
if (-not (Test-Path $Zip)) { throw "READY ZIP not found: $Zip" }
$Actual = (Get-FileHash $Zip -Algorithm SHA256).Hash.ToLowerInvariant()
Write-Host "ZIP_FOUND=$Zip"
Write-Host "ZIP_SHA256=$Actual"
if ($Actual -ne $Expected) { throw "READY ZIP hash mismatch. Expected $Expected" }
Write-Host "ZIP_HASH_VERIFIED=PASS" -ForegroundColor Green
$Stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$Dest = "D:\HYDRA_W7_RELEASE_SEAL\V005_$Stamp"
New-Item -ItemType Directory -Force -Path $Dest | Out-Null
Expand-Archive -Path $Zip -DestinationPath $Dest -Force
$Runner = Get-ChildItem $Dest -Recurse -File -Filter "RUN_HYDRA_W7_V005_PUBLIC_DEPLOYMENT_PREFLIGHT.ps1" | Select-Object -First 1
if (-not $Runner) { throw "V005 runner not found." }
Write-Host "RUNNER=$($Runner.FullName)"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File $Runner.FullName
exit $LASTEXITCODE
