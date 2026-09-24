$ErrorActionPreference = "Stop"
$Downloads = Join-Path $HOME "Downloads"
$Zip = Get-ChildItem -LiteralPath $Downloads -Filter "HYDRA_W7_V005_BOUNDED_COPY_REPAIR_BROWSER_RETEST_READY*.zip" -File | Sort-Object LastWriteTime -Descending | Select-Object -First 1
if (-not $Zip) { throw "HYDRA W7 V005 READY ZIP not found in Downloads." }
$Expected = "f5ddffdeb165dffbe665acf23727e6205cef07d0e7ade676f3f1ba4ea82e6408"
$Actual = (Get-FileHash -LiteralPath $Zip.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
Write-Host "ZIP_FOUND=$($Zip.FullName)"
Write-Host "ZIP_SHA256=$Actual"
if ($Actual -ne $Expected) { throw "ZIP hash mismatch. Expected $Expected" }
Write-Host "ZIP_HASH_VERIFIED=PASS"
$RunRoot = "D:\HYDRA_W7_RELEASE_SEAL\V005_$(Get-Date -Format yyyyMMdd_HHmmss)"
New-Item -ItemType Directory -Path $RunRoot -Force | Out-Null
Expand-Archive -LiteralPath $Zip.FullName -DestinationPath $RunRoot -Force
$Runner = Get-ChildItem -LiteralPath $RunRoot -Filter "RUN_HYDRA_W7_V005_BOUNDED_COPY_REPAIR_BROWSER_RETEST.ps1" -File -Recurse | Select-Object -First 1
if (-not $Runner) { throw "HYDRA W7 V005 runner missing after extraction." }
Write-Host "RUNNER=$($Runner.FullName)"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File $Runner.FullName -SiteRoot "D:\HYDRA_SITE\V7" -ResultBase "D:\HYDRA\WEBSITE_TEST_RESULTS"
exit $LASTEXITCODE
