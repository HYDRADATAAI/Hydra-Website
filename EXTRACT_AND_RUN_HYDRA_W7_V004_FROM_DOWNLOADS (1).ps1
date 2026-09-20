$ErrorActionPreference = "Stop"
$Downloads = Join-Path $HOME "Downloads"
$Zip = Join-Path $Downloads "HYDRA_W7_V004_READABILITY_PROOF_REPAIR_AND_RETEST_READY.zip"
$Expected = "e1000341fdc6ea91ad995ee303c6526f69b1c9537349c7b57070b3c27be65a01"
if (-not (Test-Path $Zip)) { throw "READY ZIP not found: $Zip" }
$Actual = (Get-FileHash $Zip -Algorithm SHA256).Hash.ToLowerInvariant()
Write-Host "ZIP_FOUND=$Zip"
Write-Host "ZIP_SHA256=$Actual"
if ($Actual -ne $Expected) { throw "READY ZIP hash mismatch. Expected $Expected" }
Write-Host "ZIP_HASH_VERIFIED=PASS" -ForegroundColor Green
$Stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$Dest = "D:\HYDRA_W7_RELEASE_SEAL\V004_$Stamp"
New-Item -ItemType Directory -Force -Path $Dest | Out-Null
Expand-Archive -Path $Zip -DestinationPath $Dest -Force
$Runner = Get-ChildItem $Dest -Recurse -File -Filter "RUN_HYDRA_W7_V004_REPAIR_AND_RETEST.ps1" | Select-Object -First 1
if (-not $Runner) { throw "V004 runner not found." }
Write-Host "RUNNER=$($Runner.FullName)"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File $Runner.FullName
exit $LASTEXITCODE
