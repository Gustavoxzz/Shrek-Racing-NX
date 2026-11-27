param([Parameter(Mandatory=$true)][string]$Iso, [int]$ExitVblank=120, [int]$TimeoutSeconds=20)
$ErrorActionPreference = 'Stop'
if ($ExitVblank -lt 1 -or $TimeoutSeconds -lt 1) { throw 'Os limites devem ser positivos.' }
$project = Split-Path -Parent $PSScriptRoot
$workspace = Split-Path -Parent (Split-Path -Parent $project)
$repo = Join-Path $workspace 'work/nakagawa-reference'
$bin = Join-Path $project 'build/windows-phase4/shrek.exe'
$dlls = Join-Path $workspace 'work/msys64/ucrt64/bin'
$isoItem = Get-Item -LiteralPath $Iso
foreach ($path in @($repo, $bin, $dlls, (Join-Path $repo 'build/shrek-win4/shrek_image.bin'))) {
    if (-not (Test-Path -LiteralPath $path)) { throw "Pré-requisito não encontrado: $path" }
}
$names = @('PATH','PSP_ISO','SR_BOOT_PATH','SDL_AUDIODRIVER','SDL_VIDEODRIVER','SR_EXIT_AT_VBLANK','SR_IOLOG')
$old = @{}; foreach ($name in $names) { $old[$name] = [Environment]::GetEnvironmentVariable($name, 'Process') }
try {
    $env:PATH = "$dlls;$env:PATH"
    $env:PSP_ISO = $isoItem.FullName
    $env:SR_BOOT_PATH = 'disc0:/PSP_GAME/SYSDIR/EBOOT.BIN'
    $env:SDL_AUDIODRIVER = 'dummy'; $env:SDL_VIDEODRIVER = 'dummy'
    $env:SR_EXIT_AT_VBLANK = "$ExitVblank"; $env:SR_IOLOG = '1'
    $logs = Join-Path $project 'logs'; New-Item -ItemType Directory -Force $logs | Out-Null
    $process = Start-Process -FilePath $bin -ArgumentList '--image','build/shrek-win4/shrek_image.bin','0x08804000','0x08804678','none','none','--sched' -WorkingDirectory $repo -WindowStyle Hidden -RedirectStandardOutput (Join-Path $logs 'smoke-windows-stdout.log') -RedirectStandardError (Join-Path $logs 'smoke-windows-stderr.log') -PassThru
    if (-not $process.WaitForExit($TimeoutSeconds * 1000)) { Stop-Process -Id $process.Id -Force; throw 'Limite excedido; processo encerrado.' }
    Write-Output "Runtime exit code: $($process.ExitCode)"
    if ($process.ExitCode -ne 0) { throw 'Runtime não encerrou normalmente.' }
} finally { foreach ($name in $names) { [Environment]::SetEnvironmentVariable($name, $old[$name], 'Process') } }
