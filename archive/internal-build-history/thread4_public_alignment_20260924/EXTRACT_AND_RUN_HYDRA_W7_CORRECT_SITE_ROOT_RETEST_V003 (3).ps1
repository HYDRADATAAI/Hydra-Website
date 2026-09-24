$ErrorActionPreference = "Stop"
$Downloads = Join-Path $HOME "Downloads"
$Zip = Get-ChildItem -LiteralPath $Downloads -Filter "HYDRA_W7_CORRECT_SITE_ROOT_RETEST_V003_READY*.zip" -File |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1

if (-not $Zip) {
    throw "W7 V003 READY ZIP not found in Downloads."
}

$Expected = "90a16a407e7a9531c59c2604e1343a4d5a56f7fdef61e12337d90a970b6b739e"
$Actual = (Get-FileHash -LiteralPath $Zip.FullName -Algorithm SHA256).Hash.ToLowerInvariant()

Write-Host "ZIP_FOUND=$($Zip.FullName)"
Write-Host "ZIP_SHA256=$Actual"
if ($Actual -ne $Expected) {
    throw "ZIP hash mismatch. Expected $Expected"
}
Write-Host "ZIP_HASH_VERIFIED=PASS"

$RunRoot = "D:\HYDRA_W7_RELEASE_SEAL\V003_$(Get-Date -Format yyyyMMdd_HHmmss)"
New-Item -ItemType Directory -Path $RunRoot -Force | Out-Null
Expand-Archive -LiteralPath $Zip.FullName -DestinationPath $RunRoot -Force

$Runner = Get-ChildItem -LiteralPath $RunRoot -Filter "RUN_HYDRA_W7_CORRECT_SITE_ROOT_RETEST_V003.ps1" -File -Recurse |
    Select-Object -First 1

if (-not $Runner) {
    throw "W7 V003 runner missing after extraction."
}

Write-Host "RUNNER=$($Runner.FullName)"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File $Runner.FullName -HydraRoot "D:\HYDRA"
exit $LASTEXITCODE
