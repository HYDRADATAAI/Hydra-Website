$ErrorActionPreference="Stop"
Set-StrictMode -Version Latest
$Downloads=Join-Path $env:USERPROFILE "Downloads"
$Expected="766e29721053db78a26899bf68fb4a8ea28ed8001ec83480dea9593e61bb74c6"
$Zip=Get-ChildItem -LiteralPath $Downloads -Filter "PHASE0_BINDING_RUNTIME_V001_DEPLOYMENT_ACTIVATION_AUTHORITY_PROOF_READY.zip" -File -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending | Select-Object -First 1
if(-not $Zip){throw "Phase0 Binding/Runtime V001 READY ZIP not found in Downloads."}
$Actual=(Get-FileHash -LiteralPath $Zip.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
Write-Host "ZIP_FOUND=$($Zip.FullName)"
Write-Host "ZIP_SHA256=$Actual"
if($Actual -ne $Expected){throw "Phase0 V001 READY ZIP hash mismatch."}
Write-Host "ZIP_HASH_VERIFIED=PASS"
$Work=Join-Path $Downloads "PHASE0_BINDING_RUNTIME_V001_$(Get-Date -Format yyyyMMdd_HHmmss)"
New-Item -ItemType Directory -Path $Work -Force|Out-Null
Expand-Archive -LiteralPath $Zip.FullName -DestinationPath $Work -Force
$Runner=Get-ChildItem -LiteralPath $Work -Filter "RUN_PHASE0_BINDING_RUNTIME_V001_ACTIVATION_AUTHORITY_PROOF_ON_HYDRA.ps1" -File -Recurse | Select-Object -First 1
if(-not $Runner){throw "Phase0 V001 runner not found after extraction."}
Write-Host "WORK_DIR=$Work"
Write-Host "RUNNER=$($Runner.FullName)"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File $Runner.FullName -HydraRoot "D:\HYDRA"
exit $LASTEXITCODE
