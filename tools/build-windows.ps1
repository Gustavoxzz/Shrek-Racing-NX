param([int]$Jobs = 2)
$ErrorActionPreference = 'Stop'
$project = Split-Path -Parent $PSScriptRoot
$workspace = Split-Path -Parent (Split-Path -Parent $project)
$repo = Join-Path $workspace 'work/nakagawa-reference'
$toolBin = Join-Path $workspace 'work/msys64/ucrt64/bin'
$elf = Join-Path $workspace 'work/game-private/BOOT.BIN'
foreach ($item in @($repo, $toolBin, $elf)) {
    if (-not (Test-Path -LiteralPath $item)) { throw "Pré-requisito não encontrado: $item" }
}
if ($Jobs -lt 1) { throw 'Jobs deve ser positivo.' }
$oldPath = $env:PATH
try {
    $env:PATH = "$toolBin;$oldPath"
    Push-Location $repo
    try {
        & (Join-Path $toolBin 'mingw32-make.exe') "-j$Jobs" CC=gcc PYTHON=python GAME_NAME=shrek "GAME_ELF=$elf" GAME_BASE=0x08804000 GAME_ENTRY=0x08804678 BUILD_DIR=build/shrek-win4 'RECOMP_OPT=-O0 -g1' 'RUNTIME_OPT=-O0 -g' LINK_MAP=build/shrek-win4/shrek.map POWERSHELL=pwsh all
        if ($LASTEXITCODE -ne 0) { throw "Build falhou: $LASTEXITCODE" }
    } finally { Pop-Location }
} finally { $env:PATH = $oldPath }
