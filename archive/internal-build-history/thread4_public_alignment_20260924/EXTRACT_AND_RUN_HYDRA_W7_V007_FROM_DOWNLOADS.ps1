param(
    [string]$PublicUrl = ""
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$Downloads = Join-Path $HOME "Downloads"
$ExpectedSha = "ba81b3680ed2ac8366d9bdd2d4a8bd06a7819d98dee60d807fee8accfc11df86"
$Pattern = "HYDRA_W7_V007_PUBLIC_DEPLOYMENT_FINAL_SEAL_READY*.zip"

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
    throw "Hash-matching W7 V007 READY ZIP not found. Expected SHA256=$ExpectedSha"
}

Write-Host "ZIP_FOUND=$($Zip.FullName)"
Write-Host "ZIP_SHA256=$ExpectedSha"
Write-Host "ZIP_HASH_VERIFIED=PASS"

$Dest = "D:\HYDRA_W7_RELEASE_SEAL\V007_$(Get-Date -Format yyyyMMdd_HHmmss)"
New-Item -ItemType Directory -Path $Dest -Force | Out-Null
Expand-Archive -LiteralPath $Zip.FullName -DestinationPath $Dest -Force

$Runner = Get-ChildItem -LiteralPath $Dest -Recurse -File -Filter "RUN_HYDRA_W7_V007_PUBLIC_DEPLOYMENT_FINAL_SEAL.ps1" |
    Select-Object -First 1
if (-not $Runner) { throw "V007 inner runner missing." }

Write-Host "RUNNER=$($Runner.FullName)"

if ([string]::IsNullOrWhiteSpace($PublicUrl)) {
    & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $Runner.FullName
} else {
    & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $Runner.FullName -PublicUrl $PublicUrl
}

exit $LASTEXITCODE
