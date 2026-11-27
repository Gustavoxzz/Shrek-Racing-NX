# Questões em aberto

- As unidades geradas foram compiladas isoladamente em objetos, mas não foram ligadas ou executadas; nenhum NRO do jogo existe.
- Base de carregamento e tratamento de relocação do BOOT.BIN ainda requerem validação antes de fixar o manifesto.
- O manifesto Shrek ainda não existe: a base e o contrato do runtime não foram validados. A igualdade EBOOT decriptado/BOOT confirma os bytes, não o comportamento de execução.
- Compatibilidade entre o gerador upstream e o runtime Switch do Ben 10 não foi validada.
- O código upstream contém componentes de interpretação; auditar o caminho final de execução para excluir interpretação e JIT.
- Testes no hardware Switch, renderização, áudio, persistência e desempenho ainda não foram realizados.
