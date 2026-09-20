$ErrorActionPreference="Stop"
Set-StrictMode -Version Latest

$Downloads=Join-Path $env:USERPROFILE "Downloads"
$Expected="9c3499122009a2e67314c6aae8cb2b89070fad0f2b64c0c1864d6a364e1a4ebd"

$Zip=Get-ChildItem -LiteralPath $Downloads -Filter "NYX_N2_V030_DEPLOYED_COPY_HIGHER_ORDER_BINDING_PROOF_READY.zip" -File -ErrorAction SilentlyContinue |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1

if(-not $Zip){throw "N2 V030 READY ZIP not found in Downloads."}

$Actual=(Get-FileHash -LiteralPath $Zip.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
Write-Host "ZIP_FOUND=$($Zip.FullName)"
Write-Host "ZIP_SHA256=$Actual"

if($Actual -ne $Expected){throw "N2 V030 READY ZIP hash mismatch."}
Write-Host "ZIP_HASH_VERIFIED=PASS"

$Work=Join-Path $Downloads "NYX_N2_V030_WORK_$(Get-Date -Format yyyyMMdd_HHmmss)"
New-Item -ItemType Directory -Path $Work -Force|Out-Null
Expand-Archive -LiteralPath $Zip.FullName -DestinationPath $Work -Force

$Runner=Get-ChildItem -LiteralPath $Work -Filter "RUN_N2_V030_DEPLOYED_COPY_HIGHER_ORDER_BINDING_PROOF_ON_HYDRA.ps1" -File -Recurse |
    Select-Object -First 1

if(-not $Runner){throw "N2 V030 runner not found after extraction."}

Write-Host "WORK_DIR=$Work"
Write-Host "RUNNER=$($Runner.FullName)"

powershell.exe -NoProfile -ExecutionPolicy Bypass -File $Runner.FullName -HydraRoot "D:\HYDRA"
exit $LASTEXITCODE
