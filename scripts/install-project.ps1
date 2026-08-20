param(
    [Parameter(Mandatory=$true)][string]$Target,
    [switch]$Force
)

$ErrorActionPreference = 'Stop'
$SourceRoot = Split-Path -Parent $PSScriptRoot
$Target = (Resolve-Path $Target).Path

$items = @('AGENTS.md', '.codex')
foreach ($item in $items) {
    $dest = Join-Path $Target $item
    if ((Test-Path $dest) -and -not $Force) {
        throw "$dest already exists. Review/merge it manually or rerun with -Force only if replacement is intentional."
    }
}

Copy-Item (Join-Path $SourceRoot 'AGENTS.md') (Join-Path $Target 'AGENTS.md') -Force
if (Test-Path (Join-Path $Target '.codex')) { Remove-Item (Join-Path $Target '.codex') -Recurse -Force }
Copy-Item (Join-Path $SourceRoot '.codex') (Join-Path $Target '.codex') -Recurse -Force

Write-Host "Installed Codex Guardrails into $Target"
Write-Host "Review AGENTS.md and .codex/config.toml for project-specific adjustments before committing."
