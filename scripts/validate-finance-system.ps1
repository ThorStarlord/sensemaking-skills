<#
.SYNOPSIS
    Automates validation of the finance system using the orchestration workflow.

.DESCRIPTION
    CLI wrapper around orchestration-runner.py that manages workflow execution,
    baseline comparison, GitHub issue creation, and cache updates.

.PARAMETER Mode
    Execution mode for the workflow.
    - plan_only: Display execution plan without running
    - guided_execution: Interactive mode with manual selection (default)
    - autonomous_execution: Fully automated, no user interaction

.PARAMETER CompareBaseline
    When specified, compares current validation against the baseline cache.
    Uses .validation-cache/latest as the baseline reference.

.PARAMETER CreateTickets
    When specified, automatically creates GitHub issues for validation errors found.

.PARAMETER Force
    When specified, skips validation checks and proceeds directly to execution.

.EXAMPLE
    .\validate-finance-system.ps1 -Mode guided_execution

.EXAMPLE
    .\validate-finance-system.ps1 -Mode autonomous_execution -CompareBaseline -CreateTickets

.NOTES
    Script expects:
    - docs/workflows/validation-finance-system.yaml (required)
    - scripts/orchestration-runner.py (optional, in development)
    - Python 3.x installed and available in PATH
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory = $false)]
    [ValidateSet('plan_only', 'guided_execution', 'autonomous_execution')]
    [string]$Mode = 'guided_execution',

    [Parameter(Mandatory = $false)]
    [switch]$CompareBaseline,

    [Parameter(Mandatory = $false)]
    [switch]$CreateTickets,

    [Parameter(Mandatory = $false)]
    [switch]$Force
)

# ==========================================
# PATH RESOLUTION
# ==========================================

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Split-Path -Parent $scriptDir
$workflowConfig = Join-Path $repoRoot "docs/workflows/validation-finance-system.yaml"
$orchestratorScript = Join-Path $repoRoot "scripts/orchestration-runner.py"
$outputTimestamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$outputDir = Join-Path $repoRoot "outputs/validation-$outputTimestamp"
$cacheDir = Join-Path $repoRoot ".validation-cache"
$latestCacheDir = Join-Path $cacheDir "latest"

# ==========================================
# VALIDATION CHECKS
# ==========================================

Write-Host ""
Write-Host "=========================================="
Write-Host "VALIDATION STARTUP"
Write-Host "==========================================" -ForegroundColor Cyan

# Check workflow config exists
if (-not (Test-Path $workflowConfig)) {
    Write-Host "ERROR: Workflow configuration not found: $workflowConfig" -ForegroundColor Red
    exit 1
}
Write-Host "OK Workflow config found: $workflowConfig" -ForegroundColor Green

# Check orchestrator script
if (-not (Test-Path $orchestratorScript)) {
    Write-Host "WARNING Orchestrator script not found: $orchestratorScript" -ForegroundColor Yellow
    Write-Host "  (This is expected during development, continuing anyway)" -ForegroundColor Yellow
    $orchestratorAvailable = $false
} else {
    Write-Host "OK Orchestrator script found: $orchestratorScript" -ForegroundColor Green
    $orchestratorAvailable = $true
}

# Check Python availability
try {
    $pythonVersion = python --version 2>&1
    Write-Host "OK Python available: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "WARNING Python not available in PATH - orchestration may fail" -ForegroundColor Yellow
}

# ==========================================
# BASELINE COMPARISON
# ==========================================

if ($CompareBaseline) {
    Write-Host ""
    Write-Host "Baseline Comparison:" -ForegroundColor Cyan
    if (Test-Path $latestCacheDir) {
        Write-Host "OK Baseline found at: $latestCacheDir" -ForegroundColor Green
        Write-Host "  Will compare current validation against this baseline" -ForegroundColor Gray
    } else {
        Write-Host "INFO No baseline found (first run)" -ForegroundColor Cyan
        Write-Host "  This validation will establish the baseline" -ForegroundColor Gray
    }
} else {
    Write-Host ""
    Write-Host "INFO Baseline comparison disabled (use -CompareBaseline to enable)" -ForegroundColor Gray
}

# ==========================================
# AUTO-TICKETING SUPPORT
# ==========================================

if ($CreateTickets) {
    Write-Host ""
    Write-Host "GitHub Issue Creation:" -ForegroundColor Cyan
    Write-Host "OK Auto-create enabled" -ForegroundColor Green
    Write-Host "  GitHub issues will be created for validation errors" -ForegroundColor Gray
} else {
    Write-Host ""
    Write-Host "INFO GitHub issue creation disabled (use -CreateTickets to enable)" -ForegroundColor Gray
}

# ==========================================
# DISPLAY EXECUTION PLAN
# ==========================================

Write-Host ""
Write-Host "=========================================="
Write-Host "EXECUTION PLAN"
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Mode: $Mode"
Write-Host "Output Directory: $outputDir"
Write-Host "Validation Enabled: $(-not $Force)"

if ($CompareBaseline) {
    Write-Host "Baseline Comparison: Yes"
}

if ($CreateTickets) {
    Write-Host "Auto-Ticketing: Yes"
}

# ==========================================
# ORCHESTRATOR INVOCATION
# ==========================================

if ($orchestratorAvailable) {
    Write-Host ""
    Write-Host "=========================================="
    Write-Host "EXECUTION START"
    Write-Host "==========================================" -ForegroundColor Cyan

    # Create output directory
    $null = New-Item -ItemType Directory -Path $outputDir -Force -ErrorAction SilentlyContinue

    # Build arguments
    # Note: orchestration-runner.py expects workflow_id as positional arg, not config file
    $orchestratorArgs = @(
        $orchestratorScript,
        "validation-finance-system",
        "--mode", $Mode,
        "--log-dir", $outputDir,
        "--repo-root", $repoRoot
    )

    # Add --validate flag if NOT forcing (skip validation)
    if (-not $Force) {
        $orchestratorArgs += "--validate"
    }

    # Add baseline directory hint via environment variable
    if ($CompareBaseline) {
        $env:VALIDATION_BASELINE_DIR = $latestCacheDir
    }

    # Add auto-ticketing hint via environment variable
    if ($CreateTickets) {
        $env:VALIDATION_CREATE_TICKETS = "true"
    }

    # Execute orchestrator
    Write-Host "Invoking orchestrator..." -ForegroundColor Gray
    Write-Host "Command: python $($orchestratorArgs -join ' ')" -ForegroundColor DarkGray

    try {
        python @orchestratorArgs
        $exitCode = $LASTEXITCODE

        if ($exitCode -ne 0) {
            Write-Host ""
            Write-Host "Orchestrator exited with code: $exitCode" -ForegroundColor Yellow
            Write-Host "Check output directory for details: $outputDir" -ForegroundColor Gray
        } else {
            Write-Host ""
            Write-Host "OK Orchestrator completed successfully" -ForegroundColor Green

            # ==========================================
            # CACHE UPDATE (on success)
            # ==========================================

            Write-Host ""
            Write-Host "Updating validation cache..." -ForegroundColor Cyan

            # Create cache run directory
            $cacheRunTimestamp = Get-Date -Format 'yyyyMMdd-HHmmss'
            $cacheRunDir = Join-Path $cacheDir "run-$cacheRunTimestamp"

            $null = New-Item -ItemType Directory -Path $cacheRunDir -Force -ErrorAction SilentlyContinue
            Write-Host "OK Cache run directory created: $cacheRunDir" -ForegroundColor Green

            # Copy key artifacts to cache
            $artifactsToCopy = @(
                "sensemaking_brief.md",
                "error_analysis.md",
                "changes_identified.md",
                "comparison_report.md"
            )

            foreach ($artifact in $artifactsToCopy) {
                $srcPath = Join-Path $outputDir $artifact
                if (Test-Path $srcPath) {
                    Copy-Item $srcPath $cacheRunDir -Force -ErrorAction SilentlyContinue
                    Write-Host "  OK Cached: $artifact" -ForegroundColor Green
                } else {
                    Write-Host "  INFO Not found: $artifact" -ForegroundColor Gray
                }
            }

            # Update 'latest' symlink
            Write-Host ""
            Write-Host "Updating latest symlink..." -ForegroundColor Cyan
            if (Test-Path $latestCacheDir) {
                Remove-Item $latestCacheDir -Force -ErrorAction SilentlyContinue
            }

            try {
                $null = New-Item -ItemType SymbolicLink -Path $latestCacheDir -Target $cacheRunDir -Force -ErrorAction SilentlyContinue
                Write-Host "OK Latest symlink updated: $latestCacheDir -> $cacheRunDir" -ForegroundColor Green
            } catch {
                Write-Host "WARNING Could not create symlink (may require admin): $($_.Exception.Message)" -ForegroundColor Yellow
                Write-Host "  Cache run directory still available at: $cacheRunDir" -ForegroundColor Gray
            }
        }
    } catch {
        Write-Host ""
        Write-Host "ERROR executing orchestrator: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host $_.Exception.StackTrace -ForegroundColor DarkRed
        exit 1
    }
} else {
    Write-Host ""
    Write-Host "=========================================="
    Write-Host "DRY RUN (Orchestrator Not Available)"
    Write-Host "==========================================" -ForegroundColor Yellow
    Write-Host "Orchestrator script is still under development." -ForegroundColor Gray
    Write-Host "Script validation and planning complete, but workflow not executed." -ForegroundColor Gray
    Write-Host "Output would be written to: $outputDir" -ForegroundColor Gray
}

# ==========================================
# SUMMARY OUTPUT
# ==========================================

Write-Host ""
Write-Host "=========================================="
Write-Host "VALIDATION COMPLETE"
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Output: $outputDir"
Write-Host "Mode: $Mode"
Write-Host "Cache: $cacheDir"
Write-Host ""
Write-Host "Key Artifacts:"
Write-Host "  - sensemaking_brief.md"
Write-Host "  - error_analysis.md"
Write-Host "  - changes_identified.md"
Write-Host "  - comparison_report.md (if -CompareBaseline used)"
Write-Host ""
Write-Host "For more information, see: $outputDir" -ForegroundColor Gray
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

exit $exitCode
