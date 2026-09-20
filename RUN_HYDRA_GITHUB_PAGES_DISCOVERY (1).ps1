param()

$ErrorActionPreference = "Continue"
Set-StrictMode -Version Latest

$Owner = "HYDRADATAAI"
$Repo = "hydra-website"
$RepoFull = "$Owner/$Repo"
$RepoApi = "https://api.github.com/repos/$RepoFull"
$PagesApi = "$RepoApi/pages"
$Downloads = Join-Path $HOME "Downloads"
$Out = Join-Path $Downloads "HYDRA_GITHUB_PAGES_DISCOVERY_RESULT.txt"

$lines = New-Object System.Collections.Generic.List[string]

function Emit([string]$s) {
    Write-Host $s
    [void]$lines.Add($s)
}

Emit "============================================================"
Emit "HYDRA - GITHUB PAGES DISCOVERY DIAGNOSTIC"
Emit "============================================================"
Emit "REPO=$RepoFull"
Emit "MODE=READ_ONLY"
Emit "SITE_MUTATION=NONE"
Emit "GITHUB_MUTATION=NONE"
Emit "============================================================"

$gh = Get-Command gh -ErrorAction SilentlyContinue
$usedGh = $false
$repoFound = $false
$pagesFound = $false
$publicUrl = $null

if ($gh) {
    Emit "GH_CLI=FOUND"

    & gh auth status *> $null
    if ($LASTEXITCODE -eq 0) {
        Emit "GH_AUTH=PASS"
        $usedGh = $true

        try {
            $repoJson = & gh repo view $RepoFull --json nameWithOwner,url,visibility,defaultBranchRef 2>$null
            if ($LASTEXITCODE -eq 0 -and $repoJson) {
                $repoObj = $repoJson | ConvertFrom-Json
                $repoFound = $true
                Emit "REPO_FOUND=YES"
                Emit "REPO_URL=$($repoObj.url)"
                Emit "REPO_VISIBILITY=$($repoObj.visibility)"
                if ($repoObj.defaultBranchRef -and $repoObj.defaultBranchRef.name) {
                    Emit "DEFAULT_BRANCH=$($repoObj.defaultBranchRef.name)"
                }
            } else {
                Emit "REPO_FOUND=NO"
            }
        } catch {
            Emit "REPO_LOOKUP_ERROR=$($_.Exception.Message)"
        }

        if ($repoFound) {
            try {
                $pagesJson = & gh api "repos/$RepoFull/pages" 2>$null
                if ($LASTEXITCODE -eq 0 -and $pagesJson) {
                    $pagesObj = $pagesJson | ConvertFrom-Json
                    if ($pagesObj.html_url) {
                        $pagesFound = $true
                        $publicUrl = [string]$pagesObj.html_url
                        Emit "GITHUB_PAGES=ENABLED"
                        Emit "PUBLIC_HYDRA_URL=$publicUrl"
                        if ($pagesObj.status) {
                            Emit "PAGES_STATUS=$($pagesObj.status)"
                        }
                        if ($pagesObj.source) {
                            if ($pagesObj.source.branch) { Emit "PAGES_BRANCH=$($pagesObj.source.branch)" }
                            if ($pagesObj.source.path)   { Emit "PAGES_PATH=$($pagesObj.source.path)" }
                        }
                    } else {
                        Emit "GITHUB_PAGES=NO_HTML_URL_RETURNED"
                    }
                } else {
                    Emit "GITHUB_PAGES=NOT_ENABLED_OR_NOT_ACCESSIBLE"
                }
            } catch {
                Emit "GITHUB_PAGES=NOT_ENABLED_OR_NOT_ACCESSIBLE"
                Emit "PAGES_LOOKUP_ERROR=$($_.Exception.Message)"
            }
        }
    } else {
        Emit "GH_AUTH=FAIL_OR_NOT_LOGGED_IN"
    }
} else {
    Emit "GH_CLI=NOT_FOUND"
}

if (-not $usedGh) {
    Emit "FALLBACK=PUBLIC_GITHUB_API"
    $headers = @{
        "User-Agent" = "HYDRA-GITHUB-PAGES-DISCOVERY"
        "Accept" = "application/vnd.github+json"
    }

    try {
        $repoResp = Invoke-RestMethod -Uri $RepoApi -Headers $headers -Method Get -TimeoutSec 20
        if ($repoResp -and $repoResp.full_name) {
            $repoFound = $true
            Emit "REPO_FOUND=YES_PUBLIC_API"
            Emit "REPO_URL=$($repoResp.html_url)"
            Emit "REPO_VISIBILITY=$($repoResp.visibility)"
            Emit "DEFAULT_BRANCH=$($repoResp.default_branch)"
        }
    } catch {
        Emit "REPO_FOUND=NO_PUBLIC_API"
        Emit "NOTE=Repo may be private, renamed, absent, or inaccessible without GitHub authentication."
    }

    if ($repoFound) {
        try {
            $pagesResp = Invoke-RestMethod -Uri $PagesApi -Headers $headers -Method Get -TimeoutSec 20
            if ($pagesResp -and $pagesResp.html_url) {
                $pagesFound = $true
                $publicUrl = [string]$pagesResp.html_url
                Emit "GITHUB_PAGES=ENABLED"
                Emit "PUBLIC_HYDRA_URL=$publicUrl"
                if ($pagesResp.status) {
                    Emit "PAGES_STATUS=$($pagesResp.status)"
                }
            }
        } catch {
            Emit "GITHUB_PAGES=NOT_ENABLED_OR_NOT_PUBLICLY_DISCOVERABLE"
        }
    }
}

Emit "============================================================"

if ($pagesFound -and $publicUrl) {
    Emit "VERDICT=PUBLIC_URL_PROVEN"
    Emit "NEXT_ACTION=RERUN_W7_V007_WITH_PROVEN_URL"
    Emit 'COMMAND_BEGIN'
    Emit ('powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$HOME\Downloads\EXTRACT_AND_RUN_HYDRA_W7_V007_FROM_DOWNLOADS.ps1" -PublicUrl "' + $publicUrl + '"')
    Emit 'COMMAND_END'
} elseif ($repoFound) {
    Emit "VERDICT=REPO_PROVEN_PAGES_NOT_PROVEN"
    Emit "NEXT_ACTION=ENABLE_GITHUB_PAGES_IN_REPO_SETTINGS_THEN_RERUN_THIS_DIAGNOSTIC"
} else {
    Emit "VERDICT=REPO_NOT_PROVEN"
    Emit "NEXT_ACTION=OPEN_GITHUB_AND_CONFIRM_EXACT_REPOSITORY_OWNER_NAME_OR_LOGIN_WITH_GH_CLI"
}

Emit "============================================================"
Emit "RESULT_FILE=$Out"

$lines | Set-Content -LiteralPath $Out -Encoding UTF8
