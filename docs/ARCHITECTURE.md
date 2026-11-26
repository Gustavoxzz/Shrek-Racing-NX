# Arquitetura e decisões provisórias

O executável PSP deve ser analisado e traduzido antecipadamente para C e compilado para ARM64, com endereços guest de 32 bits, memória e dispatcher explícitos. O runtime Switch e backend deko3d de Ben 10 NX são candidatos à reutilização; requerem adaptação e auditoria. A base Nakagawa usada pelo Ben 10 e o upstream atual divergiram substancialmente, portanto a compatibilidade de código gerado não está demonstrada. Começar pelo par Ben 10/base correspondente ou validar explicitamente o contrato antes de misturar versões. Auditar todas as rotas para garantir ausência de interpretação MIPS e JIT no produto final.

Não herdar constantes de boot, caminhos, patches, endereços ou comportamento específicos do Ben 10. Imports desconhecidos devem falhar visivelmente, sem sucesso fictício. O jogo deve usar seus próprios arquivos locais, sem distribuição de dados proprietários.
