# Ensaio isolado Switch — fase 5

Em `/var/tmp/shrek-nx-toolchain/bundle/rootfs/tmp/shrek-phase5-switch`, cópia separada de `shrek-phase4`, adaptei `switch_main.c`, `gui_switch.c`, `ge_dk.c` e `Makefile.switch`. Diff reproduzível em `work/phase5-switch.patch`, sobre a cópia Ben10 exata usada no ensaio anterior; o patch não contém dados do jogo. Dados gerados, ELF e NRO são privados.

O bootstrap usa `sdmc:/switch/shrek-racing-nx`, imagem `shrek_image.bin`, base 0x08804000, entrada 0x08804678 e boot path `disc0:/PSP_GAME/SYSDIR/EBOOT.BIN`. Metadados são diagnósticos Shrek, iconografia Ben10 foi removida; escala inicial 1x e boost é opt-in via `boost.txt`. Parte genérica herdada não foi integralmente auditada. O ISO é esperado em `game.iso`; fonte não foi modificada.

O bootstrap também escreve no log marcadores iniciais com título, base e entrada, verifica disponibilidade de ISO e imagem antes de chamar o runtime, faz flush e registra retorno. São verificações superficiais de acesso, não validação da identidade da ISO nem teste físico. A versão com logging foi compilada e linkada novamente com exit 0; patch atualizado inclui essas mudanças.

Comando, como root no Ubuntu de desenvolvimento:

```sh
chroot /var/tmp/shrek-nx-toolchain/bundle/rootfs /usr/bin/env DEVKITPRO=/opt/devkitpro DEVKITA64=/opt/devkitpro/devkitA64 PATH=/opt/devkitpro/tools/bin:/usr/bin:/bin make -C /tmp/shrek-phase5-switch/ben10 -f Makefile.switch -j2 PACKAGE_DIR=/tmp/shrek-phase5-switch/generated OPT_RT=-O0 OPT_GEN=-O0
```

Incremental terminou exit 0 e gerou ELF, NACP, mapa e NRO. `readelf` confirma ELF64 AArch64. `nm` confirma `sr_guest_interp_run`, `sr_guest_interp_run_internal`, `sr_guest_interp_run_with_boundary`, `sr_vfpu_interp`. Não é strict-AOT; não se testou em hardware ou se todos os serviços e caminhos funcionam. Nenhuma recomendação de instalação. A imagem guest e assets necessários não foram empacotados; configuração real de saves, segurança de lifecycle e compatibilidade do runtime continuam por validar.
