import os
import shutil
import tempfile

from pyspark.sql import DataFrame

from config.settings import Settings


class ParquetWriter:
    """ Classe responsável pela escrita de arquivos parquet """

    def __init__(self, settings: Settings):
        self._settings = settings

    def write(self, df: DataFrame) -> None:
        """
        A abordagem abaixo cria os arquivos parquet em um diretório temporário
        e depois os move para a pasta output para evitar conflito na escrita
        e leitura, bug ocorrendo no ambiente docker. Fizemos esse workarround 
        para garantir a correta execução em qualquer ambiente.
        """
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_output = os.path.join(tmp_dir, "parquet")
            df.write.parquet(tmp_output)

            os.makedirs(self._settings.output_path, exist_ok=True)

            for item in os.listdir(self._settings.output_path):
                item_path = os.path.join(self._settings.output_path, item)
                try:
                    if os.path.isdir(item_path):
                        shutil.rmtree(item_path)
                    else:
                        os.remove(item_path)
                except PermissionError:
                    pass

            for item in os.listdir(tmp_output):
                shutil.move(
                    os.path.join(tmp_output, item),
                    os.path.join(self._settings.output_path, item),
                )
