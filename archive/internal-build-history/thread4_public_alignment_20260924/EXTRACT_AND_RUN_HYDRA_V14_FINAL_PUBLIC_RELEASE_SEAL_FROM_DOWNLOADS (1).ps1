$ErrorActionPreference='Stop'
$Zip = Get-ChildItem "$HOME\Downloads\HYDRA_V14_FINAL_PUBLIC_RELEASE_SEAL_READY*.zip" -File -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending | Select-Object -First 1
if(-not $Zip){ throw 'HYDRA_V14_FINAL_PUBLIC_RELEASE_SEAL_READY ZIP not found in Downloads.' }
$ExpectedFile = "$($Zip.FullName).sha256"
if(Test-Path $ExpectedFile){
  $expected=((Get-Content $ExpectedFile -Raw).Trim() -split '\s+')[0].ToLowerInvariant()
  $actual=(Get-FileHash $Zip.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
  if($actual -ne $expected){ throw "V14 READY ZIP SHA mismatch expected=$expected actual=$actual" }
  Write-Host "ZIP_HASH_VERIFIED=PASS"
}
$Stamp=Get-Date -Format 'yyyyMMdd_HHmmss'
$Dest="D:\HYDRA_WEBSITE_DEPLOY\V14_PACKAGE_$Stamp"
New-Item -ItemType Directory -Path $Dest -Force | Out-Null
Expand-Archive -LiteralPath $Zip.FullName -DestinationPath $Dest -Force
$Runner=Get-ChildItem $Dest -Filter 'RUN_HYDRA_V14_FINAL_PUBLIC_RELEASE_SEAL.ps1' -File -Recurse | Select-Object -First 1
if(-not $Runner){ throw 'V14 runner not found after extraction.' }
Write-Host "RUNNER=$($Runner.FullName)"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File $Runner.FullName
