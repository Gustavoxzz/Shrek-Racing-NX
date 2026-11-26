$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$reference = Join-Path $root 'references/nakagawa-recomp'
if (-not (Test-Path (Join-Path $reference 'tools/title_manifest.py'))) { throw 'Clone a revisão documentada do Nakagawa em references/nakagawa-recomp.' }
$linuxPath = (& wsl -d Ubuntu -- wslpath -a $reference).Trim()
if ($LASTEXITCODE -ne 0) { throw 'Falha ao converter caminho para WSL.' }
& wsl -d Ubuntu --cd $linuxPath -- python3 tools/title_manifest.py assets/titles/synthetic.json
if ($LASTEXITCODE -ne 0) { throw 'Validação de manifesto falhou.' }
& wsl -d Ubuntu --cd $linuxPath -- python3 tools/title_codegen_plan.py assets/titles/synthetic.json --print-protected-digest
if ($LASTEXITCODE -ne 0) { throw 'Planejamento sintético falhou.' }
& wsl -d Ubuntu --cd $linuxPath -- env PYTHONPATH=tools python3 -m unittest tools.test_title_codegen_synthetic tools.test_title_codegen_plan
if ($LASTEXITCODE -ne 0) { throw "Testes públicos falharam: $LASTEXITCODE" }
