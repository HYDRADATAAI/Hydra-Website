$ErrorActionPreference="Stop"
Set-StrictMode -Version Latest

$Downloads=Join-Path $env:USERPROFILE "Downloads"
$Expected="8f704af0b06393e3221a8feb67a1472c8009b77717d71faa777a52f99c854db1"

$Zip=Get-ChildItem -LiteralPath $Downloads -Filter "PHASE0_BINDING_RUNTIME_DEFECT_026_HANDOFF_READY.zip" -File -ErrorAction SilentlyContinue |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1

if(-not $Zip){throw "Phase-0 DEFECT-026 handoff READY ZIP not found in Downloads."}

$Actual=(Get-FileHash -LiteralPath $Zip.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
Write-Host "ZIP_FOUND=$($Zip.FullName)"
Write-Host "ZIP_SHA256=$Actual"

if($Actual -ne $Expected){throw "Phase-0 DEFECT-026 handoff ZIP hash mismatch."}
Write-Host "ZIP_HASH_VERIFIED=PASS"

$Work=Join-Path $Downloads "PHASE0_DEFECT026_HANDOFF_$(Get-Date -Format yyyyMMdd_HHmmss)"
New-Item -ItemType Directory -Path $Work -Force|Out-Null
Expand-Archive -LiteralPath $Zip.FullName -DestinationPath $Work -Force

$Runner=Get-ChildItem -LiteralPath $Work -Filter "RUN_PHASE0_BINDING_RUNTIME_DEFECT_026_HANDOFF.ps1" -File -Recurse |
    Select-Object -First 1

if(-not $Runner){throw "Phase-0 DEFECT-026 handoff runner not found after extraction."}

Write-Host "WORK_DIR=$Work"
Write-Host "RUNNER=$($Runner.FullName)"

powershell.exe -NoProfile -ExecutionPolicy Bypass -File $Runner.FullName
exit $LASTEXITCODE
