param()

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$Downloads = Join-Path $HOME "Downloads"
$ExpectedSha = "a287919968067657ad3ee0d2c1dc3fe09ec5d654c46c28835ed515e0c5f54fd7"
$Pattern = "HYDRA_RECRUITER_JOURNEY_CTA_V001_READY*.zip"

Write-Host "============================================================"
Write-Host "HYDRA W6 - RECRUITER JOURNEY PREVIEW"
Write-Host "MODE=PREVIEW_ONLY"
Write-Host "V7_SITE_MUTATION=NO"
Write-Host "============================================================"

$Zip = $null
Get-ChildItem -LiteralPath $Downloads -Filter $Pattern -File -ErrorAction SilentlyContinue |
    Sort-Object LastWriteTime -Descending |
    ForEach-Object {
        if (-not $Zip) {
            $h = (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
            if ($h -eq $ExpectedSha) { $Zip = $_ }
        }
    }

if (-not $Zip) {
    throw "Hash-matching W6 READY ZIP not found in Downloads. Expected SHA256=$ExpectedSha"
}

Write-Host "ZIP_FOUND=$($Zip.FullName)"
Write-Host "ZIP_SHA256=$ExpectedSha"
Write-Host "ZIP_HASH_VERIFIED=PASS"

$Stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$Dest = "D:\HYDRA_W6_RELEASE\PREVIEW_$Stamp"
New-Item -ItemType Directory -Path $Dest -Force | Out-Null
Expand-Archive -LiteralPath $Zip.FullName -DestinationPath $Dest -Force

$Preview = Get-ChildItem -LiteralPath $Dest -Recurse -File -Filter "RECRUITER_JOURNEY_PREVIEW.html" |
    Select-Object -First 1

if (-not $Preview) {
    throw "RECRUITER_JOURNEY_PREVIEW.html missing after extraction."
}

Write-Host "EXTRACTED_TO=$Dest"
Write-Host "PREVIEW=$($Preview.FullName)"
Write-Host "PUBLIC_DEPLOYMENT=NOT_PERFORMED"
Write-Host "EXTERNAL_ACTION_BINDING_REQUIRED=YES"
Write-Host "OPENING_PREVIEW=YES"

Start-Process $Preview.FullName
