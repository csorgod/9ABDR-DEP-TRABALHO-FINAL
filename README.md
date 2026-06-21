# TRABALHO FINAL - DATA ENGINEERING PROGRAMMING

Trabalho final da disciplina de Data Engineering Programming para o curso de pós graduação MBA em Engenharia de Dados na FIAP. Professor Marcelo Barbosa Pinto.

Membros do grupo:

- Guilherme Csorgo Henriques: 370073
- Karen Luzia Vitório Martins: 370096
- Ludmila Rocha Silva: 372484
- Thiago Guilherme: 375344

## ⚠️ LEIA ANTES DE EXECUTAR: ⚠️
- Prezando pelas boas práticas do sistema de versinamento (SCM), segurança da informação e governança de dados, optamos por não versionar os dados direto no projeto. 
- Optamos também por usar o pacote `pipenv` ao invés do gerenciador de pacote tradicional `pip` por alguns motivos:
    - Gerencia pacotes de forma descomplicada
    - Resolve conflitos entre dependencias de forma automática
    - Guarda hashes dos pacotes em um arquivo `.lock` (bem útil combinado docker)
    - Separa dependencias de `dev` com dependencias de `prod`

### MÉTODO PRINCIPAL - Via Bash Script

 Para não perdermos a facilidade de execução como trade-off, criamos um script que abstrai todo o setup do projeto. O arquivo `run_program.sh` irá:

* Baixar os dados para as pastas `data/pagamentos` e `data/pedidos`;
* Instala o pacote `pipenv`
* Cria um ambiente virtual `pipenv`
* Instala todas as dependencias
* Executa `spark-submit src/main.py` 

Portanto, para testar esse projeto, basta executar:

```sh
bash run_program.py
```

### MÉTODO ALTERNATIVO - Via Docker

Requer apenas Docker instalado. Irá fazer todo o trabalho duro pra você (igual o méotodo principal, mas considerando a sequencia necesária pra imagem docker)

#### Com docker compose
```sh
docker compose up --build
```

#### Sem docker compose

```sh
docker build -t dep-trabalho-final .
docker run -v ./output:/app/output -v ./logs:/app/logs dep-trabalho-final
```

O Dockerfile irá cuidar de todo o ambiente (Python 3.11, Java 17, pipenv e dependências). O container apenas executa spark-submit src/main.py. Os volumes montados garantem que o Parquet gerado e os logs fiquem acessíveis na máquina host.

**Por que não reutilizamos o `run_program.sh` dentro do Docker?**
> O `run_program.sh` foi feito para setup em máquina local — ele baixa dados, instala pipenv, cria virtualenv e instala dependências. Dentro do Docker, tudo isso já é resolvido pelo `Dockerfile` durante o build. Reutilizá-lo no container significaria refazer trabalho desnecessário, depender de acesso à internet em runtime e criar um virtualenv dentro de um container (antipattern). Por isso o entrypoint do Docker executa apenas o `spark-submit`.


## SOBRE O PROJETO

### PRÉ-REQUISITOS

- Python 3.11+
- Java 8 ou 11 (necessário para o PySpark)
- pipenv (`pip install pipenv`)

### Escopo e sequencia de atividades
Para centralizarmos o escopo e o passo a passo de execução, criamos dois arquivos na raiz do projeto: 
- [ESCOPO.md](ESCOPO.md): O objetivo do trabalho, conforme registrado no portal do aluno. Esse conteúdo é identico ao original, apenas copiamos e colamos aqui em Markdown.
- [TAREFAS.md](TAREFAS.md): Uma abstração do escopo em entregáveis e a ordem que seguimos.

### Uso de IA
Esse projeto foi feito ~90% por humanos e ~10% por IA Generativa. Acreditamos que a tecnologia tem um papel fundamental como acelerador do processo de entrega. Por isso, você encontrará partes do projeto organizadas ou escritas por IA, principalmente em arquivos `.md`. Por mais que a IA pudesse criar e entregar o projeto inteiro, entendemos que não faria sentido visto que a intenção do trabalho é consolidar os entendimentos dos alunos em relação à programação para Engenharia de Dados.

### Github e SCM
Sobre o sistema de versionamento, optamos por usar uma única branch (main) para simplificar o desenvolvimento e evitar conflitos dado o prazo apertado para entrega do projeto. Em um sistema real, provavelmente você encontraria algo similar à `git flow`, com branches para releases, bugfix, features, etc. 

## TODOs: 
- Revisar e atualizar o "Estrutura do Projeto" e o "Descrição dos pacotes" ao final do trabalho

## ESTRUTURA DO PROJETO
Buscamos criar uma estrutura que consolide os aprendizados vistos em aula com as boas práticas de mercado. Levamos em consideração tanto a separação de escopos como a modularização dos escopos. 

```
9ABDR-DEP-TRABALHO-FINAL/
├── src/                           # Pacote principal da aplicação
│   ├── main.py                    # Ponto de entrada (aggregation root) e injeção de dependências
│   ├── __init__.py
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings.py            # Classe de configuração centralizada (caminhos, parâmetros, etc)
│   │   └── logging.py             # Configuração do logging (dictConfig para console e arquivo)
│   ├── spark/
│   │   ├── __init__.py
│   │   └── session.py             # Classe de gerenciamento da SparkSession
│   ├── data_io/
│   │   ├── __init__.py
│   │   ├── reader.py              # Classes de leitura de dados (PedidosReader e PagamentosReader)
│   │   └── writer.py              # Classe de escrita de dados em Parquet (ParquetWriter)
│   ├── business/
│   │   ├── __init__.py
│   │   └── logic.py               # Classe de lógica de negócio (filtros, joins, transformações, validação)
│   └── pipeline/
│       ├── __init__.py
│       └── orchestrator.py        # Classe de orquestração do pipeline
├── tests/
│   ├── __init__.py
│   └── test_logic.py              # Testes unitários da lógica de negócio
├── data/
│   ├── pagamentos/                # Dataset de pagamentos (JSON gzip) - não versionado
│   ├── pedidos/                   # Dataset de pedidos (CSV gzip) - não versionado
│   └── README.md                  # Documentação dos schemas e relacionamento entre datasets
├── logs/                          # Logs de execução do pipeline - não versionado
├── output/                        # Resultado do pipeline em formato Parquet - não versionado
├── Dockerfile                     # Imagem Docker do projeto (Python 3.11 + Java 17 + PySpark)
├── docker-compose.yml             # Orquestração do container com volumes para output e logs
├── docker-entrypoint.sh           # Entrypoint: baixa dados se necessário e executa o pipeline
├── .dockerignore                  # Arquivos excluídos do contexto de build Docker
├── run_program.sh                 # Script ponta a ponta: download dos dados, pipenv, dependências e execução
├── Pipfile                        # Dependências gerenciadas pelo pipenv
├── Pipfile.lock                   # Lock das versões exatas das dependências
├── pyproject.toml                 # Configuração de build e metadados do projeto
├── requirements.txt               # Dependências (fallback para pip install -r)
├── MANIFEST.in                    # Arquivos incluídos no pacote distribuível
├── ESCOPO.md                      # Enunciado do trabalho (cópia do portal do aluno)
├── TAREFAS.md                     # Checklist de atividades e progresso
└── .gitignore                     # Regras de versionamento
```

### DESCRIÇÃO DOS PACOTES

| Pacote | Responsabilidade |
|---|---|
| `src/config` | Centraliza todas as configurações do projeto (caminhos de entrada/saída, nome da aplicação, parâmetros de execução) e a configuração do logging (saída para console e arquivo). |
| `src/spark` | Gerencia a criação e o ciclo de vida da SparkSession com lazy initialization. |
| `src/data_io` | Leitura dos datasets de origem (pedidos em CSV, pagamentos em JSON) e escrita do relatório final em Parquet. Todos os schemas são definidos explicitamente, sem inferência. |
| `src/business` | Contém as regras de negócio: filtros (status, fraude, ano), join entre pedidos e pagamentos, seleção de colunas, ordenação e validação do Parquet gerado. Inclui logging das etapas e tratamento de erros com try/except. |
| `src/pipeline` | Orquestra a execução do pipeline de ponta a ponta (leitura → transformação → escrita → validação). |
| `tests` | Testes unitários da lógica de negócio utilizando pytest. |
