# Próximos passos

Fase 2: concluir a suíte nativa no filesystem Linux e registrar status real; validar o modelo de carga com referência dinâmica; configurar manifesto sem apresentar hipótese como fato; ligar os objetos ao runtime e identificar o primeiro bloqueio observado. Preservar os relatórios de CFG e a saída anterior. Os exemplos ARM64 e deko3d compilaram, mas ainda requerem teste físico.

1. Concluir testes públicos, documentar versões e resultados.
2. Determinar base, relocação, imports e entrada do ELF PSP a partir de evidências; verificar módulos e requisitos.
3. Preparar manifesto compatível com a revisão escolhida sem adivinhar valores, validar esquema e plano.
4. Executar codegen apenas quando os pré-requisitos e testes sintéticos estiverem validados; registrar cobertura e falhas.
5. Adaptar e testar runtime e backend em etapas, preservando licenças e proibindo interpretação no produto final.
