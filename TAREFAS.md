# Tarefas do Projeto

Checklist de atividades para execução do trabalho final. Marque com `[✔]` conforme concluído.

---

## Fase 1 — Setup e Infraestrutura

- [✔] 1.1 Criar repositório público no GitHub
- [✔] 1.2 Clonar repositório e configurar `.gitignore`
- [✔] 1.3 Baixar dataset de pagamentos (JSON)
- [✔] 1.4 Baixar dataset de pedidos (CSV)
- [✔] 1.5 Analisar estrutura e schema dos datasets

## Fase 2 — Estrutura do Projeto e Empacotamento

- [✔] 2.1 Definir estrutura de diretórios e pacotes
- [✔] 2.2 Criar `pyproject.toml`
- [✔] 2.3 Criar `requirements.txt`
- [✔] 2.4 Criar `MANIFEST.in`
- [✔] 2.5 Criar `main.py` (esqueleto)
- [✔] 2.6 Configurar `pipenv` com `Pipfile` e `Pipfile.lock`

## Fase 3 — Desenvolvimento dos Componentes

- [✔] 3.1 Pacote de Configurações — classe de configuração centralizada (`src/config/settings.py`)
- [✔] 3.2 Pacote de Sessão Spark — classe de gerenciamento da SparkSession (`src/spark/session.py`)
- [✔] 3.3 Pacote de I/O — classe de leitura dos CSVs de pedidos com schema explícito (`src/io/reader.py`)
- [✔] 3.4 Pacote de I/O — classe de leitura dos JSONs de pagamentos com schema explícito (`src/io/reader.py`)
- [✔] 3.5 Pacote de I/O — classe de escrita do relatório em Parquet (`src/io/writer.py`)
- [✔] 3.6 Pacote de Lógica de Negócio (`src/business/logic.py`)
  - [✔] Filtrar pagamentos recusados (`status=false`)
  - [✔] Filtrar avaliação de fraude legítima (`fraude=false`)
  - [✔] Filtrar pedidos do ano de 2025
  - [✔] Join entre pedidos e pagamentos
  - [✔] Selecionar colunas: id pedido, UF, forma de pagamento, valor total, data do pedido
  - [✔] Ordenar por UF, forma de pagamento, data de criação
- [✔] 3.7 Logging — configurar `logging` na classe de lógica de negócios
- [✔] 3.8 Tratamento de Erros — implementar `try/except` com logging do erro
- [✔] 3.9 Pacote de Orquestração — classe que orquestra o pipeline (`src/pipeline/orchestrator.py`)
- [✔] 3.10 Injeção de Dependências — montar `main.py` como aggregation root

## Fase 4 — Testes

- [ ] 4.1 Criar teste unitário para a classe de lógica de negócios (`tests/test_logic.py`)
- [ ] 4.2 Executar os testes e garantir que passam (`pipenv run pytest`)

## Fase 5 — Execução e Validação

- [ ] 5.1 Executar o pipeline completo (`pipenv run python main.py`)
- [ ] 5.2 Validar o arquivo Parquet gerado (colunas, filtros, ordenação, dados de 2025)

## Fase 6 — Documentação

- [✔] 6.1 Criar `README.md` com instruções de execução
- [ ] 6.2 Push final de todo o código para o repositório público

## Fase 7 — Documento de Entrega (PDF)

- [ ] 7.1 Criar capa com nome da disciplina, nome e RM de cada integrante
- [ ] 7.2 Coletar evidências (prints) dos códigos-fonte (máx. 20 linhas por print, fonte legível)
- [ ] 7.3 Coletar evidência da execução dos testes (pytest passando)
- [ ] 7.4 Coletar evidência da execução do pipeline e do resultado (Parquet gerado)
- [ ] 7.5 Incluir link do repositório público por extenso no documento
- [ ] 7.6 Compilar tudo em documento único PDF (não .ipynb)
- [ ] 7.7 Submeter o PDF pelo Portal do Aluno
