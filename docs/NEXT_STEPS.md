# Próximos passos

Fase 5: concluir captura local ATRAC dos dois runtimes e comparar pacote, offset, bitreader e estado após erro; não alterar retorno até evidência. Verificar resultado do ensaio offscreen com pulsos de Start, sem inferir menu a partir do tempo. Integrar apenas adaptações Switch auditadas e testes pertinentes, mantendo diagnósticos distintos de strict-AOT.

O candidato contíguo da ISO compartilha 456 bytes iniciais com a captura e decodifica em ensaio offline; a captura falha. Rastrear onde o segundo trecho do buffer guest é montado e comparar com captura real do PPSSPP antes de aplicar qualquer correção ou substituir dados.

Fase 4: comparar captura e temporização com PPSSPP; investigar stalls e encerramento de vídeo com logs de scheduler e MPEG; alcançar e testar menu com áudio real. Concluir verificação do executável Windows e suíte nativa. Aplicar e testar o protótipo VFPU apenas após comparação diferencial, incluindo exceções e delay slots; auditar o dispatcher e criar um modo strict-AOT. Adaptar inicialização e caminhos do experimento Switch antes de pedir teste em hardware.

Fase 3: investigar a execução após abertura do vídeo, comparar estado e fluxo com PPSSPP e capturar destinos indiretos alcançados. A mensagem inicial de spin teve atividade posterior e não é bloqueio confirmado. Validar contrato de título e remover dependências de interpretação para o produto final. Repetir teste de vídeo com espaço suficiente. Comparar SP/RA iniciais com PPSSPP; integrar runtime Switch após compatibilidade de APIs e VFPU AOT. Adicionar símbolos de depuração completos e verificar mapa de linkagem.

Fase 2: concluir a suíte nativa no filesystem Linux e registrar status real; validar o modelo de carga com referência dinâmica; configurar manifesto sem apresentar hipótese como fato; ligar os objetos ao runtime e identificar o primeiro bloqueio observado. Preservar os relatórios de CFG e a saída anterior. Os exemplos ARM64 e deko3d compilaram, mas ainda requerem teste físico.

1. Concluir testes públicos, documentar versões e resultados.
2. Determinar base, relocação, imports e entrada do ELF PSP a partir de evidências; verificar módulos e requisitos.
3. Preparar manifesto compatível com a revisão escolhida sem adivinhar valores, validar esquema e plano.
4. Executar codegen apenas quando os pré-requisitos e testes sintéticos estiverem validados; registrar cobertura e falhas.
5. Adaptar e testar runtime e backend em etapas, preservando licenças e proibindo interpretação no produto final.
