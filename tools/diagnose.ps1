$ErrorActionPreference = 'Continue'
Write-Output 'Windows tools:'
foreach ($name in @('git','python','cmake','ninja','gcc','java','wsl')) {
    $command = Get-Command $name -ErrorAction SilentlyContinue
    if ($command) { Write-Output ("{0}: {1}" -f $name, $command.Source) }
    else { Write-Output ("{0}: not found" -f $name) }
}
Write-Output 'WSL tools:'
foreach ($name in @('python3','git','gcc','make','cmake','ninja','java')) {
    $location = & wsl -d Ubuntu -- which $name 2>$null
    if ($LASTEXITCODE -eq 0) { Write-Output ("{0}: {1}" -f $name, $location) }
    else { Write-Output ("{0}: not found" -f $name) }
}
& wsl -d Ubuntu -- test -d /opt/devkitpro
if ($LASTEXITCODE -eq 0) { Write-Output 'devkitPro: present' } else { Write-Output 'devkitPro: not found' }
