# Projeto-FCCPD
Trabalho da segunda unidade da cadeira de FCCPD

## Desafio 1: Containeres em Rede
Esse desafio implementa dois containers Docker que se comunicam através de uma rede bridge customizada, garantindo o isolamento da comunicação. Foi usado o Docker Compose para fazer a criação da rede e dos serviços simultaneamente.

### INSTRUÇÕES DE EXECUÇÃO

Pré requisito: Docker e Docker Compose instalados.

1. Navegue até o diretório do desafio ( `cd desafio1` )
2. Abra um novo terminal e digite `docker compose up` para iniciar o modo interativo e visualizar os logs em tempo real.

Após isso, você verá os logs intercalados. O cliente mostrará a requisição e o servidor vai responder na porta 8080.

Para encerrar a execução, use Cntrl+C

### ARQUITETURA

Rede: Uma rede do tipo bridge chamada 'rede-desafio1' foi criada pra conectar exclusivamente esses dois containeres.

Container 1 (servidor): Usa a imagem nginx:alpine. Foi configurado via arquivo nginx.conf personalizado para escutar na porta 8080 e retornar uma mensagem de texto simples confirmando o recebimento da requisição.

Container 2 (cliente): Usa a imagem alpine/curl. Executa um script em shell que entra em loop infinito, realizando uma requisição HTTP para o container servidor a cada 5 segundos.

### DECISÕES TÉCNICAS

Docker Compose: usei o compose pra definitir a infraestrutura como código, facilitando a execução e garantindo que a rede seja sempre criada automaticamente junto com os containeres. Além disso, o docker compose foi utilizado em sala de aula, então optei por familiaridade.

Nomes de serviço como DNS: Dentro da rede do docker, os containeres resolvem os nomes dos serviços, por isso o cliente consegue acessar o servidor apenas chamando http://web-server:8080, sem precisar saber o IP.

Imagem Alpine: foi usado versões baseadas em alpine linux para manter as imagens leves e o download mais rápido.
