# Questões em aberto

- Um executável Linux exploratório exibiu conteúdo do jogo offscreen; a fidelidade visual e o menu não foram validados. Existe NRO experimental com configurações Ben10 e componentes de interpretação; não é instalável como port e não há build final sem interpretação.
- Base de carregamento e tratamento de relocação do BOOT.BIN ainda requerem validação antes de fixar o manifesto.
- O manifesto Shrek ainda não existe: a base e o contrato do runtime não foram validados. A igualdade EBOOT decriptado/BOOT confirma os bytes, não o comportamento de execução.
- Compatibilidade entre o gerador upstream e o runtime Switch do Ben 10 não foi validada.
- O código upstream contém componentes de interpretação; auditar o caminho final de execução para excluir interpretação e JIT.
- As unidades geradas contêm chamadas a `sr_vfpu_interp`. Verificar caminhos alcançados e implementar tradução AOT apropriada antes de considerar atendida a restrição de interpretação.
- Um stream ATRAC3+ encontrado após a abertura foi recusado pelo decoder: modo de amplitude GHA 0 não implementado. Ainda não está demonstrado se essa falha causa a pausa observada na apresentação.
- Testes no hardware Switch, renderização, áudio, persistência e desempenho ainda não foram realizados.
