# Common functions and variables for all twitter-kit PowerShell scripts

function Get-RepoRoot {
    try {
        $gitRoot = git rev-parse --show-toplevel 2>$null
        if ($LASTEXITCODE -eq 0 -and $gitRoot) {
            return $gitRoot.Trim()
        }
    } catch {}
    
    # Fall back to script location for non-git repos
    $scriptDir = Split-Path -Parent $PSScriptRoot
    return (Resolve-Path "$scriptDir/..").Path
}

function Get-CurrentBranch {
    # First check if TWITTERKIT_FEATURE environment variable is set
    if ($env:TWITTERKIT_FEATURE) {
        return $env:TWITTERKIT_FEATURE
    }
    
    # Then check git if available
    try {
        $branch = git rev-parse --abbrev-ref HEAD 2>$null
        if ($LASTEXITCODE -eq 0 -and $branch) {
            return $branch.Trim()
        }
    } catch {}
    
    # For non-git repos, try to find the latest feature directory
    $repoRoot = Get-RepoRoot
    $specsDir = Join-Path $repoRoot "specs"
    
    if (Test-Path $specsDir) {
        $latestFeature = ""
        $highest = 0
        
        Get-ChildItem -Path $specsDir -Directory | ForEach-Object {
            if ($_.Name -match '^(\d{3})-') {
                $number = [int]$Matches[1]
                if ($number -gt $highest) {
                    $highest = $number
                    $latestFeature = $_.Name
                }
            }
        }
        
        if ($latestFeature) {
            return $latestFeature
        }
    }
    
    return "main"  # Final fallback
}

function Test-HasGit {
    try {
        $null = git rev-parse --show-toplevel 2>$null
        return $LASTEXITCODE -eq 0
    } catch {
        return $false
    }
}

function Test-FeatureBranch {
    param(
        [string]$Branch,
        [bool]$HasGitRepo
    )
    
    # For non-git repos, we can't enforce branch naming
    if (-not $HasGitRepo) {
        Write-Warning "[twitterkit] Git repository not detected; skipped branch validation"
        return $true
    }
    
    if ($Branch -notmatch '^\d{3}-') {
        Write-Error "Not on a feature branch. Current branch: $Branch"
        Write-Error "Feature branches should be named like: 001-feature-name"
        return $false
    }
    
    return $true
}

function Find-FeatureDirByPrefix {
    param(
        [string]$RepoRoot,
        [string]$BranchName
    )
    
    $specsDir = Join-Path $RepoRoot "specs"
    
    # Extract numeric prefix from branch
    if ($BranchName -notmatch '^(\d{3})-') {
        return Join-Path $specsDir $BranchName
    }
    
    $prefix = $Matches[1]
    $matches = @()
    
    if (Test-Path $specsDir) {
        $matches = Get-ChildItem -Path $specsDir -Directory | Where-Object { $_.Name -match "^$prefix-" }
    }
    
    if ($matches.Count -eq 0) {
        return Join-Path $specsDir $BranchName
    } elseif ($matches.Count -eq 1) {
        return $matches[0].FullName
    } else {
        Write-Warning "Multiple spec directories found with prefix '$prefix': $($matches.Name -join ', ')"
        return Join-Path $specsDir $BranchName
    }
}

function Get-FeaturePaths {
    $repoRoot = Get-RepoRoot
    $currentBranch = Get-CurrentBranch
    $hasGit = Test-HasGit
    $featureDir = Find-FeatureDirByPrefix -RepoRoot $repoRoot -BranchName $currentBranch
    
    return @{
        REPO_ROOT = $repoRoot
        CURRENT_BRANCH = $currentBranch
        HAS_GIT = $hasGit
        FEATURE_DIR = $featureDir
        FEATURE_SPEC = Join-Path $featureDir "spec.md"
        IMPL_PLAN = Join-Path $featureDir "plan.md"
        TASKS = Join-Path $featureDir "tasks.md"
        RESEARCH = Join-Path $featureDir "research.md"
        DATA_MODEL = Join-Path $featureDir "data-model.md"
        QUICKSTART = Join-Path $featureDir "quickstart.md"
        CONTRACTS_DIR = Join-Path $featureDir "contracts"
    }
}

function Test-FileExists {
    param(
        [string]$Path,
        [string]$Name
    )
    
    if (Test-Path $Path) {
        Write-Host "  ✓ $Name" -ForegroundColor Green
        return $true
    } else {
        Write-Host "  ✗ $Name" -ForegroundColor Red
        return $false
    }
}

function Test-DirHasContent {
    param(
        [string]$Path,
        [string]$Name
    )
    
    if ((Test-Path $Path) -and (Get-ChildItem -Path $Path -ErrorAction SilentlyContinue)) {
        Write-Host "  ✓ $Name" -ForegroundColor Green
        return $true
    } else {
        Write-Host "  ✗ $Name" -ForegroundColor Red
        return $false
    }
}
