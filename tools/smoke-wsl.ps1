param(
    [Parameter(Mandatory = $true)][string]$Iso,
    [int]$ExitVblank = 900,
    [int]$TimeoutSeconds = 35
)
$ErrorActionPreference = 'Stop'
if ($ExitVblank -lt 1 -or $TimeoutSeconds -lt 1) { throw 'Os limites devem ser positivos.' }
$root = Split-Path -Parent $PSScriptRoot
$isoItem = Get-Item -LiteralPath $Iso
$isoLinux = (& wsl -d Ubuntu -- wslpath -a $isoItem.FullName).Trim()
if ($LASTEXITCODE -ne 0) { throw 'Falha ao converter caminho da ISO.' }
$repo = (& wsl -d Ubuntu -- wslpath -a (Join-Path $root 'references/nakagawa-recomp')).Trim()
if ($LASTEXITCODE -ne 0) { throw 'Falha ao converter caminho do checkout.' }
$log = Join-Path $root 'logs/smoke-wsl.log'
New-Item -ItemType Directory -Force (Split-Path $log) | Out-Null
& wsl -d Ubuntu --cd $repo -- env "PSP_ISO=$isoLinux" 'SR_BOOT_PATH=disc0:/PSP_GAME/SYSDIR/EBOOT.BIN' 'SR_IOLOG=1' 'SR_MPEGLOG=1' 'SR_VIDEO=offscreen' "SR_EXIT_AT_VBLANK=$ExitVblank" 'SDL_AUDIODRIVER=dummy' timeout -k 3s "${TimeoutSeconds}s" build/shrek3/shrek --image build/shrek3/shrek_image.bin 0x08804000 0x08804678 none none --gui *> $log
$result = $LASTEXITCODE
Write-Output "Runtime exit code: $result; log: $log"
& wsl -d Ubuntu --cd $repo -- python3 ../../tools/smoke_markers.py ../../logs/smoke-wsl.log
if ($result -ne 0) { throw "Runtime não encerrou normalmente: $result" }
