$ErrorActionPreference = "Stop"
$Downloads = Join-Path $HOME "Downloads"
$Zip = Get-ChildItem -LiteralPath $Downloads -Filter "HYDRA_W7_CORRECT_SITE_ROOT_RETEST_V002_READY*.zip" -File | Sort-Object LastWriteTime -Descending | Select-Object -First 1
if (-not $Zip) { throw "V002 READY ZIP not found in Downloads." }
$Expected = "4fb5bc87f0c9c1adab37436703a524eb3200cb743566781582e2bf28695491d6"
$Actual = (Get-FileHash -LiteralPath $Zip.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
Write-Host "ZIP_FOUND=$($Zip.FullName)"
Write-Host "ZIP_SHA256=$Actual"
if ($Actual -ne $Expected) { throw "ZIP hash mismatch. Expected $Expected" }
Write-Host "ZIP_HASH_VERIFIED=PASS"
$RunRoot = "D:\HYDRA_W7_RELEASE_SEAL\V002_$(Get-Date -Format yyyyMMdd_HHmmss)"
New-Item -ItemType Directory -Path $RunRoot -Force | Out-Null
Expand-Archive -LiteralPath $Zip.FullName -DestinationPath $RunRoot -Force
$Runner = Get-ChildItem -LiteralPath $RunRoot -Filter "RUN_HYDRA_W7_CORRECT_SITE_ROOT_RETEST_V002.ps1" -File -Recurse | Select-Object -First 1
if (-not $Runner) { throw "V002 runner missing after extraction." }
Write-Host "RUNNER=$($Runner.FullName)"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File $Runner.FullName -HydraRoot "D:\HYDRA"
exit $LASTEXITCODE
