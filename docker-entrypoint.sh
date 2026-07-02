#!/bin/bash
set -e
 
DATA_DIR="/app/data"
 
if [ -z "$(ls "$DATA_DIR/pedidos/"*.csv.gz 2>/dev/null)" ] || [ -z "$(ls "$DATA_DIR/pagamentos/"*.json.gz 2>/dev/null)" ]; then
    echo "=== Baixando datasets ==="
 
    TMP_DIR="/tmp/datasets"
    rm -rf "$TMP_DIR"
    mkdir -p "$TMP_DIR"
 
    echo "[1/4] Clonando repositorio de pedidos..."
    git clone --depth 1 https://github.com/infobarbosa/datasets-csv-pedidos.git "$TMP_DIR/pedidos"
 
    echo "[2/4] Copiando arquivos de pedidos..."
    cp "$TMP_DIR/pedidos/data/pedidos/"*.csv.gz "$DATA_DIR/pedidos/"
 
    echo "[3/4] Clonando repositorio de pagamentos..."
    git clone --depth 1 https://github.com/infobarbosa/dataset-json-pagamentos.git "$TMP_DIR/pagamentos"
 
    echo "[4/4] Copiando arquivos de pagamentos..."
    cp "$TMP_DIR/pagamentos/data/pagamentos/"*.json.gz "$DATA_DIR/pagamentos/"
 
    rm -rf "$TMP_DIR"
    echo "=== Download concluido ==="
else
    echo "=== Dados ja presentes, pulando download ==="
fi
 
echo "=== Executando pipeline ==="
spark-submit src/main.py

exec tail -f /dev/null