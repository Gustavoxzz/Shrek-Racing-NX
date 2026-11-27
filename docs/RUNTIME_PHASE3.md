# Fase 3 — fluxo desktop Nakagawa para imagem relocável

## Ensaio real

Na árvore `references/nakagawa-recomp`, o comando abaixo iniciou o build em WSL, sem manifesto e em plataforma não suportada para retail; saída em `logs/build-phase3.log` na raiz do projeto:

```sh
make -j2 CC=gcc PYTHON=python3 GAME_NAME=shrek GAME_ELF=../../original/private/BOOT.BIN GAME_BASE=0x08804000 GAME_ENTRY=0x08804678 BUILD_DIR=build/shrek3 RECOMP_OPT=-O0 RUNTIME_OPT=-O0 all
```

O pipeline gerou imagem relocada, imports e sete unidades; link terminou com código 0 em `build/shrek3/shrek`. A compilação usou `-O0`, mas não incluiu DWARF de depuração. É um binário exploratório Linux que contém componentes de interpretação VFPU; não é o produto final.

Uma segunda linkagem oficial com os mesmos parâmetros e `LINK_MAP=build/shrek3/shrek.map` terminou com código 0 e gerou mapa. `file` identifica o resultado como ELF x86-64 não stripped; isto não equivale a símbolos DWARF completos.

Duas execuções locais com `--image build/shrek3/shrek_image.bin 0x08804000 0x08804678 none none --sched`, `PSP_ISO` apontando para a ISO local, `SR_BOOT_PATH=disc0:/PSP_GAME/SYSDIR/EBOOT.BIN` e `SDL_AUDIODRIVER=dummy` registraram carregamento da imagem, 13221 registros, entrada guest, HLE e threads. A primeira usou `SR_HLELOG=1`, timeout 45 s e precisou de SIGKILL após SIGTERM; a segunda usou `SR_IOLOG=1` e `timeout -k 2s 15s`, terminando por SIGKILL (137). Logs privados em `logs/run-phase3.log` e `logs/run-io-phase3.log`. Não são execuções completas nem demonstram estabilidade.

Sequência observada: SetCompiledSdkVersion, SetCompilerVersion, criação/início de threads, chamadas GE de enfileiramento/sincronização, configuração de display 480x272 e I/O assíncrono. Log de FS: abriu `disc0:/PSP_GAME/USRDIR/PACKFILE.DAT`, leu blocos de 32768 bytes e mais tarde abriu `MOVIES/activisn.pmf`. Uma mensagem de possível spin em 0x0893ed74 / RA 0x0893bfa0 apareceu durante I/O; atividade posterior ocorreu, logo não se estabeleceu que era o bloqueio definitivo. Não há evidência de frame visível, abertura completa, progresso de corrida ou áudio real: o backend de áudio era dummy e o modo era headless. Não há trace completo de destinos indiretos ou comparação de estado com PPSSPP.

O log também mostra leituras de `activisn.pmf` até offset 1509376, com retorno de bytes. Isso demonstra I/O do vídeo, não sua decodificação ou apresentação.

Referência local: `work/nakagawa-reference`, commit `adba2471bb9963f24533b7422a5e9119bd4c7116`. Pesquisa de fonte e `--help`, sem compilar ou executar jogo nesta análise. O suporte oficial documentado (`docs/LINUX_DEVELOPMENT.md`) limita Linux/WSL a showcases de projeto headless; jogos comerciais e janela interativa não são suportados nessa plataforma. Windows 11 x64 é baseline. Um teste WSL de título retail é exploratório.

## Manifesto e endereço

`tools/title_manifest.py` valida esquema; `tools/title_codegen_plan.py` extrai exclusivamente `executable.base`, `entry`, `extra_executable_spans` e perfil do manifesto. `entry` é endereço de execução no espaço guest, não offset de arquivo. Para a base **candidata** 0x08804000 e offset 0x678 previamente analisados, a aritmética produz entry candidata 0x08804678; não é atestação da base física nem da correção de inicialização. Utilizar `codegen_profile: none`; não transportar configurações HST, bindings ou módulos não comprovados. Confirmar se `bss_metadata_source` deve ser `elf` ou `psp-header` a partir das seções e cabeçalho do título; não inventar. Perfil, manifesto, imagem e geração devem usar a mesma base. A informação sobre PRXs depende de inspeção do jogo.

Fonte `mk/pipeline.mk`: para `GAME_ELF` plano, `tools/prxload.py --env-elf <base> ... --out=<game>_image.bin` produz imagem plana realocada; `codegen.py --env-elf <game>_recomp.c --base=<base>` analisa o ELF original com a mesma base; `imports.py --env-elf <base> ...` extrai imports. Não passar imagem `.bin` realocada como entrada ELF nem aplicar relocação duas vezes. O cabeçalho `~PSP` opcional é somente entrada adicional se o manifesto determinar `psp-header`, não substitui ELF plano. `prxload.py:_image_address_bias` evita rebasing duplo de ET_EXEC com PT_LOAD igual à base; outras classes seguem semântica própria. Base/entrada não devem ser determinadas só pelo padrão no Makefile.

## Pipeline oficial de pacote

Exemplo de comandos no checkout upstream, adaptando caminhos privados e verificando o manifesto e dependências; **não foram executados neste relatório**:

```sh
python tools/title_manifest.py /CAMINHO/manifesto-publico.json
python tools/title_codegen_plan.py /CAMINHO/manifesto-publico.json --print-protected-digest
python tools/title_codegen_plan.py /CAMINHO/manifesto-publico.json \
  --game-name shrek --game-elf /CAMINHO/BOOT.BIN --build-dir /CAMINHO/build-privado \
  --manager-plan
python tools/title_codegen_plan.py /CAMINHO/manifesto-publico.json \
  --package --game-elf /CAMINHO/BOOT.BIN --output-dir /CAMINHO/pacote-privado
```

`--module-dir` aponta para PRXs declarados quando necessários; `--psp-header` para EBOOT.BIN original quando exigido. `--package` exige diretório dedicado não versionado. Planejamento e documentação não garantem compatibilidade de runtime. A compilação desktop oficial usa SDL3 3.x, Vulkan, compilador C, Python e Make; fontes/shaders de runtime são ligados junto aos objetos gerados, biblioteca SDL3/Vulkan e `-lm` no Linux (`mk/housekeeping.mk`, Makefile). A compilação anterior isolada de objetos do jogo não realizou link de runtime. O planner faz duas fases, reconstituindo pipeline e arquivo resposta do link, produzindo binário e metadata. Recomenda-se usar esta rota antes de tentar link manual.

`python tools/nk_cli.py bringup --help` mostra `bringup ISO --work-dir DIR --report REPORT [--user-data-root DIR] [--launch-timeout 1..120] [--capture-rounds 1..16]`: processo experimental automático com staging, compilação e execução; as capturas para código instalado em runtime têm requisitos próprios e não estabelecem a ausência de interpretação no produto final. Usuário proíbe interpretação MIPS no produto final, de modo que deve ser auditado dispatcher/fallback, independentemente do resultado do bringup. Manter workspace, dados e logs derivados privados. `--instruction-trace` é opcional e cria trace privado.

## Inicialização

`src/rt/driver.c` exige modo imagem para PRX relocável: carrega bytes no guest em base dada, inicializa memória, registra funções geradas e procura entry; `--sched` executa scheduler sem janela, `--gui` inicializa janela e scheduler. Forma do driver, somente depois de link e de validar pacote/endereço:

```sh
PSP_ISO='/CAMINHO/jogo.iso' SR_BOOT_PATH='disc0:/PSP_GAME/SYSDIR/EBOOT.BIN' \
  /CAMINHO/binario --image /CAMINHO/shrek_image.bin 0x08804000 0x08804678 none none --sched
```

Comando é ilustração de diagnóstico, **não executado**; não substituir `SR_BOOT_PATH`, sistema de arquivos ou nome de arquivo antes de verificar o launch plan do título. O launcher oficial resolve base e run-entry a partir de manifesto; fallback_entry, se declarado, tem precedência sobre executable.entry, portanto não adicionar fallback sem evidência. O launcher limpa variáveis herdadas de ISO/boot, define `PSP_ISO`, `SR_BOOT_PATH`, `SR_DATAROOT`, `SR_LOOSE_CONTENT_ROOTS`, `SR_USER_DATA_ROOT`, controla áudio/vídeo e monta argv com `none none`; importa refletir os mesmos bindings e manter saves/logs privados. Use `python tools/nk_cli.py launch --help` para rota de jogo preparado.

Falta validar inicialização de GP, argumentos, BSS, HLE, módulos, gerenciamento de imagem, fluxo gráfico e interrupção segura no caminho escolhido; link e primeiro frame não foram demonstrados. Fontes: `docs/PORTING.md`, `docs/SETUP.md`, `docs/LINUX_DEVELOPMENT.md`, `docs/ARCHITECTURE.md`, `mk/pipeline.mk`, `mk/housekeeping.mk`, `tools/title_codegen_plan.py`, `tools/nk_core/launcher.py`, `src/rt/driver.c`.
