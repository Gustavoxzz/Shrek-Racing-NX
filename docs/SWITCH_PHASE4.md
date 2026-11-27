# Ensaio Switch — fase 4

Ver COMPATIBILITY_MATRIX.md para revisões, comandos e diferenças. Em cópia isolada, o gerador Nakagawa da base Ben10 `70b1d3f8` produziu código do Shrek e o runtime Ben10 compilou e ligou ELF AArch64, NACP, mapa e NRO com retorno zero. Saídas privadas em `build/switch-phase4-experiment/`.

O artefato preserva caminhos, configuração e iconografia do Ben10 e liga símbolos de interpretação MIPS/VFPU. Não é strict-AOT, não está pronto para instalação ou distribuição e não foi testado no console. O link prova compatibilidade suficiente para construir este experimento, não que o jogo inicialize. Corrigir acoplamentos, compatibilidade semântica e fallback antes do pacote de teste.
