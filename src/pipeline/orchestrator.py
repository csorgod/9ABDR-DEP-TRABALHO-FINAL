import logging

from io.reader import PedidosReader, PagamentosReader
from io.writer import ParquetWriter
from business.logic import BusinessLogic

logger = logging.getLogger(__name__)


class PipelineOrchestrator:
    """
    Classe de orquestração do pipeline. Ela coordenará a ordem de execução 
    dos passos e realizará logs para para passo a ser executado afim de manter
    a rastreabilidade e identificar potenciais problemas com maior precisão 
    """

    def __init__(
        self,
        pedidos_reader: PedidosReader,
        pagamentos_reader: PagamentosReader,
        writer: ParquetWriter,
        business_logic: BusinessLogic,
    ):
        self._pedidos_reader = pedidos_reader
        self._pagamentos_reader = pagamentos_reader
        self._writer = writer
        self._business_logic = business_logic

    def run(self) -> None:
        logger.info("Iniciando pipeline")

        logger.info("Lendo dataset de pedidos")
        df_pedidos = self._pedidos_reader.read()

        logger.info("Lendo dataset de pagamentos")
        df_pagamentos = self._pagamentos_reader.read()

        logger.info("Executando lógica de negócio")
        df_resultado = self._business_logic.execute(df_pedidos, df_pagamentos)

        logger.info("Gravando relatório em Parquet")
        self._writer.write(df_resultado)

        logger.info("Pipeline finalizado com sucesso")
