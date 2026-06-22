import shutil
import os

from pyspark.sql import DataFrame

from config.settings import Settings


class ParquetWriter:
    """ Classe responsável pela escrita de arquivos parquet """

    def __init__(self, settings: Settings):
        self._settings = settings

    def write(self, df: DataFrame) -> None:
        if os.path.exists(self._settings.output_path):
            shutil.rmtree(self._settings.output_path, ignore_errors=True)

        df.write.mode("overwrite").parquet(self._settings.output_path)
