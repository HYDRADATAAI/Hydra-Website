$ErrorActionPreference = 'Stop'
$Downloads = Join-Path $HOME 'Downloads'
$Zip = Get-ChildItem -LiteralPath $Downloads -Filter 'HYDRA_WEBSITE_V12_BROWSER_RELEASE_PREFLIGHT_READY*.zip' -File | Sort-Object LastWriteTime -Descending | Select-Object -First 1
if(-not $Zip){ throw 'HYDRA V12 READY ZIP not found in Downloads.' }
$ShaFile = "$($Zip.FullName).sha256"
if(Test-Path -LiteralPath $ShaFile){
  $Expected = ((Get-Content -LiteralPath $ShaFile -Raw).Trim() -split '\s+')[0].ToLowerInvariant()
  $Actual = (Get-FileHash -LiteralPath $Zip.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
  Write-Host "ZIP_FOUND=$($Zip.FullName)"
  Write-Host "ZIP_SHA256=$Actual"
  if($Expected -ne $Actual){ throw "ZIP hash mismatch. expected=$Expected actual=$Actual" }
  Write-Host 'ZIP_HASH_VERIFIED=PASS' -ForegroundColor Green
} else {
  $Actual = (Get-FileHash -LiteralPath $Zip.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
  Write-Host "ZIP_FOUND=$($Zip.FullName)"
  Write-Host "ZIP_SHA256=$Actual"
  Write-Host 'ZIP_HASH_VERIFIED=SKIPPED_SHA_FILE_NOT_FOUND' -ForegroundColor Yellow
}
$RunRoot = "D:\HYDRA_WEBSITE_RELEASE\V12_$(Get-Date -Format yyyyMMdd_HHmmss)"
New-Item -ItemType Directory -Path $RunRoot -Force | Out-Null
Expand-Archive -LiteralPath $Zip.FullName -DestinationPath $RunRoot -Force
$Runner = Get-ChildItem -LiteralPath $RunRoot -Filter 'RUN_HYDRA_WEBSITE_V12_RELEASE_PREFLIGHT.ps1' -File -Recurse | Select-Object -First 1
if(-not $Runner){ throw 'V12 internal preflight runner not found after extraction.' }
Write-Host "RUNNER=$($Runner.FullName)"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File $Runner.FullName
if($LASTEXITCODE -ne 0){ exit $LASTEXITCODE }
$Site = Join-Path $Runner.Directory.FullName 'index.html'
Write-Host "SITE=$Site"
Start-Process $Site
