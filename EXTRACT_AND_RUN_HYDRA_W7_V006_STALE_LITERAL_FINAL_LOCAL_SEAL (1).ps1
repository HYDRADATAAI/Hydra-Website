$ErrorActionPreference = "Stop"
$Downloads = Join-Path $HOME "Downloads"
$Zip = Get-ChildItem -LiteralPath $Downloads -Filter "HYDRA_W7_V006_STALE_LITERAL_ADJUDICATION_FINAL_LOCAL_SEAL_READY*.zip" -File |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1

if (-not $Zip) {
    throw "HYDRA W7 V006 READY ZIP not found in Downloads."
}

$Expected = "914dc419e592fb23582f60810cd94a4a3ce9216a89937fe0e91c8a90ea6f7fba"
$Actual = (Get-FileHash -LiteralPath $Zip.FullName -Algorithm SHA256).Hash.ToLowerInvariant()

Write-Host "ZIP_FOUND=$($Zip.FullName)"
Write-Host "ZIP_SHA256=$Actual"
if ($Actual -ne $Expected) {
    throw "ZIP hash mismatch. Expected $Expected"
}
Write-Host "ZIP_HASH_VERIFIED=PASS"

$RunRoot = "D:\HYDRA_W7_RELEASE_SEAL\V006_$(Get-Date -Format yyyyMMdd_HHmmss)"
New-Item -ItemType Directory -Path $RunRoot -Force | Out-Null
Expand-Archive -LiteralPath $Zip.FullName -DestinationPath $RunRoot -Force

$Runner = Get-ChildItem -LiteralPath $RunRoot -Filter "RUN_HYDRA_W7_V006_STALE_LITERAL_FINAL_LOCAL_SEAL.ps1" -File -Recurse |
    Select-Object -First 1

if (-not $Runner) {
    throw "HYDRA W7 V006 runner missing after extraction."
}

Write-Host "RUNNER=$($Runner.FullName)"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File $Runner.FullName -SiteRoot "D:\HYDRA_SITE\V7" -ResultBase "D:\HYDRA\WEBSITE_TEST_RESULTS"
exit $LASTEXITCODE
