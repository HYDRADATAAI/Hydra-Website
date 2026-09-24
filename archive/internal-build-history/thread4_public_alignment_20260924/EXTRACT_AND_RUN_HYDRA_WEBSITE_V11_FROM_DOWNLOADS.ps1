$ErrorActionPreference = 'Stop'
$Downloads = Join-Path $HOME 'Downloads'
$Zip = Get-ChildItem $Downloads -File -Filter 'HYDRA_WEBSITE_V11_HOSTILE_RECRUITER_FRICTION_SEAL_READY.zip' | Sort-Object LastWriteTime -Descending | Select-Object -First 1
if (-not $Zip) { throw 'V11 READY ZIP not found in Downloads.' }
Write-Host "ZIP_FOUND=$($Zip.FullName)" -ForegroundColor Cyan
$Hash = (Get-FileHash $Zip.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
Write-Host "ZIP_SHA256=$Hash"
$Sidecar = "$($Zip.FullName).sha256"
if (Test-Path $Sidecar) {
  $Expected = ((Get-Content $Sidecar -Raw).Trim() -split '\\s+')[0].ToLowerInvariant()
  if ($Expected -ne $Hash) { throw "ZIP hash mismatch. expected=$Expected actual=$Hash" }
  Write-Host 'ZIP_HASH_VERIFIED=PASS' -ForegroundColor Green
}
$Dest = 'D:\HYDRA_SITE\V11'
if (Test-Path $Dest) { Remove-Item $Dest -Recurse -Force }
New-Item -ItemType Directory -Path $Dest -Force | Out-Null
Expand-Archive -LiteralPath $Zip.FullName -DestinationPath $Dest -Force
$Runner = Get-ChildItem $Dest -File -Filter 'RUN_HYDRA_WEBSITE_V11_LOCAL_AUDIT.ps1' -Recurse | Select-Object -First 1
if (-not $Runner) { throw 'Local audit runner not found after extraction.' }
Write-Host "RUNNER=$($Runner.FullName)" -ForegroundColor Cyan
powershell.exe -NoProfile -ExecutionPolicy Bypass -File $Runner.FullName
