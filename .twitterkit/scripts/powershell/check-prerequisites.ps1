#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Consolidated prerequisite checking script for twitter-kit

.DESCRIPTION
    This script provides unified prerequisite checking for Twitter-kit workflow.

.PARAMETER Json
    Output in JSON format

.PARAMETER RequireTasks
    Require tasks.md to exist (for implementation phase)

.PARAMETER IncludeTasks
    Include tasks.md in AVAILABLE_DOCS list

.PARAMETER PathsOnly
    Only output path variables (no validation)

.EXAMPLE
    ./check-prerequisites.ps1 -Json

.EXAMPLE
    ./check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks

.EXAMPLE
    ./check-prerequisites.ps1 -PathsOnly
#>

param(
    [switch]$Json,
    [switch]$RequireTasks,
    [switch]$IncludeTasks,
    [switch]$PathsOnly,
    [switch]$Help
)

if ($Help) {
    Get-Help $MyInvocation.MyCommand.Path -Detailed
    exit 0
}

# Source common functions
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
. (Join-Path $scriptDir "common.ps1")

# Get feature paths
$paths = Get-FeaturePaths

# Validate branch
if (-not (Test-FeatureBranch -Branch $paths.CURRENT_BRANCH -HasGitRepo $paths.HAS_GIT)) {
    exit 1
}

# If paths-only mode, output paths and exit
if ($PathsOnly) {
    if ($Json) {
        @{
            REPO_ROOT = $paths.REPO_ROOT
            BRANCH = $paths.CURRENT_BRANCH
            FEATURE_DIR = $paths.FEATURE_DIR
            FEATURE_SPEC = $paths.FEATURE_SPEC
            IMPL_PLAN = $paths.IMPL_PLAN
            TASKS = $paths.TASKS
        } | ConvertTo-Json -Compress
    } else {
        Write-Host "REPO_ROOT: $($paths.REPO_ROOT)"
        Write-Host "BRANCH: $($paths.CURRENT_BRANCH)"
        Write-Host "FEATURE_DIR: $($paths.FEATURE_DIR)"
        Write-Host "FEATURE_SPEC: $($paths.FEATURE_SPEC)"
        Write-Host "IMPL_PLAN: $($paths.IMPL_PLAN)"
        Write-Host "TASKS: $($paths.TASKS)"
    }
    exit 0
}

# Validate required directories and files
if (-not (Test-Path $paths.FEATURE_DIR)) {
    Write-Error "Feature directory not found: $($paths.FEATURE_DIR)"
    Write-Error "Run /twitterkit.specify first to create the feature structure."
    exit 1
}

if (-not (Test-Path $paths.IMPL_PLAN)) {
    Write-Error "plan.md not found in $($paths.FEATURE_DIR)"
    Write-Error "Run /twitterkit.plan first to create the implementation plan."
    exit 1
}

# Check for tasks.md if required
if ($RequireTasks -and -not (Test-Path $paths.TASKS)) {
    Write-Error "tasks.md not found in $($paths.FEATURE_DIR)"
    Write-Error "Run /twitterkit.tasks first to create the task list."
    exit 1
}

# Build list of available documents
$docs = @()

if (Test-Path $paths.RESEARCH) { $docs += "research.md" }
if (Test-Path $paths.DATA_MODEL) { $docs += "data-model.md" }

if ((Test-Path $paths.CONTRACTS_DIR) -and (Get-ChildItem -Path $paths.CONTRACTS_DIR -ErrorAction SilentlyContinue)) {
    $docs += "contracts/"
}

if (Test-Path $paths.QUICKSTART) { $docs += "quickstart.md" }

if ($IncludeTasks -and (Test-Path $paths.TASKS)) {
    $docs += "tasks.md"
}

# Output results
if ($Json) {
    @{
        FEATURE_DIR = $paths.FEATURE_DIR
        AVAILABLE_DOCS = $docs
    } | ConvertTo-Json -Compress
} else {
    Write-Host "FEATURE_DIR:$($paths.FEATURE_DIR)"
    Write-Host "AVAILABLE_DOCS:"
    
    Test-FileExists -Path $paths.RESEARCH -Name "research.md" | Out-Null
    Test-FileExists -Path $paths.DATA_MODEL -Name "data-model.md" | Out-Null
    Test-DirHasContent -Path $paths.CONTRACTS_DIR -Name "contracts/" | Out-Null
    Test-FileExists -Path $paths.QUICKSTART -Name "quickstart.md" | Out-Null
    
    if ($IncludeTasks) {
        Test-FileExists -Path $paths.TASKS -Name "tasks.md" | Out-Null
    }
}
