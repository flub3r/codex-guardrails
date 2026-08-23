param(
    [Parameter(Mandatory=$true)][string]$Target
)

$ErrorActionPreference = 'Stop'
$SourceRoot = Split-Path -Parent $PSScriptRoot
$Target = (Resolve-Path -LiteralPath $Target).Path

$items = @('AGENTS.md', '.codex')
foreach ($item in $items) {
    $dest = Join-Path $Target $item
    if (Test-Path -LiteralPath $dest) {
        throw "$dest already exists. Nothing was changed; review and merge the existing configuration manually."
    }
}

Copy-Item -LiteralPath (Join-Path $SourceRoot 'AGENTS.md') -Destination (Join-Path $Target 'AGENTS.md')
Copy-Item -LiteralPath (Join-Path $SourceRoot '.codex') -Destination (Join-Path $Target '.codex') -Recurse

Write-Host "Installed Codex Guardrails into $Target"
Write-Host "Review AGENTS.md and .codex/config.toml for project-specific adjustments before committing."
