$ErrorActionPreference = 'Stop'
$ExpectedSha256 = 'a9f68ce0791c568a0d6357cf0e495b165e0fbeba683aceb6b74def97dadc1a2b'
$Downloads = Join-Path $HOME 'Downloads'
$Zip = Get-ChildItem $Downloads -Filter 'HYDRA_WEBSITE_V7_CASE_STUDY_READY*.zip' -File -ErrorAction SilentlyContinue |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1

if (-not $Zip) { throw 'HYDRA Website V7 READY ZIP not found in Downloads.' }

Write-Host '============================================================' -ForegroundColor Cyan
Write-Host 'HYDRA WEBSITE V7 - CASE STUDY + PUBLIC PROOF SURFACE' -ForegroundColor Cyan
Write-Host '============================================================' -ForegroundColor Cyan
Write-Host "ZIP_FOUND=$($Zip.FullName)"
$Actual = (Get-FileHash -LiteralPath $Zip.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
Write-Host "ZIP_SHA256=$Actual"
if ($Actual -ne $ExpectedSha256) { throw "ZIP hash mismatch. Expected $ExpectedSha256" }
Write-Host 'ZIP_HASH_VERIFIED=PASS' -ForegroundColor Green

$Dest = 'D:\HYDRA_SITE\V7'
if (Test-Path $Dest) { Remove-Item -LiteralPath $Dest -Recurse -Force }
New-Item -ItemType Directory -Path $Dest -Force | Out-Null
Expand-Archive -LiteralPath $Zip.FullName -DestinationPath $Dest -Force
Write-Host "EXTRACTED_TO=$Dest"

$Manifest = Join-Path $Dest 'PACKAGE_MANIFEST_SHA256.txt'
if (-not (Test-Path $Manifest)) { throw 'Package hash manifest missing.' }
foreach ($Line in Get-Content -LiteralPath $Manifest) {
    if ([string]::IsNullOrWhiteSpace($Line)) { continue }
    if ($Line -notmatch '^([0-9a-f]{64})  (.+)$') { throw "Malformed manifest line: $Line" }
    $Expected = $Matches[1]
    $Relative = $Matches[2] -replace '/', '\'
    $Target = Join-Path $Dest $Relative
    if (-not (Test-Path -LiteralPath $Target)) { throw "Manifest file missing: $Relative" }
    $Got = (Get-FileHash -LiteralPath $Target -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($Got -ne $Expected) { throw "Manifest hash mismatch: $Relative" }
}
Write-Host 'CONTENT_MANIFEST_VERIFIED=PASS' -ForegroundColor Green

$Test = Join-Path $Dest 'TEST_HYDRA_SITE.ps1'
if (Test-Path $Test) {
    & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $Test
    if ($LASTEXITCODE -ne 0) { throw 'HYDRA website package test failed.' }
}

$Index = Join-Path $Dest 'index.html'
if (-not (Test-Path $Index)) { throw 'index.html missing after extraction.' }
Write-Host 'HYDRA_PROJECT_ROOT_TOUCHED=NO' -ForegroundColor Green
Write-Host 'OPENING_SITE=YES' -ForegroundColor Green
Start-Process $Index
