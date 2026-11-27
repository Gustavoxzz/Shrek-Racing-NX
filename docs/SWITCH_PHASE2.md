# Fase 2 — toolchain Switch (27/11/2026)

A instalação oficial Debian documentada em https://github.com/devkitPro/pacman/releases/tag/v6.0.2 usa https://apt.devkitpro.org/install-devkitpro-pacman. A solicitação ao script foi recusada com HTTP 403 Cloudflare; o script não foi executado. Não foi feito shutdown/reboot do WSL.

Alternativa oficial: imagem Docker Hub `devkitpro/devkita64` digest `sha256:1fc388c3a0d34bd2045a6dadcb1020e069d5f876a187fd705de14b4440c00282` (inspecionada e copiada por digest), extraída com `skopeo` e `umoci` instalados dos repositórios Ubuntu. Os arquivos da imagem e rootfs estão na distribuição WSL em `/var/tmp/shrek-nx-toolchain/`; são ambiente de trabalho, não estão versionados nem devem ser considerados distribuição. A imagem oficial inclui compilador, bibliotecas, ferramentas de shader e exemplos.

Comandos executados no Ubuntu WSL2 como root:

```sh
apt-get install -y --no-install-recommends skopeo umoci
mkdir -p /var/tmp/shrek-nx-toolchain
skopeo copy docker://docker.io/devkitpro/devkita64@sha256:1fc388c3a0d34bd2045a6dadcb1020e069d5f876a187fd705de14b4440c00282 oci:/var/tmp/shrek-nx-toolchain/image:latest
umoci unpack --image /var/tmp/shrek-nx-toolchain/image:latest /var/tmp/shrek-nx-toolchain/bundle
chroot /var/tmp/shrek-nx-toolchain/bundle/rootfs /usr/bin/env DEVKITPRO=/opt/devkitpro DEVKITA64=/opt/devkitpro/devkitA64 PATH=/opt/devkitpro/tools/bin:/usr/bin:/bin make -C /opt/devkitpro/examples/switch/templates/application
chroot /var/tmp/shrek-nx-toolchain/bundle/rootfs /usr/bin/env DEVKITPRO=/opt/devkitpro DEVKITA64=/opt/devkitpro/devkitA64 PATH=/opt/devkitpro/tools/bin:/usr/bin:/bin make -C /opt/devkitpro/examples/switch/graphics/deko3d/deko_basic
```

Ambos make concluíram com código 0. `application` produziu ELF, NACP e NRO; `deko_basic` compilou shaders vertex e fragment em `.dksh`, empacotou RomFS e produziu ELF, NACP e NRO. `aarch64-none-elf-readelf -h` confirmou os dois ELFs como ELF64, Machine AArch64. Nenhum exemplo foi executado no Switch e isso não demonstra a compilação ou funcionamento do jogo.

Pacotes na imagem: devkitA64 GCC 15.2.0-7, binutils 2.45.1-2, newlib 4.6.0.20260123-4, libnx 4.12.0-1, deko3d 0.5.0-1, switch-tools 1.13.1-1, switch-examples 20260201-1. Imagem e pacotes são fixados pelo digest acima; atualizar exige revalidação. O upstream https://github.com/switchbrew/switch-examples também foi clonado em `work/switch-examples`, mas os exemplos compilados vieram da imagem oficial, não desse clone.

Limitações: o rootfs extraído exige acesso root e não está integrado ao Makefile do projeto; nada foi modificado no código principal. A integração do runtime e dos shaders do Ben 10 NX com Shrek continua por fazer. Executar no hardware e conferir vídeo/entrada exige Switch e confirmação do usuário.
