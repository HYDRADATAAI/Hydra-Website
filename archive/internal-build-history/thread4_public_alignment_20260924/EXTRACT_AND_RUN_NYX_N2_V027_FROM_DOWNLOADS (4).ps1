$ErrorActionPreference="Stop"
Set-StrictMode -Version Latest

$Downloads=Join-Path $env:USERPROFILE "Downloads"
$Expected="b648ac492115430ab489bdcfbaf2b574262f047c8fbea04bb54894a18c14a7b0"
$Zip=Get-ChildItem -LiteralPath $Downloads -Filter "NYX_N2_V027_BINDING_RECEIPT_RUNTIME_ENTRYPOINT_FIELD_PROOF_READY.zip" -File -ErrorAction SilentlyContinue |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1

if(-not $Zip){throw "N2 V027 READY ZIP not found in Downloads."}

$Actual=(Get-FileHash -LiteralPath $Zip.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
Write-Host "ZIP_FOUND=$($Zip.FullName)"
Write-Host "ZIP_SHA256=$Actual"

if($Actual -ne $Expected){throw "N2 V027 READY ZIP hash mismatch."}
Write-Host "ZIP_HASH_VERIFIED=PASS"

$Work=Join-Path $Downloads "NYX_N2_V027_WORK_$(Get-Date -Format yyyyMMdd_HHmmss)"
New-Item -ItemType Directory -Path $Work -Force|Out-Null
Expand-Archive -LiteralPath $Zip.FullName -DestinationPath $Work -Force

$Runner=Get-ChildItem -LiteralPath $Work -Filter "RUN_N2_V027_BINDING_RECEIPT_RUNTIME_ENTRYPOINT_FIELD_PROOF_ON_HYDRA.ps1" -File -Recurse |
    Select-Object -First 1

if(-not $Runner){throw "N2 V027 runner not found after extraction."}

Write-Host "WORK_DIR=$Work"
Write-Host "RUNNER=$($Runner.FullName)"

powershell.exe -NoProfile -ExecutionPolicy Bypass -File $Runner.FullName -HydraRoot "D:\HYDRA"
exit $LASTEXITCODE
