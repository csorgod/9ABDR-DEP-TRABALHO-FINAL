import logging

from pyspark.sql import DataFrame
from pyspark.sql.functions import col, year

from config.settings import Settings


class BusinessLogic:
    """ 
    Classe centralizadora da regra de negócio. É onde aplicaremos as regras de 
    tratamento e agregação. As regras serão definidas em doc string nas respectivas
    funções. 

    A alta gestão da empresa deseja um relatório de pedidos de venda cujo pagamentos 
    recusados (status=false) e que na avaliação de fraude foram classificados como 
    legítimos (fraude=false).

    O relatório deve ter os seguintes atributos:
    - 1. Identificador do pedido (id pedido)
    - 2. Estado (UF) onde o pedido foi feito
    - 3. Forma de pagamento
    - 4. Valor total do pedido
    - 5. Data do pedido

    - O relatório deve compreender pedidos apenas do ano de 2025.
    - O relatório deve estar ordenado por estado (UF), forma de pagamento e data de criação do pedido.
    - O relatório deve ser gravado em formato parquet.
    """

    def __init__(self, settings: Settings):
        self.logger = logging.getLogger(__name__)
        self._settings = settings

    def execute(self, df_pedidos: DataFrame, df_pagamentos: DataFrame) -> DataFrame:
        try:
            self.logger.info("Iniciando execução da lógica de negócio")

            self.logger.info("Pedidos recebidos: %d registros", df_pedidos.count())
            self.logger.info("Pagamentos recebidos: %d registros", df_pagamentos.count())

            df_pagamentos_filtrado = self._filtrar_pagamentos(df_pagamentos)
            self.logger.info("Pagamentos após filtro (status=false, fraude=false): %d registros", df_pagamentos_filtrado.count())

            df_pedidos_filtrado = self._filtrar_pedidos_por_ano(df_pedidos)
            self.logger.info("Pedidos após filtro (ano=%d): %d registros", self._settings.ano_filtro, df_pedidos_filtrado.count())

            df_joined = self._join_pedidos_pagamentos(df_pedidos_filtrado, df_pagamentos_filtrado)
            self.logger.info("Registros após join: %d", df_joined.count())

            df_selecionado = self._selecionar_colunas(df_joined)
            df_ordenado = self._ordenar(df_selecionado)
            self.logger.info("Lógica de negócio finalizada com sucesso — %d registros no relatório final", df_ordenado.count())
            return df_ordenado
        except Exception as e:
            self.logger.error("Erro durante a execução da lógica de negócio: %s", e)
            raise

    def _filtrar_pagamentos(self, df: DataFrame) -> DataFrame:
        """
        filtra pagamentos onde status == False (recusados) e avaliacao_fraude.fraude == False 
        (classificados como legítimos). 
        """
        self.logger.info("Filtrando pagamentos recusados (status=false) e fraude legítima (fraude=false)")
        return df.filter(
            (~col("status")) & (~col("avaliacao_fraude.fraude"))
        )

    def _filtrar_pedidos_por_ano(self, df: DataFrame) -> DataFrame:
        """
        usa a função year() do PySpark para extrair o ano de DATA_CRIACAO e manter 
        apenas pedidos de 2025 (configuramos a regra em settings.ano_filtro)
        """
        self.logger.info("Filtrando pedidos do ano de %d", self._settings.ano_filtro)
        return df.filter(year(col("DATA_CRIACAO")) == self._settings.ano_filtro)

    def _join_pedidos_pagamentos(self, df_pedidos: DataFrame, df_pagamentos: DataFrame) -> DataFrame:
        """
         faz um inner join entre pedidos e pagamentos pela chave ID_PEDIDO == id_pedido 
         (o casing é diferente entre os datasets, por isso a comparação explícita entre 
         as duas colunas). Podiamos tratar esse campo, mas não estava no escopo do projeto.
        """
        self.logger.info("Realizando join entre pedidos e pagamentos (ID_PEDIDO == id_pedido)")
        return (
            df_pedidos.join(
                df_pagamentos,
                df_pedidos["ID_PEDIDO"] == df_pagamentos["id_pedido"],
                "inner",
            )
            .drop(df_pagamentos["id_pedido"])
        )

    def _selecionar_colunas(self, df: DataFrame) -> DataFrame:
        """
        Retorna apenas as 5 colunas do relatório final:
        - id_pedido (alias de ID_PEDIDO)
        - UF
        - forma_pagamento (vem do dataset de pagamentos)
        - valor_total = VALOR_UNITARIO * QUANTIDADE (calculado, não é o valor_pagamento)
        - data_pedido (alias de DATA_CRIACAO)
        """
        self.logger.info("Selecionando colunas do relatório: id_pedido, UF, forma_pagamento, valor_total, data_pedido")
        return df.select(
            col("ID_PEDIDO").alias("id_pedido"),
            col("UF"),
            col("forma_pagamento"),
            (col("VALOR_UNITARIO") * col("QUANTIDADE")).alias("valor_total"),
            col("DATA_CRIACAO").alias("data_pedido"),
        )

    def _ordenar(self, df: DataFrame) -> DataFrame:
        """ ordena o resultado por UF, forma_pagamento e data_pedido """
        self.logger.info("Ordenando resultado por UF, forma_pagamento e data_pedido")
        return df.orderBy("UF", "forma_pagamento", "data_pedido")
