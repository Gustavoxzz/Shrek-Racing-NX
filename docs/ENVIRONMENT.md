# Diagnóstico do ambiente — 2026-11-26

Windows NT build 26300; WSL2 disponível, distribuição Ubuntu 26.04.1 LTS, kernel 6.18.58.1 x86_64. Git no Windows disponível; os aliases Windows python/python3 apontavam à Microsoft Store e não foram considerados interpretadores funcionais. WSL Git 2.53.0 e Python 3.14.4.

O usuário WSL requer senha para sudo, porém `wsl -d Ubuntu -u root -- id` funcionou. Instalação efetuada com sucesso (código 0), a partir dos repositórios Ubuntu configurados:

```
wsl -d Ubuntu -u root -- apt-get update
wsl -d Ubuntu -u root -- env DEBIAN_FRONTEND=noninteractive apt-get install -y build-essential cmake ninja-build pkg-config python3-venv libsdl2-dev libgl1-mesa-dev
```

Verificação subsequente: GCC 15.2.0, GNU Make 4.4.1, CMake 4.2.3, Ninja 1.13.2, SDL 2.32.10, OpenGL pkg-config 1.2. Essas ferramentas básicas não constituem evidência de testes Nakagawa aprovados; é necessário compilar e executar testes da revisão selecionada.

Foram adicionados `python-is-python3`, SDL3 3.4.2, SDL3_ttf 3.2.2 e bibliotecas Vulkan do Ubuntu para testes. SDL3 3.4.2 difere da versão 3.4.20 recomendada pela documentação do upstream. A primeira execução dos testes nativos falhou na ligação por falta de SDL3 e Vulkan; uma nova execução foi iniciada após instalá-los.

Inicialmente não encontrados no PATH Windows: CMake, Ninja, GCC, Clang, Java, make, pacman, devkitA64, dksh ou Ghidra. No WSL, Java e devkitPro ainda não verificados/instalados; /opt/devkitpro ausente no diagnóstico inicial e DEVKITPRO/DEVKITA64 vazios. Os toolchains e bibliotecas Switch, bem como shaders e Ghidra, permanecem por configurar e validar.
