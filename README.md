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

# Desafio 2: Volumes e Persistência de Dados

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

5.  **Container leitor (Opcional):** Acesse os dados persistidos usando o segundo container através da rede:
    ```bash
    docker exec -it desafio2-leitor sh -c "PGPASSWORD=admin psql -h desafio2-db -U admin -d desafio2 -c 'SELECT * FROM usuarios;'"
    ```
    <img width="1387" height="208" alt="image" src="https://github.com/user-attachments/assets/ec500beb-733e-44f6-9e33-11c719b1663e" />


Para encerrar a execução e remover containers/rede (mantendo o volume): `docker-compose down`

---

### ARQUITETURA

Rede: Uma rede do tipo bridge chamada **'rede-desafio2'** foi criada para conectar os dois containers.

Volume: Um **volume nomeado** chamado **'dados-db-desafio2'** é usado para persistir os dados do PostgreSQL. Ele está mapeado para o diretório `/var/lib/postgresql/data` do container principal.

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

---

# Desafio 4: Microsserviços Independentes

Este desafio demonstra uma arquitetura de **microsserviços reais**, onde dois serviços isolados se comunicam exclusivamente via requisições **HTTP**. O objetivo é comprovar o isolamento de responsabilidades e a comunicação funcional entre os serviços através da rede Docker.

---

### INSTRUÇÕES DE EXECUÇÃO

**Pré-requisitos**: Docker e Docker Compose instalados.

1.  Navegue até o diretório do desafio ( `cd desafio4` )
2.  Construa as imagens e inicie os serviços:
    ```bash
    docker-compose up --build -d
    ```
3.  **Teste do Serviço A (Fornecedor):** Acesse o endpoint do Serviço A no seu navegador para verificar a lista de usuários em formato JSON:
    `http://localhost:5000/usuarios`
    
    <img width="324" height="407" alt="image" src="https://github.com/user-attachments/assets/841a7d92-5236-4ebc-9e66-befa35270034" />



4.  **Teste do Serviço B (Consumidor):** Acesse o endpoint do Serviço B para verificar a comunicação HTTP e o processamento dos dados:
    `http://localhost:5001/info`

    O Serviço B consumirá o Serviço A, formatará a saída (ex: "Usuário X ativo desde...") e a exibirá, comprovando a comunicação entre os contêineres.

    <img width="490" height="252" alt="image" src="https://github.com/user-attachments/assets/09281828-16ce-4761-aff2-2b756d3c74b2" />


Para encerrar a execução e remover containers/rede: `docker-compose down`

---

### ARQUITETURA

Rede: Uma rede do tipo bridge chamada **'desafio4_rede'** foi criada para conectar exclusivamente os dois microsserviços.

Microsserviço A: Contido no diretório `service_a/`. É o **Fornecedor de Dados**.
* Usa Flask em Python para expor o endpoint `/usuarios` (porta 5000) com uma lista mockada de usuários.
* É acessado pelo Serviço B através do hostname **`service-a`**.

Microsserviço B: Contido no diretório `service_b/`. É o **Consumidor de Dados**.
* Usa Flask e a biblioteca `requests` para fazer uma requisição HTTP GET ao Serviço A.
* Expõe o endpoint `/info` (porta 5001) com os dados formatados.

---

### DECISÕES TÉCNICAS

**Isolamento Completo (Dockerfiles):** Cada microsserviço possui seu próprio `Dockerfile` e diretório, garantindo que sejam **construídos de forma independente**, cumprindo o requisito de isolamento.

**Comunicação Via HTTP:** A comunicação entre os contêineres é realizada puramente por requisições HTTP (`requests` em Python), simulando o comportamento de APIs em uma arquitetura distribuída.

**Configuração com Variáveis de Ambiente:** O endereço do Serviço A é passado para o Serviço B via **variável de ambiente** (`SERVICE_A_URL`). Isso garante que o código da aplicação seja agnóstico ao ambiente, usando apenas o hostname **`service-a:5000`** definido pelo Docker.

**Tecnologia Flask:** Foi utilizada a *framework* Flask (Python) por sua leveza e agilidade para criar e testar APIs rapidamente, focando na lógica de comunicação Docker, e não na complexidade da aplicação.


---

# Desafio 5: Microsserviços com API Gateway

Este desafio implementa uma arquitetura de microsserviços onde o acesso externo é **centralizado** através de um **API Gateway** (utilizando Nginx). O Gateway é o único ponto de entrada para a aplicação, sendo responsável por rotear as requisições para os microsserviços corretos via rede interna.

---

### INSTRUÇÕES DE EXECUÇÃO

**Pré-requisitos**: Docker e Docker Compose instalados.

1.  Navegue até o diretório do desafio ( `cd desafio5` )
2.  Construa as imagens e inicie os serviços:
    ```bash
    docker-compose up --build -d
    ```
3.  **Teste do Gateway (Users):** Acesse o endpoint `/users` através da porta padrão do Gateway (`80`). O Gateway irá rotear internamente para o Microsserviço 1:
    `http://localhost/users`

    <img width="317" height="274" alt="image" src="https://github.com/user-attachments/assets/6753d1ed-5d80-44c6-bf8a-835ed6663073" />


5.  **Teste do Gateway (Orders):** Acesse o endpoint `/orders` através da porta padrão do Gateway (`80`). O Gateway irá rotear internamente para o Microsserviço 2:
    `http://localhost/orders`
    
    <img width="286" height="339" alt="image" src="https://github.com/user-attachments/assets/60a8c2bc-efd7-490d-a350-212434c37776" />


Ambos os testes são acessados pela porta **80** (do Gateway), comprovando que ele funciona como ponto único de entrada.

Para encerrar a execução e remover containers/rede: `docker-compose down`

---

### ARQUITETURA

Rede: Uma rede do tipo bridge chamada **'desafio5_rede'** foi criada para conectar todos os serviços de forma isolada.

Container 1 (Gateway): Usa a imagem `nginx:alpine` com um arquivo de configuração (`nginx.conf`) customizado. Este é o **ponto único de entrada** exposto na porta **80** e faz o roteamento (`proxy_pass`) para os serviços internos.

Microsserviço 1 (Users): Usa Python/Flask. É o fornecedor de dados de usuários no endpoint `/api/users` (porta 5000). Acessível internamente via hostname **`service-users`**.

Microsserviço 2 (Orders): Usa Python/Flask. É o fornecedor de dados de pedidos no endpoint `/api/orders` (porta 5001). Acessível internamente via hostname **`service-orders`**.

---

### DECISÕES TÉCNICAS

**API Gateway com Nginx:** Foi utilizado o Nginx por sua eficiência e robustez como proxy reverso. O `nginx.conf` mapeia caminhos da URL externa (`/users`, `/orders`) para endereços internos completos (`http://service-users:5000/api/users`), garantindo a **separação de domínios** e o **roteamento centralizado**.

**Centralização do Acesso:** Apenas o contêiner do **Gateway** expõe portas para o host (`80:80`). Os microsserviços de `users` e `orders` não expõem portas diretamente, reforçando o conceito de que o acesso deve ser mediado pelo Gateway.

**Integração Interna:** A comunicação entre o gateway e os microsserviços é feita via hostname do Docker Compose (`service-users` e `service-orders`), garantindo uma integração robusta e desacoplada de endereços IP.

**Serviços Leves:** Utilização do Flask (Python) para criar APIs leves e rápidas, focando no desafio de orquestração e roteamento, e não na complexidade do código de aplicação.
