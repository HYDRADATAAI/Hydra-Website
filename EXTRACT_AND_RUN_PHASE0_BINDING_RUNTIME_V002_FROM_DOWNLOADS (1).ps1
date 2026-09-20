$ErrorActionPreference="Stop"
Set-StrictMode -Version Latest

$Downloads=Join-Path $env:USERPROFILE "Downloads"
$Expected="07188b2cc974ac5d015a4025c6975bbefddd971ad81afdf4a2503feb1534f348"

$Zip=Get-ChildItem -LiteralPath $Downloads -Filter "PHASE0_BINDING_RUNTIME_V002_FINAL_BLOCKED_ACTIVATION_AUTHORITY_SEAL_READY.zip" -File -ErrorAction SilentlyContinue |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1

if(-not $Zip){throw "Phase0 Binding/Runtime V002 READY ZIP not found in Downloads."}

$Actual=(Get-FileHash -LiteralPath $Zip.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
Write-Host "ZIP_FOUND=$($Zip.FullName)"
Write-Host "ZIP_SHA256=$Actual"

if($Actual -ne $Expected){throw "Phase0 V002 READY ZIP hash mismatch."}
Write-Host "ZIP_HASH_VERIFIED=PASS"

$Work=Join-Path $Downloads "PHASE0_BINDING_RUNTIME_V002_$(Get-Date -Format yyyyMMdd_HHmmss)"
New-Item -ItemType Directory -Path $Work -Force|Out-Null
Expand-Archive -LiteralPath $Zip.FullName -DestinationPath $Work -Force

$Runner=Get-ChildItem -LiteralPath $Work -Filter "RUN_PHASE0_BINDING_RUNTIME_V002_FINAL_BLOCKED_SEAL.ps1" -File -Recurse |
    Select-Object -First 1

if(-not $Runner){throw "Phase0 V002 runner not found after extraction."}

Write-Host "WORK_DIR=$Work"
Write-Host "RUNNER=$($Runner.FullName)"

powershell.exe -NoProfile -ExecutionPolicy Bypass -File $Runner.FullName
exit $LASTEXITCODE
