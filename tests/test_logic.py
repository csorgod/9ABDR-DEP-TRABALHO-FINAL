import pytest
from datetime import datetime
from pyspark.sql import SparkSession
from pyspark.sql.types import (
    StructType, StructField,
    StringType, IntegerType, DoubleType,
    BooleanType, TimestampType
)
from business.logic import BusinessLogic
from config.settings import Settings


# SparkSession  para a bateria de testes.
@pytest.fixture(scope="session")
def spark():
    session = (
        SparkSession.builder
        .appName("test_business_logic")
        .master("local[1]")
        .getOrCreate()
    )
    yield session
    session.stop()


@pytest.fixture(scope="session")
def settings():
    return Settings()


# df sintéticos que simulam os dados reais do pipeline.
@pytest.fixture(scope="session")
def df_pedidos(spark):
    schema = StructType([
        StructField("ID_PEDIDO",      IntegerType(),   False),
        StructField("UF",             StringType(),    False),
        StructField("DATA_CRIACAO",   TimestampType(), False),
        StructField("VALOR_UNITARIO", DoubleType(),    False),
        StructField("QUANTIDADE",     IntegerType(),   False),
    ])
    data = [
        (1, "SP", datetime(2025, 3, 10, 12, 0, 0), 10.0, 2),  # válido: 2025
        (2, "RJ", datetime(2024, 7,  1,  9, 0, 0),  5.0, 1),  # inválido: ano 2024
        (3, "MG", datetime(2025, 6, 15,  8, 0, 0), 20.0, 3),  # válido: 2025
    ]
    return spark.createDataFrame(data, schema=schema)


@pytest.fixture(scope="session")
def df_pagamentos(spark):
    schema = StructType([
        StructField("id_pedido",        IntegerType(), False),
        StructField("forma_pagamento",  StringType(),  False),
        StructField("status",           BooleanType(), False),
        StructField("avaliacao_fraude", StructType([
            StructField("fraude", BooleanType(), False)
        ]), False),
    ])
    data = [
        (1, "cartao", False, {"fraude": False}),  # válido: status=False, fraude=False
        (2, "boleto", False, {"fraude": False}),  # deverá ser excluído no join (2024)
        (3, "pix",    True,  {"fraude": False}),  # inválido: status=True
        (3, "credito",False, {"fraude": True}),   # inválido: fraude=True
    ]
    return spark.createDataFrame(data, schema=schema)


# Teste: manter apenas linhas onde status == False e avaliacao_fraude.fraude == False
def test_filtrar_pagamentos_remove_status_true_e_fraude_true(spark, settings, df_pagamentos):
    logic = BusinessLogic(spark, settings)
    result = logic._filtrar_pagamentos(df_pagamentos)
    rows = result.collect()

    ids = [r.id_pedido for r in rows]
    assert len(rows) == 2
    assert 1 in ids
    assert 2 in ids
    assert 3 not in ids


# Teste: manter apenas pedidos de 2025.
def test_filtrar_pedidos_por_ano_remove_ano_incorreto(spark, settings, df_pedidos):
    logic = BusinessLogic(spark, settings)
    result = logic._filtrar_pedidos_por_ano(df_pedidos)
    rows = result.collect()

    ids = [r.ID_PEDIDO for r in rows]
    assert len(rows) == 2
    assert 1 in ids
    assert 3 in ids
    assert 2 not in ids             # id=2 é de 2024


# Teste: retornar apenas id=1 (único ID em comum).
def test_join_pedidos_pagamentos_retorna_apenas_interseccao(spark, settings):
    logic = BusinessLogic(spark, settings)

    schema_pedidos = StructType([
        StructField("ID_PEDIDO",      IntegerType(),   False),
        StructField("UF",             StringType(),    False),
        StructField("DATA_CRIACAO",   TimestampType(), False),
        StructField("VALOR_UNITARIO", DoubleType(),    False),
        StructField("QUANTIDADE",     IntegerType(),   False),
    ])
    schema_pagamentos = StructType([
        StructField("id_pedido",       IntegerType(), False),
        StructField("forma_pagamento", StringType(),  False),
        StructField("status",          BooleanType(), False),
        StructField("avaliacao_fraude", StructType([
            StructField("fraude", BooleanType(), False)
        ]), False),
    ])

    pedidos = spark.createDataFrame(
        [(1, "SP", datetime(2025, 3, 10, 12, 0, 0), 10.0, 2),
         (3, "MG", datetime(2025, 6, 15,  8, 0, 0), 20.0, 3)],
        schema=schema_pedidos
    )
    pagamentos = spark.createDataFrame(
        [(1, "cartao", False, {"fraude": False}),
         (2, "boleto", False, {"fraude": False})],
        schema=schema_pagamentos
    )

    result = logic._join_pedidos_pagamentos(pedidos, pagamentos)
    rows = result.collect()

    assert len(rows) == 1
    assert rows[0].ID_PEDIDO == 1
    assert "id_pedido" not in result.columns



# Teste:garantir que haja 5 colunas no schema final e valor_total
def test_selecionar_colunas_retorna_schema_correto_e_calcula_valor_total(spark, settings):
    logic = BusinessLogic(spark, settings)

    schema = StructType([
        StructField("ID_PEDIDO",      IntegerType(),   False),
        StructField("UF",             StringType(),    False),
        StructField("DATA_CRIACAO",   TimestampType(), False),
        StructField("VALOR_UNITARIO", DoubleType(),    False),
        StructField("QUANTIDADE",     IntegerType(),   False),
        StructField("forma_pagamento",StringType(),    False),
    ])
    data = [(1, "SP", datetime(2025, 3, 10, 12, 0, 0), 10.0, 2, "cartao")]
    df = spark.createDataFrame(data, schema=schema)

    result = logic._selecionar_colunas(df)
    row = result.collect()[0]

    assert result.columns == ["id_pedido", "UF", "forma_pagamento", "valor_total", "data_pedido"]
    assert row.id_pedido == 1
    assert row.valor_total == 20.0 #valor * quantidade
    assert row.data_pedido == datetime(2025, 3, 10, 12, 0, 0)


# Teste: ordenar por UF, forma_pagamento e data_pedido.
def test_ordenar_resultado_por_UF_forma_pagamento_data_pedido(spark, settings):
    logic = BusinessLogic(spark, settings)

    schema = StructType([
        StructField("id_pedido",       IntegerType(),   False),
        StructField("UF",              StringType(),    False),
        StructField("forma_pagamento", StringType(),    False),
        StructField("valor_total",     DoubleType(),    False),
        StructField("data_pedido",     TimestampType(), False),
    ])
    data = [
        (3, "SP", "pix",    30.0, datetime(2025, 6, 15, 8,  0, 0)),
        (1, "MG", "cartao", 20.0, datetime(2025, 3, 10, 12, 0, 0)),
        (2, "MG", "boleto", 10.0, datetime(2025, 7,  1,  9, 0, 0)),
    ]
    df = spark.createDataFrame(data, schema=schema)

    result = logic._ordenar(df)
    rows = result.collect()

    assert rows[0].UF == "MG" and rows[0].forma_pagamento == "boleto"
    assert rows[1].UF == "MG" and rows[1].forma_pagamento == "cartao"
    assert rows[2].UF == "SP"


# Teste: validar o pipeline inteiro e retornar apenas 1 registro válido (dfs mockados)
def test_execute_retorna_apenas_registros_validos(spark, settings, df_pedidos, df_pagamentos):
    logic = BusinessLogic(spark, settings)
    result = logic.execute(df_pedidos, df_pagamentos)
    rows = result.collect()

    assert len(rows) == 1
    assert rows[0].id_pedido == 1
    assert rows[0].UF == "SP"
    assert rows[0].forma_pagamento == "cartao"
    assert rows[0].valor_total == 20.0
    assert rows[0].data_pedido == datetime(2025, 3, 10, 12, 0, 0)


# Teste: garantir que colunas finais entregues nunca mudem.
def test_execute_colunas_corretas(spark, settings, df_pedidos, df_pagamentos):
    logic = BusinessLogic(spark, settings)
    result = logic.execute(df_pedidos, df_pagamentos)

    assert result.columns == ["id_pedido", "UF", "forma_pagamento", "valor_total", "data_pedido"]