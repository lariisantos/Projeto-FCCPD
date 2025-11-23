# Projeto-FCCPD
Trabalho da segunda unidade da cadeira de FCCPD

# Desafio 1: Containeres em Rede
Esse desafio implementa dois containers Docker que se comunicam através de uma rede bridge customizada, garantindo o isolamento da comunicação. Foi usado o Docker Compose para fazer a criação da rede e dos serviços simultaneamente.

### INSTRUÇÕES DE EXECUÇÃO

**Pré requisitos**: Docker e Docker Compose instalados.

1. Navegue até o diretório do desafio ( `cd desafio1` )
2. Abra um novo terminal e digite `docker compose up` para iniciar o modo interativo e visualizar os logs em tempo real.

Após isso, você verá os logs intercalados. O cliente mostrará a requisição e o servidor vai responder na porta 8080.

Para encerrar a execução, use Cntrl+C

---

### ARQUITETURA

Rede: Uma rede do tipo bridge chamada 'rede-desafio1' foi criada pra conectar exclusivamente esses dois containeres.

Container 1 (servidor): Usa a imagem nginx:alpine. Foi configurado via arquivo nginx.conf personalizado para escutar na porta 8080 e retornar uma mensagem de texto simples confirmando o recebimento da requisição.

Container 2 (cliente): Usa a imagem alpine/curl. Executa um script em shell que entra em loop infinito, realizando uma requisição HTTP para o container servidor a cada 5 segundos.

---

### DECISÕES TÉCNICAS

Docker Compose: usei o compose pra definitir a infraestrutura como código, facilitando a execução e garantindo que a rede seja sempre criada automaticamente junto com os containeres. Além disso, o docker compose foi utilizado em sala de aula, então optei por familiaridade.

Nomes de serviço como DNS: Dentro da rede do docker, os containeres resolvem os nomes dos serviços, por isso o cliente consegue acessar o servidor apenas chamando http://web-server:8080, sem precisar saber o IP.

Imagem Alpine: foi usado versões baseadas em alpine linux para manter as imagens leves e o download mais rápido.

---

# Desafio 2: Documentação de Volumes e Persistência de Dados

Esse desafio documenta a implementação e comprovação da **persistência de dados** para um banco de dados PostgreSQL utilizando **volumes nomeados** do Docker. O projeto também incluiu o uso de um container secundário para acessar os dados através da rede Docker, simulando um ambiente de aplicação (desafio opcional). O objetivo é comprovar que os dados sobrevivem mesmo após a remoção e recriação do container.

### INSTRUÇÕES DE EXECUÇÃO

**Pré-requisitos**: Docker e Docker Compose instalados.

1.  Navegue até o diretório do desafio ( `cd desafio2` )
2.  Inicie os containers com o compose:
    ```bash
    docker-compose up -d
    ```
3.  **Criação dos Dados:** Acesse o container do banco e insira os dados de teste
    > **Nota sobre o Comando:** Em vez de executar o `psql` diretamente, foi acessado o *shell* (`sh`) do container primeiro.
    ```bash
    docker exec -it desafio2-db sh
    /# psql -U admin -d desafio2
    ```
    <img width="949" height="537" alt="image" src="https://github.com/user-attachments/assets/52904152-ef8f-41e8-8b2a-c005b4600176" />

4.  **Teste de Persistência:** Para provar que o volume funciona, saia do banco com `exit` e após isso derrube os containeres e tente acessar os dados:
    ```bash
    docker compose down
    docker-compose up -d
    docker exec -it desafio2-db psql -U admin -d desafio2 -c "SELECT * FROM usuarios;"
    ```
    <img width="1401" height="508" alt="image" src="https://github.com/user-attachments/assets/c48b6d5c-0cfc-47fa-997c-d84f121fe75d" />

5.  **Container Leitor Opcional:** Acesse os dados persistidos usando o segundo container através da rede:
    ```bash
    docker exec -it desafio2-leitor sh -c "PGPASSWORD=admin psql -h desafio2-db -U admin -d desafio2 -c 'SELECT * FROM usuarios;'"
    ```
    <img width="1387" height="208" alt="image" src="https://github.com/user-attachments/assets/ec500beb-733e-44f6-9e33-11c719b1663e" />


Para encerrar a execução e remover containers/rede (mantendo o volume!): `docker-compose down`

---

### ARQUITETURA

Rede: Uma rede do tipo bridge chamada **'rede-desafio2'** foi criada para conectar os dois containers.

Volume: Um **Volume Nomeado** chamado **'dados-db-desafio2'** é usado para persistir os dados do PostgreSQL. Ele está mapeado para o diretório `/var/lib/postgresql/data` do container principal.

Container 1 (DB): Usa a imagem `postgres:15-alpine`. Responsável por armazenar e gerenciar os dados. Seu ciclo de vida é separado dos dados graças ao volume.

Container 2 (Leitor): Usa a imagem `postgres:15-alpine` (apenas como cliente `psql`). Executado para acessar o DB principal através da rede, validando o acesso e a leitura dos dados persistidos.

---

### DECISÕES TÉCNICAS

**Volumes Nomeados (Named Volumes):** A escolha por volumes nomeados é a forma recomendada pelo Docker para persistência. Eles são gerenciados pelo Docker e sobrevivem aos comandos `docker rm` e `docker-compose down`, garantindo que os dados não sejam perdidos.

**Comprovação da Persistência:** O fluxo de parar, remover e recriar o container `db_desafio2` prova que a nova instância encontrou os dados criados pela instância anterior, validando o uso do volume.

**Acesso Via Rede (Opcional):** O container `leitor_desafio2` acessa o banco usando o nome do serviço (`desafio2-db`) e injetando a senha via variável de ambiente (`PGPASSWORD`), demonstrando uma comunicação típica de microserviços.

**Imagem Alpine:** Uso de versões baseadas em Alpine Linux para manter o tamanho das imagens leve e otimizar o tempo de *download* e *startup*.

---

# Desafio 3: Docker Compose Orquestrando Serviços 

Esse desafio tem como objetivo principal usar o **Docker Compose** para orquestrar e gerenciar três serviços distintos (`web`, `db` e `cache`) que dependem uns dos outros. O foco é garantir a comunicação entre os serviços e configurar as dependências e variáveis de ambiente corretamente.

---

### INSTRUÇÕES DE EXECUÇÃO

**Pré-requisitos**: Docker e Docker Compose instalados.

1.  Navegue até o diretório do desafio ( `cd desafio3` )
2.  Inicie os containers em modo *detached* (segundo plano):
    ```bash
    docker-compose up -d
    ```
3.  **Teste de Comunicação:** Acesse o container web e comprove a conexão com os demais serviços usando seus nomes de host (DNS interno):
    ```bash
    #acessa o shell do container da aplicação
    docker exec -it desafio3-web-app sh
    
    #testa a conexão com o Cache (Redis)
    ping cache -c 3
    
    #testa a conexão com o DB (PostgreSQL) na porta 5432
    nc -vz db 5432
    ```
    O resultado esperado é `0% packet loss` no `ping` e a porta **`5432 open`** no `nc`, comprovando a comunicação entre os serviços.

    <img width="998" height="325" alt="image" src="https://github.com/user-attachments/assets/4fbe741f-2599-40fd-b382-41798bd32e8e" />


Para encerrar a execução e remover containers/rede: `docker-compose down`

---

### ARQUITETURA

Rede: Uma rede do tipo bridge chamada **'desafio3_rede'** foi criada para conectar os três serviços.

Container 1 (DB): Usa a imagem `postgres:15-alpine`. É o **Banco de Dados PostgreSQL** principal, com um Volume Nomeado para persistência de dados.

Container 2 (Cache): Usa a imagem `redis:alpine`. É o serviço de **Cache Redis**.

Container 3 (Web): Usa a imagem `busybox`. Simula a camada de **aplicação (Backend)**. Ele é usado como ponto de teste para comprovar a comunicação com o DB e o Cache.

---

### DECISÕES TÉCNICAS

**Docker Compose e Orquestração:** Utilizado para definir a infraestrutura como código, garantindo que a rede, os volumes e as variáveis de ambiente sejam criados e configurados corretamente.

**Dependências (`depends_on`):** O serviço **`web`** foi configurado com `depends_on: [db, cache]`. Isso garante que o Docker Compose inicialize primeiro o Banco de Dados e o Cache antes de tentar iniciar a aplicação web, assegurando a ordem de *startup*.

**Nomes de serviço como DNS:** Dentro da rede interna, o serviço **`web`** utiliza os nomes dos serviços (`db` e `cache`) como hostnames para estabelecer a comunicação, o que é a prática padrão do Docker Compose para comunicação entre contêineres.

**Serviço Web Simulado:** O serviço **`web`** utiliza a imagem **`busybox`** apenas para fins de teste. Com o `entrypoint` configurado para `tail -f /dev/null`, o container se mantém ativo e funcional, permitindo a execução de comandos de rede (`ping` e `nc`) para comprovar o sucesso da orquestração.
