param([string]$SiteRoot="D:\HYDRA_SITE\V7",[string]$PublicUrl="")
$ErrorActionPreference="Stop"
$Zip=Get-ChildItem "$HOME\Downloads\HYDRA_W7_BROWSER_RELEASE_SEAL_V001_READY*.zip" -File -ErrorAction SilentlyContinue|Sort-Object LastWriteTime -Descending|Select-Object -First 1
if(-not $Zip){throw "W7 browser seal ZIP not found in Downloads"}
$Hash=(Get-FileHash $Zip.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
Write-Host "ZIP_FOUND=$($Zip.FullName)"
Write-Host "ZIP_SHA256=$Hash"
$Stamp=Get-Date -Format "yyyyMMdd_HHmmss"
$Run="D:\HYDRA\WEBSITE_TESTS\W7_BROWSER_SEAL_PACKAGE_$Stamp"
New-Item -ItemType Directory -Path $Run -Force|Out-Null
Expand-Archive $Zip.FullName -DestinationPath $Run -Force
$Runner=Get-ChildItem $Run -Recurse -File -Filter "RUN_HYDRA_W7_BROWSER_RELEASE_SEAL.ps1"|Select-Object -First 1
if(-not $Runner){throw "W7 runner not found after extraction"}
$Args=@("-NoProfile","-ExecutionPolicy","Bypass","-File",$Runner.FullName,"-SiteRoot",$SiteRoot)
if($PublicUrl){$Args+=@("-PublicUrl",$PublicUrl)}
& powershell.exe @Args
exit $LASTEXITCODE
