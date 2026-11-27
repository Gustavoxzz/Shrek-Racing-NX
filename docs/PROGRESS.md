# Progresso — 2026-11-26

## Fase 3 — 2026-11-27

- PPSSPP v1.20.4 carregou a cópia local na base 0x08804000, entry 0x08804678 e GP 0x08a6ea80. Não é medição de hardware; SP/RA não foram capturados. Evidência e relatório privados em original/private.
- A suíte nativa da fase 2 terminou com falha no teste de gravação de vídeo: a verificação de espaço informou 1651 MiB, abaixo dos 4096 MiB exigidos. `psmf_media_selftest` passou 76995 verificações antes da falha. O teste de texturas passou anteriormente no filesystem Linux. Não afirmar aprovação global.
- M3.1–M3.5: build exploratório em WSL pelo Make oficial terminou com código 0, e execução headless carregou memória, registrou funções, entrou em 0x08804678, chamou HLE e leu PACKFILE.DAT. Linux não é rota oficialmente suportada pelo upstream para jogos comerciais; binário inclui caminhos de interpretação VFPU. Evidência e limites em RUNTIME_PHASE3.md e logs privados. Não foi validado frame ou estabilidade.
- M3.10: sete unidades e registro compilaram separadamente para ARM64, usando headers upstream e compatibilidade Switch; objeto verificado ELF64/AArch64. Isso não valida a ABI completa nem a linkagem com Ben10. Ver SWITCH_PHASE3.md; os objetos permanecem privados.

## Fase 2 — 2026-11-27

- O teste `texrepl-selftest`, que falhou em `/mnt/c` por limitações do sistema de arquivos, passou em checkout no filesystem Linux. A repetição de `native-core-tests` está em andamento; não há resultado global neste registro. Log em `logs/native-phase2.log` (ignorado).
- `EBOOT.BIN` decriptado localmente pela API do Nakagawa é idêntico byte a byte ao `BOOT.BIN` segundo `cmp`. Não há validação independente da autenticidade da cópia. Relatório e scripts privados em `original/private/report.md` e no mesmo diretório.
- Exemplos oficiais Switch `application` e `deko_basic` compilaram com sucesso, incluindo shaders, ELF AArch64 e NRO; sem teste em hardware. Ver `SWITCH_PHASE2.md` para ambiente isolado e reprodução.
- `sh tools/compile-generated.sh` terminou com status 0 em WSL/GCC 15.2: compilou o registro e as sete unidades anteriores para objetos com `-O0 -g1`. Não houve ligação, executável ou execução. O script e os objetos pressupõem os dados privados locais; objetos são ignorados.
- A inspeção do GP aponta relocação para `0x08a6ea80` com base `0x08804000`; a equivalência BOOT/EBOOT foi confirmada localmente, e a base posteriormente observada no PPSSPP. O hardware PSP não foi inspecionado.
- O relatório CFG indica 780 chamadas e 90 saltos computados sem destino estático; não representam necessariamente falhas em execução. Ver COVERAGE_PHASE2.md para divergência de contagens e limites.

O projeto está em pesquisa inicial. Não existe port jogável, NRO ou teste em Switch. Os marcos permanecem pendentes.

- M00 parcial: WSL2 Ubuntu disponível. Ferramentas básicas instaladas; Switch SDK e validação completa pendentes. Detalhes em ENVIRONMENT.md.
- M01 parcial: referências Ben 10 NX e Nakagawa obtidas e comparação inicial registrada em REFERENCE_ANALYSIS.md. A auditoria integral e compatibilidade ainda não foram concluídas.
- M02 parcial: ISO local identifica ULUS10194, DISC_VERSION 1.01, firmware 2.82. Hash e catálogo local estão em original/private, ignorado pelo Git; o hash identifica esta cópia, não comprova autenticidade ou integridade contra fonte independente. Manifesto de título ainda depende de configuração validada.
- M03 parcial: BOOT.BIN é ELF MIPS PSP relocável, entry relativa 0x678; EBOOT.BIN é contêiner ~PSP. O loader upstream aplicou 59.801 relocações com base candidata 0x08804000 e entrada resultante 0x08804678; essa escolha não foi confirmada no hardware. Foram identificadas 23 bibliotecas de imports e assinatura PAK no PACKFILE.DAT. Relatório privado em original/private.
- M04 parcial: ensaio do gerador com a base candidata produziu sete unidades C e mensagem de conclusão. O wrapper perdeu o status real de saída; não alegar exit code válido. Relatório do gerador: 13.221 funções traduzidas, 1.160 palavras não atribuídas, 16.120 palavras com conflito de posse e 870 arestas indiretas não resolvidas. Não houve compilação ou execução; métricas não comprovam correção. Saídas privadas em generated/shrek-attempt.
- Testes públicos: em WSL, Python 3.14.4, `tools/test-public-wsl.ps1` validou manifesto e plano sintéticos e executou 64 testes com sucesso, sem skips, após instalar `python-is-python3`. Uma tentativa intermediária havia falhado pela ausência do comando `python`. Isto não valida execução do jogo.
- `native-core-tests`: tentativa falhou na ligação por ausência de SDL3 e Vulkan; NKSTATE passou 1.212 verificações antes da falha. A suíte completa não está validada.

Referências e ambientes locais são ignorados pelo Git; ver REFERENCES.md e BUILD.md para reconstrução. Não versionar saídas derivadas do jogo.
