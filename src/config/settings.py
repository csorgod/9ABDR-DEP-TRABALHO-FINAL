import os


class Settings:

    def __init__(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.app_name = "9ABDR-DEP-TRABALHO-FINAL"
        self.pedidos_path = os.path.join(base_dir, "data", "pedidos")
        self.pagamentos_path = os.path.join(base_dir, "data", "pagamentos")
        self.output_path = os.path.join(base_dir, "output", "relatorio")
        self.log_path = os.path.join(base_dir, "logs")
        self.pedidos_separator = ";"
        self.pedidos_header = True
        self.output_format = "parquet"
        self.ano_filtro = 2025
