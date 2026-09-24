$ErrorActionPreference="Stop"
Set-StrictMode -Version Latest

$Downloads=Join-Path $env:USERPROFILE "Downloads"
$Expected="5aa1a5acac9b85dbb680704f938f24898714828bcd27c36087e3704a8c4787f1"

$Zip=Get-ChildItem -LiteralPath $Downloads -Filter "NYX_N2_V031_DEPLOYMENT_ACTIVATION_CONTRACT_ESCALATION_READY.zip" -File -ErrorAction SilentlyContinue |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1

if(-not $Zip){throw "N2 V031 READY ZIP not found in Downloads."}

$Actual=(Get-FileHash -LiteralPath $Zip.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
Write-Host "ZIP_FOUND=$($Zip.FullName)"
Write-Host "ZIP_SHA256=$Actual"

if($Actual -ne $Expected){throw "N2 V031 READY ZIP hash mismatch."}
Write-Host "ZIP_HASH_VERIFIED=PASS"

$Work=Join-Path $Downloads "NYX_N2_V031_WORK_$(Get-Date -Format yyyyMMdd_HHmmss)"
New-Item -ItemType Directory -Path $Work -Force|Out-Null
Expand-Archive -LiteralPath $Zip.FullName -DestinationPath $Work -Force

$Runner=Get-ChildItem -LiteralPath $Work -Filter "RUN_N2_V031_DEPLOYMENT_ACTIVATION_CONTRACT_ESCALATION.ps1" -File -Recurse |
    Select-Object -First 1

if(-not $Runner){throw "N2 V031 runner not found after extraction."}

Write-Host "WORK_DIR=$Work"
Write-Host "RUNNER=$($Runner.FullName)"

powershell.exe -NoProfile -ExecutionPolicy Bypass -File $Runner.FullName
exit $LASTEXITCODE
