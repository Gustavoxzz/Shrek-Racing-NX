# Investigação ATRAC — fase 5

O runtime Nakagawa recusou um pacote de 1120 bytes cujo endereço guest estava alinhado a 16 bytes. A sequência completa não foi encontrada literalmente na ISO; ela pode ter sido transformada pelo carregador do jogo, e a ausência não demonstra corrupção. Os bytes, hash, metadados e relatórios de captura permanecem privados.

Busca adicional local encontrou uma ocorrência do prefixo de 64 bytes na ISO. Comparado aos 1120 bytes contíguos a partir dessa ocorrência, o pacote capturado coincide nos primeiros 456 bytes e diverge a partir daí. Isso sugere investigar montagem descontínua ou transformação dos dados; não demonstra, por si só, corrupção nem a identidade do frame esperado pelo PPSSPP. Offset e hashes estão no relatório privado.

O mesmo decoder, em instância estéreo nova e sob as mesmas condições do ensaio offline, aceitou o bloco contíguo candidato da ISO: retorno 1120 e 2048 amostras; a captura recusada produziu zero amostras. É evidência diferencial para investigar montagem/streaming. Não confirma que o candidato seja o frame recebido pelo PPSSPP ou que a substituição direta seja semanticamente correta; nenhuma substituição foi aplicada.

O sufixo de 664 bytes da captura também foi encontrado literalmente em outra região anterior do mesmo PACKFILE. Os dois fragmentos encontrados cabem no intervalo da leitura de 32768 bytes registrada pouco antes da falha. Isso permite rastrear cópia e possível wrap de buffer, mas ainda não determina que camada combinou as regiões ou se uma montagem descontínua seria esperada. Offsets precisos e métodos estão na evidência privada.

Em ensaio offline com uma instância estéreo nova do decoder Nakagawa, o pacote reproduziu a recusa de GHA amplitude mode 0. A posição do bitreader imediatamente após ler o bit de modo era 8912 de 8960 bits. Com configuração mono, o ensaio falhou antes; não se conclui qual configuração foi usada pelo PPSSPP. A reprodução isolada confirma o comportamento desse decoder com esses bytes, não a integridade do pacote ou sua equivalência ao recebido pelo PPSSPP.

Na inspeção estática da cópia PPSSPP, falha no decoder faz a camada ATRAC retornar `SCE_ERROR_ATRAC_ALL_DATA_DECODED`, informar zero amostras e fim, sem avançar amostra nem consumir frame naquela rota. O Nakagawa retorna `ATRAC_ERROR_UNKNOWN_FORMAT`, zero amostras, fim e remaining zero. São diferenças de implementação, não medição do PSP. Ainda não existe captura do pacote correspondente no PPSSPP, nem teste comparativo dos estados após erro. Não modificar o retorno ou implementar decoder baseado apenas nessa diferença.

O utilitário `tools/compare_packets.py <captura-a> <captura-b> --offset-a <n> --offset-b <n>` compara arquivos locais limitados a 1 MiB e relata tamanhos, hashes, alinhamento e primeira diferença sem imprimir bytes. Resultados e capturas são privados e não devem ser versionados. Testes sintéticos em `tests/test_compare_packets.py` cobrem igualdade, diferenças, tamanho e limites.
