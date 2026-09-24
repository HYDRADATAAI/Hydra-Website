param(
 [string]$SiteRoot="D:\HYDRA_SITE\V7",
 [string]$GitHubUrl=""
)
$ErrorActionPreference="Stop"
$Zip=Get-ChildItem "$HOME\Downloads\HYDRA_V7_W6_BOUNDED_REPAIR_V001_READY*.zip" -File -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending | Select-Object -First 1
if(-not $Zip){throw "Repair ZIP not found in Downloads"}
$Hash=(Get-FileHash $Zip.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
Write-Host "ZIP_FOUND=$($Zip.FullName)"
Write-Host "ZIP_SHA256=$Hash"
$Stamp=Get-Date -Format "yyyyMMdd_HHmmss"
$Root="D:\HYDRA\WEBSITE_TESTS\V7_W6_REPAIR_PACKAGE_$Stamp"
New-Item -ItemType Directory -Path $Root -Force|Out-Null
Expand-Archive $Zip.FullName -DestinationPath $Root -Force
$Runner=Get-ChildItem $Root -Recurse -File -Filter "RUN_V7_W6_BOUNDED_REPAIR.ps1"|Select-Object -First 1
$Args=@("-NoProfile","-ExecutionPolicy","Bypass","-File",$Runner.FullName,"-SiteRoot",$SiteRoot)
if($GitHubUrl){$Args+=@("-GitHubUrl",$GitHubUrl)}
& powershell.exe @Args
exit $LASTEXITCODE
