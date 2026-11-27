# Fase 4 — compatibilidade e ensaio de link Switch

Estado: experimento local privado. Cópias isoladas, sem alterações ao projeto principal. Referências: Ben10 `a2a30be95d7cfc7cdf66e906093a24efe1f992de`, Nakagawa base `70b1d3f83bd2ac445d1a76d6fb05b0bbbbdc5bfa`, upstream atual `adba2471bb9963f24533b7422a5e9119bd4c7116`. Toolchain da imagem oficial devkitPro fixada em `docs/SWITCH_PHASE2.md`.

| Superfície | Gerador 70b1 / runtime Ben10 | Gerador adba / runtime Ben10 | Evidência e limite |
|---|---|---|---|
| Código gerado e headers | Gerador produziu 22 chunks e registro; compilação e link retornaram 0 | Incompatível diretamente | Registro adba não compila: faltam `SrVfpuUse`, `sr_vfpu_report_unverified_uses`; chunk adba falha em `sr_fpu_sqrt_s`, `SR_VFPU_ACCESS_REFUSED` (logs fase 3). |
| CpuState ABI | ambos headers declaram ABI 3, mas diferem em bytes | ambos declaram ABI 3 | O número igual não prova layouts e semântica de todas APIs. |
| Configuração de título | `title_runtime_config.py` 70b1 gerou schema 12 genérico | Não demonstrada | Schema 12 corresponde ao `#if` do `title_config.c` Ben10. Config genérica não prova correção do título. |
| Imagem/base/entry | base 0x08804000, entrada 0x08804678 | desktop exploratório usou os mesmos valores | Base observada no PPSSPP, sem verificação em hardware; código Ben10 tem caminho SD fixo e configurações que exigem adaptação. |
| Dispatcher/AOT | lista do runtime inclui `guest_interp.c` e `vfpu_interp.c` | adba gerado compilado faz referência `sr_vfpu_interp` | A proibição de interpretação MIPS/VFPU no produto exige implementação AOT e auditoria. Gerador base tem 5670 ocorrências textuais em 17 unidades; não mede frequência em execução. |
| GE, audio, arquivos, sincronização | backend deko3d e shim Ben10 presentes | não testado como conjunto | Ben10 tem mudança específica de semáforo e GE assíncrono; fidelidade com Shrek não demonstrada. |
| Módulos PRX | nenhum declarado neste ensaio | não demonstrado | Ausência no comando de build não prova que jogo não carregue módulos. |

Emissão com `python3 tools/codegen.py <BOOT.BIN> <privado>/shrek_recomp.c --base=0x08804000 --funcs-per-chunk=2000 --target-chunk-bytes=4000000` retornou 0, 13221 funções e 0 fallbacks declarados; o conceito de cobertura estática não garante ausência de chamadas à interpretação e nem correção semântica. Header de configuração genérica foi gerado pelo mesmo commit, sem manifesto, apenas para avaliar link. `reproduce.sh` documenta comandos completos e exige rootfs oficial já instalado, espaço isolado e entrada privada; não executa limpeza destrutiva. Código gerado em `generated/`, logs e eventual binário são privados, proibida publicação.

Comando de build: `make -f Makefile.switch -j2 PACKAGE_DIR=/tmp/shrek-phase4/generated TITLE=shrek ENTRY=0x08804678 TARGET=shrek-racing-nx APP_NAME=Shrek-Racing-NX OPT_RT=-O0 OPT_GEN=-O0`, em cópia do Ben10 dentro do rootfs. O código não foi adaptado: `switch_main.c` ainda nomeia diretório `ben10-psp`, usa configuração e imagem esperadas do projeto referencial. Por isso, ainda que link bem-sucedido, qualquer NRO é apenas artefato experimental, não inicialização validada, não deve ser enviado/instalado como port. Não houve teste em hardware, renderização, áudio, save ou desempenho.

## Resultado do link

O Make terminou com **código 0**, compilou os shaders e gerou ELF, mapa, NACP e NRO. `readelf -h` identifica ELF64 little-endian, AArch64, tipo DYN; resultados e advertências de assembler estão em `build.log`, inspeção em `readelf.txt`, arquivos privados em `private-artifacts/`. `nm` detectou no ELF `sr_guest_interp_run`, `sr_guest_interp_run_internal`, `sr_guest_interp_run_with_boundary` e `sr_vfpu_interp` (ver `interpreter-symbols.txt`). A presença confirma componentes compilados/linkados, não prova frequência de uso durante execução; a restrição do produto final continua pendente. O `.nro` é 38.535.225 bytes e é um artefato privado de experimento, sem validação funcional ou em console, com caminho SD e iconografia Ben10 ainda presentes. Não instalar nem distribuir. Nenhum marco de jogo executável é comprovado.
