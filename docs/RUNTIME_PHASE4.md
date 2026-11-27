# Runtime e ambiente — fase 4

O checkout Nakagawa fixado foi compilado no Windows com MSYS2 UCRT64 isolado, GCC 16.2.0, Python 3.14.10, SDL3 3.4.20 e Vulkan loader 1.4.363. A segunda tentativa, com `POWERSHELL=pwsh`, concluiu o alvo `all` com código 0, incluindo staging. A primeira linkou mas falhou no staging porque o PowerShell invocado não encontrou `Get-FileHash`. PE x86-64 tem `.debug_info` e `.debug_line`, mapa e símbolos; gerados usam `-g1`, runtime majoritariamente `-g`, mas regra GE usa `-O2` sem `-g`. A depuração não é completa. O binário contém interpretação VFPU e não é produto final. Objetos, imagem guest e executável ficam em `build/windows-phase4/` ignorado pelo Git.

Reprodução do build, no checkout isolado preparado e com UCRT64 temporariamente no PATH:

```powershell
mingw32-make -j2 CC=gcc PYTHON=python GAME_NAME=shrek GAME_ELF=<BOOT.BIN-privado> GAME_BASE=0x08804000 GAME_ENTRY=0x08804678 BUILD_DIR=build/shrek-win4 "RECOMP_OPT=-O0 -g1" "RUNTIME_OPT=-O0 -g" LINK_MAP=build/shrek-win4/shrek.map POWERSHELL=pwsh all
```

O primeiro smoke Windows falhou com status 0xC0000409 e log de LUT VFPU ausente no diretório de trabalho. Repetido no checkout upstream com `assets/vfpu` disponível, ISO local, imagem privada, `--sched`, áudio dummy e `SR_EXIT_AT_VBLANK=120`, terminou com código 0. Registrou 13221 funções, leituras e `display_flip` em VBlank 95. `EXEC_SHARE` relata zero entradas no interpretador de CPU na amostra; não cobre VFPU nem prova strict-AOT. Não houve janela interativa, validação visual Windows ou áudio real. Comando completo e logs privados em `logs/phase4-env.md` e `logs/phase4-smoke-retry-stderr.log`.

Espaço: C: tinha aproximadamente 118 GiB disponíveis; `/` WSL relatou 951 GiB e 67 milhões de inodes livres, ao passo que `/tmp` é tmpfs de 1,9 GiB. O teste de vídeo exigia 4096 MiB livres; executado em `/var/tmp`, `videorec_selftest` passou inclusive FFV1 e mux. O alvo `psmf-media-focused-selftest` e a suíte `native-core-tests` terminaram com código 0 em checkout Linux com `TMPDIR` no filesystem Linux; alguns casos foram ignorados por serem específicos de Windows ou indisponíveis no host. Logs privados em `logs/focused-phase4.log` e `logs/native-phase4.log`.

Para smoke controlado WSL: `tools/smoke-wsl.ps1 -Iso <ISO> -ExitVblank 300 -TimeoutSeconds 20`. O script usa o limite oficial por VBlank, guarda logs privados e relata apenas marcadores com evidência. Em teste retornou código 0. Um timeout externo permanece como proteção caso o encerramento não ocorra.
