import logging
import logging.config

from config.logging import log_config
from config.settings import Settings
from spark.session import SparkSessionManager
from data_io.reader import PedidosReader, PagamentosReader
from data_io.writer import ParquetWriter
from business.logic import BusinessLogic
from pipeline.orchestrator import PipelineOrchestrator

logging.config.dictConfig(log_config)
logger = logging.getLogger(__name__)


def main():
    logger.info("Inicializando aplicação")

    settings = Settings()
    spark_manager = SparkSessionManager(settings)
    spark = spark_manager.get_session()

    pedidos_reader = PedidosReader(spark, settings)
    pagamentos_reader = PagamentosReader(spark, settings)
    writer = ParquetWriter(settings)
    business_logic = BusinessLogic(spark, settings)

    pipeline = PipelineOrchestrator(
        pedidos_reader=pedidos_reader,
        pagamentos_reader=pagamentos_reader,
        writer=writer,
        business_logic=business_logic,
    )

    try:
        pipeline.run()
    except Exception as e:
        logger.error("Erro fatal na execução do pipeline: %s", e)
        raise
    finally:
        spark_manager.stop()
        logger.info("Aplicação encerrada")


if __name__ == "__main__":
    main()
