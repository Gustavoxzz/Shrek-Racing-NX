# Referências: análise inicial (2026-11-26)

Fontes clonadas em work/ para inspeção, sem alterar o projeto principal:
- Ben10 NX: a2a30be95d7cfc7cdf66e906093a24efe1f992de.
- Nakagawa upstream: adba2471bb9963f24533b7422a5e9119bd4c7116.
- Base declarada pelo Ben10: 70b1d3f83bd2ac445d1a76d6fb05b0bbbbdc5bfa.

O README do Ben10 afirma que é derivado daquela revisão, com mudanças de novembro de 2026. A comparação upstream da base até HEAD em src/rt, tools/codegen.py e assets/titles mostra 297 arquivos modificados, 113982 inserções e 8148 exclusões; não é seguro presumir compatibilidade binária entre o backend Switch e o gerador atual. Começar integração pelo par Ben10/base fixada e avaliar alterações do upstream seletivamente, ou estabelecer um teste explícito de contrato entre a saída atual e o runtime Switch antes de misturá-los. Ainda não há validação dessa compatibilidade.

PORTING.md: exige ELF PSP puro (7f454c46), analisador/gerador, endereço base e entrada obtidos do executável, e módulos realmente usados. Os exemplos e constantes HST não são configuração do Shrek. O esquema atual usa manifesto validado por tools/title_manifest.py e planner title_codegen_plan.py; schema permite declarar módulos, roots e políticas. Não incluir caminhos locais nem hashes privados no manifesto público. A documentação adverte que o pipeline genérico não comprova portabilidade nem correção de runtime. Import desconhecido deve falhar visivelmente. Regressões sintéticas não provam comportamento do jogo. `make verify` completo requer oráculos externos e reporta NOT_RUN quando ausentes.

Ben10: src/rt/switch/ge_dk.c implementa backend deko3d; ge_async.c, fila GE; audio_switch.c, áudio; sdl_shim, adaptação SDL; posix_shim.c, chamadas de FS; prof_switch.c, perfil; switch_main.c, bootstrap. Makefile.switch compila shaders com uam, constrói AArch64 com devkitA64/libnx, deko3d e exporta ELF/NACP/NRO. Fontes HLE/ATRAC/H264 e núcleo estão em src/rt e src/core; VFPU em assets/vfpu. São candidatos a reutilização sujeitos a análise semântica e licenças, não validados para Shrek.

Particularidades NÃO transplantáveis: Makefile.switch define TITLE experimental-ulus10307, ENTRY 0x088994d4, nome e target Ben10; switch_main.c fixa diretório sdmc:/switch/ben10-psp e base 0x08804000. Código e configuração de instalação precisam ser parametrizados com dados verificados do Shrek; não herdar valores. A inicialização define resolução/cap e outras opções que também requerem avaliação. A lista de fontes, dispatcher, runtime e todos os caminhos de fallback devem ser auditados para comprovar ausência de interpretação MIPS no produto final, já que o upstream contém guest_interp.c e testes de interpretador. Sua mera presença no repositório não prova uso em execução.

O repositório Ben10 declara GPL-3.0-or-later; preservar LICENSE, NOTICE.md, CREDITS.md, THIRD_PARTY_LICENSES e proveniência por arquivo ao reutilizar. O README afirma que o projeto foi testado em console apenas parcialmente; não extrapolar para Shrek.

Próximos passos: validar sintéticos públicos, identificar e obter ELF plano a partir da entrada local; confrontar esquema na revisão fixada, gerar plano só após determinar base e entry; auditar acoplamentos específicos e caminhos de interpretação; instrumentar cobertura, sem prometer funcionalidade antes dos testes.
