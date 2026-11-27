# Cobertura — fase 3

Na execução de referência PPSSPP v1.20.4, o módulo carregou em 0x08804000, com entry 0x08804678 e GP 0x08a6ea80. O log privado está em `original/private/ppsspp-v1.20.4-shrek-debug.log` e a análise em `original/private/base-phase3.md`. Isso demonstra concordância nesta configuração do PPSSPP, não observação de hardware nem equivalência completa dos estados. SP e RA iniciais não foram capturados.

As 870 arestas do CFG são transferências de destino calculado; não há observações dinâmicas do port ainda. A classificação das palavras não atribuídas e os limites de cobertura permanecem em COVERAGE_PHASE2.md. As fontes geradas incluem chamadas para `sr_vfpu_interp`; contagem textual não prova que cada chamada seja executada. O caminho final precisa ser auditado e cumprir o requisito AOT.
