# De-Para Octadesk para a Migração Movidesk - v 2.0

Este programa consiste em consumir dados da API Octadesk e alimentar uma planilha para criação de um De-Para de campos que serão utilizados na migração entre API Octadesk e Movidesk.


## Uso

* Baixar os arquivos [aqui](https://github.com/jhohannessf/service_movidesk)
* Baixe os arquivos individualmente, clicando no nome do arquivo, após abrir procure uma opção no lado direito superior, chamada "Download raw file".
* Você vai precisar de uma ferramenta IDE para edição e execução do código 
* Pode ser o PyCharm ou VS Code. Ambas precisarão de chamado no Jira para a instalação.
    * Baixar o Pycharm [aqui](https://www.jetbrains.com/pt-br/pycharm/download/?section=windows)
      * Como instalar e configurar o Pycharm [aqui](https://www.youtube.com/watch?v=EDQGZEsNARg)
    * Baixe o VS Code [aqui](https://code.visualstudio.com/download)
      * Como instalar e configurar o VS Code [aqui](https://www.youtube.com/watch?v=Zy3iaMZbPO8)
* Com a ferramenta instalada e configurada, você precisará abrir o projeto que baixou
  * No PyCharm, canto superior esquerdo, aperta Alt + \ > File > Open
    * Após abrir o projeto, você precisará importar todos os pacotes e bibliotecas que estão sendo utilizadas
      * Abra o terminal (Alt + F12), escreva pip install -r requirements.txt e aperte `enter` 
        * Aguarde finalizar a instalação por completa
  * No VS Code, canto superior esquerdo > File > Open File ou aperta Ctrl + O 
    * Após abrir o projeto, você precisará importar todos os pacotes e bibliotecas que estão sendo utilizadas
      * Para ler e utilizar o arquivo requirements.txt no VS Code, abra o terminal integrado (Ctrl + ' ou Terminal > Novo Terminal) e execute o comando pip install -r requirements.txt. Isso instalará automaticamente todas as bibliotecas listadas no ambiente virtual ativo.
  * Preencha os dados do cliente dentro do arquivo `.env`. Apenas o token da API Movidesk.
  * Preencha a planilha `sheets-service.xlsx`, que está localizada dentro da pasta /data. Não altere as colunas da planilha, respeite os critérios de preenchimento.
    * Em caso de dúvidas, consulte a  API de Serviços do Movidesk [aqui](https://atendimento.movidesk.com/kb/pt-br/article/7440/api-servicos?ticketId=&q=)
  * Por fim, execute o arquivo `service.py`
    * Para executar no PyCharm, basta clicar com botão direito do mouse no arquivo.py e clicar em `run + nome do arquivo` . No caso, `run + service`
    * Para executar no VS Code, instale a extensão Python, abra o arquivo .py, clique no botão "Play" no canto superior direito para executar no terminal integrado ou use o terminal (Ctrl+` e python seu_arquivo.py), sendo o botão Play o mais direto para rodar o script inteiro ou seleções. 
