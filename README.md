# Projeto-Integrador-I
O projeto integrado I consiste em desenvolver um sistema de votação digital fictício, concebido com finalidade estritamente didática. Seu principal objetivo é promover a integração prática de conhecimentos das áreas de Lógica de programação em python, manipulação de bancos de dados com SQL e aplicação de conceitos matemáticos (como Álgebra Linear) voltados à proteção da informação

O sistema é executado exclusivamente via terminal (sem interface gráfica) e é estruturado em dois módulos principais, cada um com submódulos específicos:
  * **Gerenciamento**: responsável pela administração dos dados da eleição. Permite cadastrar, editar, remover, buscar e listar eleitores e candidatos. Durante o cadastro, o sistema valida matematicamente o CPF e o título de eleitor, impede duplicidade de dados e gera automaticamente uma chave de acesso exclusiva para cada eleitor. Informações sensíveis como CPF e chave de acesso são protegidas pela Cifra de Hill antes de serem armazenadas no banco de dados.
  * **Votação**:  composto por quatro submódulos:
    * Abertura da Urna: autenticação do mesário, seguida da zerézima — procedimento que zera os votos e exibe publicamente que todos os candidatos partem com zero votos, garantindo transparência.
    * Votação: identificação do eleitor por título, CPF e chave de acesso, registro do voto com geração de protocolo criptografado e atualização do status do eleitor.
    * Encerramento: finalização oficial da votação pelo mesário, com dupla confirmação de segurança, seguida da apuração dos resultados, estatísticas de comparecimento e validação de integridade da urna.
    * Auditoria: exibição do histórico de logs de ocorrências e dos protocolos de votação gerados, permitindo rastreabilidade completa do processo eleitoral.
    * Resultado: exibição do boletim de urna, da estatística de comparecimento e de votos por partidos e a validação de integridade da votação
  


## Execução do sistema
O sistema é executado exclusivamente via terminal (linha de comando), sem interface gráfica. Para executa-lo é necessário configurar o ambiente corretamente, para isso basta seguir as seguintes etapas:
  1. Fazer o download do repositório, utilizando o comando de clonagem ou baixando os arquivos manualmente.
  2. Garantir que python 3 está instalado
  3. Fazer a instalação da biblioteca responsável por conectar com o mySQL, para isso basta digitar o seguinte comando no terminal: `pip install mysql-connector-python`
  4. Criar o banco de dados, para isso é preciso executar os scrips fornecidos no projeto, responsáveis pela criação das tabelas necessárias, em algum ambiente de mySQL, como o workbench
  5. Executar o arquivo **main** do projeto
## Tecnologias usadas
  * Python 3.x
  * MySQL
  * Bibliotecas do python: mysql.connector, datetime, random 
  * Git e GitHub    
## Integrantes
  * Felipe Birolli Laiko
  * Luis Gustavo Fortunato Filho
  * Matheus Augusto Papa Batista
  * Nicholas de Castro Lopes
  * Rafael Salazar Ahumada Comitre
