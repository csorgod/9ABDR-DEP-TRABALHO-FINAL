# TRABALHO FINAL - DATA ENGINEERING PROGRAMMING

Trabalho final da disciplina de Data Engineering Programming para o curso de pós graduação MBA em Engenharia de Dados na FIAP. Professor Marcelo Barbosa Pinto.

Membros do grupo:

- Guilherme Csorgo Henriques: 370073
- Karen Luzia Vitório Martins: 370096
- Ludmila Rocha Silva: 372484
- Thiago Guilherme: 375344

## LEIA ANTES DE EXECUTAR:
- Prezando pelas boas práticas do sistema de versinamento (SCM), segurança da informação e governança de dados, optamos por não versionar os dados direto no projeto. 
- Optamos também por usar o pacote `pipenv` ao invés do gerenciador de pacote tradicional `pip` por alguns motivos:
    - Gerencia pacotes de forma descomplicada
    - Resolve conflitos entre dependencias de forma automática
    - Guarda hashes dos pacotes em um arquivo `.lock` (bem útil combinado docker)
    - Separa dependencias de `dev` com dependencias de `prod`

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

## SOBRE O PROJETO

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
│   ├── main.py                    # Ponto de entrada (aggregation root)
│   ├── config/
│   │   └── settings.py            # Classe de configuração do projeto (caminhos, parâmetros, etc)
│   ├── spark/
│   │   └── session.py             # Classe de gerenciamento da SparkSession
│   ├── data_io/
│   │   ├── reader.py              # Classes de leitura de dados (CSV e JSON a priori)
│   │   └── writer.py              # Classe de escrita de dados (Parquet)
│   ├── business/
│   │   └── logic.py               # Classe de lógica de negócio (filtros, joins, transformações, etc)
│   └── pipeline/
│       └── orchestrator.py        # Classe de orquestração do pipeline
├── tests/
│   └── test_logic.py              # Centralização dos testes
├── data/
│   ├── pagamentos/                # Dataset de pagamentos (JSON) - não versionado
│   └── pedidos/                   # Dataset de pedidos (CSV) - não versionado
├── output/                        # Resultado do pipeline em formato Parquet - não versionado
├── Pipfile                        # Dependências gerenciadas pelo pipenv
├── Pipfile.lock                   # Lock das versões exatas das dependências
├── pyproject.toml                 # Configuração de build e metadados do projeto
├── requirements.txt               # Dependências (fallback para pip install -r)
├── MANIFEST.in                    # Arquivos incluídos no pacote distribuível
└── .gitignore                     # Regras de versionamento
```

### Descrição dos pacotes

| Pacote | Responsabilidade |
|---|---|
| `src/config` | Centraliza todas as configurações do projeto (caminhos de entrada/saída, nome da aplicação, parâmetros de execução). |
| `src/spark` | Gerencia a criação e o ciclo de vida da SparkSession. |
| `src/data_io` | Leitura dos datasets de origem (pedidos em CSV, pagamentos em JSON) e escrita do relatório final em Parquet. Todos os schemas são definidos explicitamente. |
| `src/business` | Contém as regras de negócio: filtros, joins e transformações. Inclui logging das etapas e tratamento de erros com try/except. |
| `src/pipeline` | Orquestra a execução do pipeline de ponta a ponta (leitura → transformação → escrita). |
| `tests` | Testes unitários da lógica de negócio utilizando pytest. |

### Dados

Os datasets não são versionados no repositório. Para executar o projeto, clone os datasets do professor nas pastas correspondentes:

- **Pagamentos (JSON):** copie os arquivos de `dataset-json-pagamentos/data/pagamentos/` para `data/pagamentos/`
- **Pedidos (CSV):** copie os arquivos de `datasets-csv-pedidos/data/pedidos/` para `data/pedidos/`

## Como executar

### Pré-requisitos

- Python 3.11+
- Java 8 ou 11 (necessário para o PySpark)
- pipenv (`pip install pipenv`)

### Instalação das dependências

```bash
pipenv install
```

Para instalar também as dependências de desenvolvimento (pytest):

```bash
pipenv install --dev
```

### Executando o pipeline

```bash
pipenv run python src/main.py
```

O resultado será gravado em formato Parquet na pasta `output/`.

### Executando os testes

```bash
pipenv run pytest
```
