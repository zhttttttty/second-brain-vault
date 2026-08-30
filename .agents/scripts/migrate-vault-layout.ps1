[CmdletBinding(DefaultParameterSetName = "DryRun")]
param(
    [Parameter(Mandatory = $true)]
    [string]$Vault,

    [Parameter(ParameterSetName = "DryRun")]
    [switch]$DryRun,

    [Parameter(ParameterSetName = "Apply", Mandatory = $true)]
    [switch]$Apply
)

$ErrorActionPreference = "Stop"
$isDryRun = -not $Apply
$utf8NoBom = [System.Text.UTF8Encoding]::new($false)
$root = [System.IO.Path]::GetFullPath((Resolve-Path -LiteralPath $Vault).Path).TrimEnd(
    [System.IO.Path]::DirectorySeparatorChar,
    [System.IO.Path]::AltDirectorySeparatorChar
)
$rootPrefix = $root + [System.IO.Path]::DirectorySeparatorChar

if (-not (Test-Path -LiteralPath (Join-Path $root "AGENTS.md") -PathType Leaf)) {
    throw "Vault root verification failed: AGENTS.md is missing under $root"
}

function Resolve-WithinVault {
    param([Parameter(Mandatory = $true)][string]$RelativePath)

    $candidate = [System.IO.Path]::GetFullPath((Join-Path $root $RelativePath))
    if ($candidate -ne $root -and -not $candidate.StartsWith($rootPrefix, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "Path escapes the Vault: $RelativePath"
    }
    return $candidate
}

$directoryMap = @(
    [pscustomobject]@{ Old = "00_System"; New = "System"; Optional = $false },
    [pscustomobject]@{ Old = "01_Context"; New = "Context"; Optional = $false },
    [pscustomobject]@{ Old = "02_Daily"; New = "01_Daily"; Optional = $false },
    [pscustomobject]@{ Old = "03_Projects"; New = "02_Projects"; Optional = $false },
    [pscustomobject]@{ Old = "04_Knowledge"; New = "03_Knowledge"; Optional = $false },
    [pscustomobject]@{ Old = "05_References"; New = "04_References"; Optional = $false },
    [pscustomobject]@{ Old = "06_Tasks"; New = "05_Tasks"; Optional = $false },
    [pscustomobject]@{ Old = "07_Bases"; New = "Bases"; Optional = $false },
    [pscustomobject]@{ Old = "20_Archive"; New = "06_Archive"; Optional = $true }
)

$templateMoves = @(
    [pscustomobject]@{ Before = "02_Daily/.templates/Daily_Note.md"; After = "01_Daily/.templates/Daily_Note.md"; New = "Templates/Daily_Note.md" },
    [pscustomobject]@{ Before = "03_Projects/.templates/Project.md"; After = "02_Projects/.templates/Project.md"; New = "Templates/Project.md" }
)

$replacementMap = [ordered]@{
    "├── .templates/`r`n│   └── Project.md       # 单页项目模板`r`n" = ""
    "├── .templates/`n│   └── Project.md       # 单页项目模板`n" = ""
    'template_root = root / "04_Knowledge" / "00_Cards" / ".templates"' = 'template_root = root / "Templates" / "Cards"'
    'templates = list((root / "04_Knowledge" / "00_Cards" / ".templates").glob' = 'templates = list((root / "Templates" / "Cards").glob'
    'templates = list((card_root / ".templates").glob' = 'templates = list((root / "Templates" / "Cards").glob'
    'elif ".templates" not in path.parts:' = 'elif "Templates" not in path.parts:'
    'if ".templates" not in path.parts and' = 'if "Templates" not in path.parts and'
    '完整模板见 `.templates/` 目录' = '完整模板见根目录 `Templates/Cards/`'
    '从 `.templates/` 找对应类型的模板' = '从根目录 `Templates/Cards/` 找对应类型的模板'
    '不要在 `.templates/` 里' = '不要误放进 `Templates/Cards/`'
    '`.templates/` 提供统一模板' = '根目录 `Templates/` 提供统一模板'
    '将 `.templates/Project.md`' = '将根目录 `Templates/Project.md`'
    '复制 `.templates/Daily_Note.md`' = '使用 `Templates/Daily_Note.md`'
    '模板文件统一放在 `.templates/`' = '模板文件统一放在根目录 `Templates/`'
    '`.templates/` 中尚未实例化的模板' = '`Templates/` 中尚未实例化的模板'
    '使用 `.templates/Daily_Note.md`' = '使用 `Templates/Daily_Note.md`'
    '项目模板为 `.templates/Project.md`' = '项目模板为 `Templates/Project.md`'
    '  - `.templates/` — 标准化卡片模板' = '  - `Templates/Cards/` — 标准化卡片模板'
    "04_Knowledge/00_Cards/.templates" = "Templates/Cards"
    "04_Knowledge\00_Cards\.templates" = "Templates\Cards"
    "02_Daily/.templates" = "Templates"
    "02_Daily\.templates" = "Templates"
    "03_Projects/.templates" = "Templates"
    "03_Projects\.templates" = "Templates"
    "03_Projects/.templates/Project.md" = "Templates/Project.md"
    "03_Projects\.templates\Project.md" = "Templates\Project.md"
    "02_Daily/.templates/Daily_Note" = "Templates/Daily_Note"
    "02_Daily\.templates\Daily_Note" = "Templates\Daily_Note"
    "00_Cards/.templates" = "Templates/Cards"
    "00_Cards\.templates" = "Templates\Cards"
    "00_System" = "System"
    "01_Context" = "Context"
    "02_Daily" = "01_Daily"
    "03_Projects" = "02_Projects"
    "04_Knowledge" = "03_Knowledge"
    "05_References" = "04_References"
    "06_Tasks" = "05_Tasks"
    "07_Bases" = "Bases"
    "20_Archive" = "06_Archive"
}

$conflicts = [System.Collections.Generic.List[string]]::new()
$plannedDirectories = [System.Collections.Generic.List[object]]::new()
foreach ($item in $directoryMap) {
    $source = Resolve-WithinVault $item.Old
    $target = Resolve-WithinVault $item.New
    $sourceExists = Test-Path -LiteralPath $source
    $targetExists = Test-Path -LiteralPath $target

    if ($sourceExists -and $targetExists) {
        $conflicts.Add("Both source and target exist: $($item.Old) -> $($item.New)")
    }
    elseif ($sourceExists) {
        $plannedDirectories.Add($item)
    }
    elseif (-not $targetExists -and -not $item.Optional) {
        $conflicts.Add("Required directory is missing on both sides: $($item.Old) / $($item.New)")
    }
}

if ($conflicts.Count -gt 0) {
    $conflicts | ForEach-Object { Write-Error $_ }
    throw "Preflight failed with $($conflicts.Count) conflict(s). Nothing was changed."
}

$cardTemplateSourceBefore = Resolve-WithinVault "04_Knowledge/00_Cards/.templates"
$cardTemplateSourceAfter = Resolve-WithinVault "03_Knowledge/00_Cards/.templates"
$cardTemplateTarget = Resolve-WithinVault "Templates/Cards"
$existingCardTemplateSource = if (Test-Path -LiteralPath $cardTemplateSourceBefore) {
    $cardTemplateSourceBefore
} elseif (Test-Path -LiteralPath $cardTemplateSourceAfter) {
    $cardTemplateSourceAfter
} else {
    $null
}
if ($existingCardTemplateSource -and (Test-Path -LiteralPath $cardTemplateTarget)) {
    $conflicts.Add("Both card template source and target exist")
}

foreach ($move in $templateMoves) {
    $sourceBefore = Resolve-WithinVault $move.Before
    $sourceAfter = Resolve-WithinVault $move.After
    $target = Resolve-WithinVault $move.New
    $sourceExists = (Test-Path -LiteralPath $sourceBefore) -or (Test-Path -LiteralPath $sourceAfter)
    if ($sourceExists -and (Test-Path -LiteralPath $target)) {
        $conflicts.Add("Both template source and target exist: $($move.Before) -> $($move.New)")
    }
}
if ($conflicts.Count -gt 0) {
    $conflicts | ForEach-Object { Write-Error $_ }
    throw "Template preflight failed. Nothing was changed."
}

Write-Output "Mode: $(if ($isDryRun) { 'DRY RUN' } else { 'APPLY' })"
Write-Output "Vault: $root"
foreach ($item in $plannedDirectories) {
    Write-Output "Directory: $($item.Old) -> $($item.New)"
}
Write-Output "Templates: distributed .templates -> Templates/"

if (-not $isDryRun -and $plannedDirectories.Count -gt 0) {
    $stageName = ".__vault_layout_migration_$([DateTime]::UtcNow.ToString('yyyyMMddHHmmssfff'))"
    $stageRoot = Resolve-WithinVault $stageName
    New-Item -ItemType Directory -Path $stageRoot | Out-Null

    foreach ($item in $plannedDirectories) {
        $source = Resolve-WithinVault $item.Old
        $staged = Join-Path $stageRoot $item.Old
        Move-Item -LiteralPath $source -Destination $staged
    }
    foreach ($item in $plannedDirectories) {
        $staged = Join-Path $stageRoot $item.Old
        $target = Resolve-WithinVault $item.New
        Move-Item -LiteralPath $staged -Destination $target
    }
    Remove-Item -LiteralPath $stageRoot
}

if (-not $isDryRun) {
    $archiveRoot = Resolve-WithinVault "06_Archive"
    if (-not (Test-Path -LiteralPath $archiveRoot)) {
        New-Item -ItemType Directory -Path $archiveRoot | Out-Null
    }

    $templatesRoot = Resolve-WithinVault "Templates"
    $cardsRoot = Resolve-WithinVault "Templates/Cards"
    New-Item -ItemType Directory -Path $templatesRoot -Force | Out-Null
    New-Item -ItemType Directory -Path $cardsRoot -Force | Out-Null

    foreach ($move in $templateMoves) {
        $source = Resolve-WithinVault $move.After
        $target = Resolve-WithinVault $move.New
        if (Test-Path -LiteralPath $source -PathType Leaf) {
            Move-Item -LiteralPath $source -Destination $target
        }
    }

    $cardSource = Resolve-WithinVault "03_Knowledge/00_Cards/.templates"
    if (Test-Path -LiteralPath $cardSource -PathType Container) {
        foreach ($file in Get-ChildItem -LiteralPath $cardSource -File) {
            $target = Join-Path $cardsRoot $file.Name
            if (Test-Path -LiteralPath $target) {
                throw "Card template target already exists: $target"
            }
            Move-Item -LiteralPath $file.FullName -Destination $target
        }
    }

    $oldTemplateDirectories = @(
        "01_Daily/.templates",
        "02_Projects/.templates",
        "03_Knowledge/00_Cards/.templates"
    )
    foreach ($relative in $oldTemplateDirectories) {
        $path = Resolve-WithinVault $relative
        if ((Test-Path -LiteralPath $path -PathType Container) -and
            (Get-ChildItem -LiteralPath $path -Force | Measure-Object).Count -eq 0) {
            Remove-Item -LiteralPath $path
        }
    }
}

$allowedExtensions = @(".md", ".json", ".yaml", ".yml", ".py", ".sh", ".ps1", ".base", ".canvas", ".txt")
$specialNames = @("LICENSE", ".gitignore")
$scriptPath = [System.IO.Path]::GetFullPath($MyInvocation.MyCommand.Path)
$changelogPath = Resolve-WithinVault "03_Knowledge/CHANGELOG.md"
$legacyChangelogPath = Resolve-WithinVault "04_Knowledge/CHANGELOG.md"
$changedFiles = [System.Collections.Generic.List[string]]::new()

$files = Get-ChildItem -LiteralPath $root -Recurse -Force -File | Where-Object {
    $_.FullName -notlike "$rootPrefix.git$([System.IO.Path]::DirectorySeparatorChar)*" -and
    $_.FullName -notlike "*$([System.IO.Path]::DirectorySeparatorChar)__pycache__$([System.IO.Path]::DirectorySeparatorChar)*" -and
    -not $_.LinkType -and
    ($allowedExtensions -contains $_.Extension.ToLowerInvariant() -or $specialNames -contains $_.Name) -and
    ([System.IO.Path]::GetFullPath($_.FullName) -ne $scriptPath) -and
    ([System.IO.Path]::GetFullPath($_.FullName) -ne $changelogPath) -and
    ([System.IO.Path]::GetFullPath($_.FullName) -ne $legacyChangelogPath)
}

foreach ($file in $files) {
    $content = [System.IO.File]::ReadAllText($file.FullName)
    $updated = $content
    foreach ($entry in $replacementMap.GetEnumerator()) {
        $updated = $updated.Replace([string]$entry.Key, [string]$entry.Value)
    }
    if ($updated -ne $content) {
        $relative = [System.IO.Path]::GetRelativePath($root, $file.FullName).Replace("\", "/")
        $changedFiles.Add($relative)
        if (-not $isDryRun) {
            [System.IO.File]::WriteAllText($file.FullName, $updated, $utf8NoBom)
        }
    }
}

$migrationMarker = ".agents/scripts/migrate-vault-layout.ps1"
$changelogNeedsEntry = $false
if (Test-Path -LiteralPath $changelogPath -PathType Leaf) {
    $changelogContent = [System.IO.File]::ReadAllText($changelogPath)
    $changelogNeedsEntry = -not $changelogContent.Contains($migrationMarker)
    if ($changelogNeedsEntry -and -not $isDryRun) {
        $today = [DateTime]::Now.ToString("yyyy-MM-dd")
        $newline = if ($changelogContent.Contains("`r`n")) { "`r`n" } else { "`n" }
        $entry = '- `架构迁移` | 将旧编号目录迁移为 `01_Daily` 至 `06_Archive` 内容区，并将 `Context`、`System`、`Bases`、`Templates` 设为无编号支撑层 | `.agents/scripts/migrate-vault-layout.ps1`'
        $heading = "## $today"
        $headingIndex = $changelogContent.IndexOf($heading, [System.StringComparison]::Ordinal)
        if ($headingIndex -ge 0) {
            $lineEnd = $changelogContent.IndexOf("`n", $headingIndex)
            if ($lineEnd -lt 0) { $lineEnd = $changelogContent.Length - 1 }
            $insertAt = $lineEnd + 1
            $changelogContent = $changelogContent.Insert($insertAt, $newline + $entry + $newline)
        } else {
            $firstHistory = $changelogContent.IndexOf("$newline## ", [System.StringComparison]::Ordinal)
            $block = "$newline## $today$newline$newline$entry$newline"
            if ($firstHistory -ge 0) {
                $changelogContent = $changelogContent.Insert($firstHistory, $block)
            } else {
                $changelogContent += $block
            }
        }
        $updatedPattern = [regex]::new('(?m)^updated:\s*.*$')
        if ($updatedPattern.IsMatch($changelogContent)) {
            $changelogContent = $updatedPattern.Replace($changelogContent, "updated: $today", 1)
        }
        [System.IO.File]::WriteAllText($changelogPath, $changelogContent, $utf8NoBom)
    }
}

Write-Output "Reference files: $($changedFiles.Count)"
$changedFiles | Sort-Object | ForEach-Object { Write-Output "  $_" }
Write-Output "Changelog: $(if ($changelogNeedsEntry) { if ($isDryRun) { 'would append migration entry' } else { 'appended migration entry' } } else { 'already recorded or unavailable' })"
if ($isDryRun) {
    Write-Output "Dry run complete. Re-run with -Apply to make changes."
} else {
    Write-Output "Migration applied. Run stale-path scan and Vault validation before committing."
}
