$ErrorActionPreference='Stop'
$Zip = Get-ChildItem "$HOME\Downloads\HYDRA_V13_PUBLIC_GITHUB_DEPLOYMENT_RUNNER_READY*.zip" -File |
  Where-Object { $_.Name -notmatch '\.return\.' } |
  Sort-Object LastWriteTime -Descending | Select-Object -First 1
if(-not $Zip){ throw 'HYDRA V13 deployment runner ZIP not found in Downloads.' }
$Expected = '584f42763200f2a82e6b4d77356d7d0a0bab63ec85671f68b612f95ff3f53880'
$Actual = (Get-FileHash -LiteralPath $Zip.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
Write-Host "ZIP_FOUND=$($Zip.FullName)"
Write-Host "ZIP_SHA256=$Actual"
if($Actual -ne $Expected){ throw "Deployment runner ZIP SHA mismatch. Expected $Expected" }
Write-Host 'ZIP_HASH_VERIFIED=PASS'
$RunRoot = "D:\HYDRA_WEBSITE_DEPLOY\V13_RUNNER_PACKAGE_$(Get-Date -Format yyyyMMdd_HHmmss)"
New-Item -ItemType Directory -Path $RunRoot -Force | Out-Null
Expand-Archive -LiteralPath $Zip.FullName -DestinationPath $RunRoot -Force
$Runner = Get-ChildItem -LiteralPath $RunRoot -Recurse -Filter 'RUN_HYDRA_V13_PUBLIC_GITHUB_DEPLOYMENT.ps1' -File | Select-Object -First 1
if(-not $Runner){ throw 'V13 deployment runner missing after extraction.' }
Write-Host "RUNNER=$($Runner.FullName)"
Write-Host 'WARNING: the next command may commit and push the bounded V12 payload to the public HYDRADATAAI/Hydra-Website repository.' -ForegroundColor Yellow
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File $Runner.FullName
exit $LASTEXITCODE
