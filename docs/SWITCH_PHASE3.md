# Fase 3 — compilação ARM64 e compatibilidade de runtime

Imagem e toolchain fixados conforme `work/switch-phase2.md`; Nakagawa upstream `adba2471bb9963f24533b7422a5e9119bd4c7116`. Código privado gerado está em `work/game-private` e objetos em `work/phase3-switch`; não distribuí-los.

A linha de compilação reproduz, em essência, flags de código gerado de `ben10-reference/Makefile.switch`: `-march=armv8-a+crc+crypto -mtune=cortex-a57 -mtp=soft -fPIE -ffunction-sections -D__SWITCH__ -fno-strict-aliasing -ffp-contract=off -DSR_FLIGHT_RECORDER_LINKED`, com `-O0` para diagnóstico, forced include `src/rt/switch/nk_switch_compat.h` do Ben10, e cabeçalhos de runtime upstream atual. Comandos completos em `work/phase3-switch/compile.sh`; resultado por chunk em `status-real.txt`; logs por chunk na mesma pasta.

A unidade de registro `shrek.c` compilou para objeto com headers upstream atual. A compilação sequencial dos sete chunks terminou com retorno zero. Isso prova somente compilação de unidades individuais, não link, execução, correção semântica nem desempenho.

Compatibilidade direta com runtime Ben10 testada sem alterações: compilação de `shrek.c` falhou porque `SrVfpuUse` e `sr_vfpu_report_unverified_uses` não existem no header Ben10; ver `ben10-compile.log`. Teste sintático de `shrek_0.c` com header Ben10 falhou por ausência de `sr_fpu_sqrt_s` e `SR_VFPU_ACCESS_REFUSED`; ver `ben10-chunk.log`. Ambos `recomp.h` declaram `SR_CPUSTATE_ABI_VERSION` 3, e os campos de `CpuState` inspecionados são idênticos; este indício de layout comum não demonstra compatibilidade de API ou comportamento. Atualizar/adaptar o runtime ou gerar novamente com revisão compatível requer testar sem mascarar erros.

Restrição arquitetural: contagem textual de 5.670 ocorrências de `sr_vfpu_interp(` no código gerado. Muitas são caminhos alternativos condicionais de acesso à memória, logo a contagem não mede chamadas realizadas. Mesmo assim sua inclusão no runtime final deve ser tratada: usuário proibiu interpretação; substituição requer implementação AOT e testes de equivalência, não ocultação nem link automático. A presença desses caminhos não demonstra que execução real os alcançaria.

Nota de auditoria: uma primeira tentativa de script de compilação sofreu expansão indevida de variáveis pelo PowerShell; `status.txt` e `chunk_.log` são inválidos e não constituem resultados. O script corrigido preserva as variáveis e escreve `status-real.txt`.

Conclusão: as sete unidades `shrek_0.c` a `shrek_6.c` e o registrador `shrek.c` compilaram separadamente com retorno 0, usando headers upstream e flags acima, sem linkar runtime. `readelf -h shrek_0.o` mostrou ELF64/AArch64; `nm -u shrek_0.o` confirma símbolo indefinido `sr_vfpu_interp`, portanto a dependência existe no objeto e não só no texto. Resultados e objetos estão sob `build/phase3-switch/`, ignorado no Git e privado. Nenhum ELF ou NRO de jogo foi gerado.
