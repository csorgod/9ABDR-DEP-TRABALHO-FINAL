#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DATA_DIR="$SCRIPT_DIR/data"
TMP_DIR="$SCRIPT_DIR/.tmp_download"

echo "=== Baixando datasets ==="

rm -rf "$TMP_DIR"
mkdir -p "$TMP_DIR"

echo "[1/4] Clonando repositório de pedidos (CSV)..."
git clone --depth 1 https://github.com/infobarbosa/datasets-csv-pedidos.git "$TMP_DIR/pedidos"

echo "[2/4] Copiando arquivos de pedidos para data/pedidos/..."
cp "$TMP_DIR/pedidos/data/pedidos/"*.csv.gz "$DATA_DIR/pedidos/"

echo "[3/4] Clonando repositório de pagamentos (JSON)..."
git clone --depth 1 https://github.com/infobarbosa/dataset-json-pagamentos.git "$TMP_DIR/pagamentos"

echo "[4/4] Copiando arquivos de pagamentos para data/pagamentos/..."
cp "$TMP_DIR/pagamentos/data/pagamentos/"*.json.gz "$DATA_DIR/pagamentos/"

echo "=== Limpando arquivos temporários ==="
rm -rf "$TMP_DIR"

echo "=== Concluído ==="
echo "Pedidos:    $(ls "$DATA_DIR/pedidos/"*.csv.gz 2>/dev/null | wc -l) arquivos"
echo "Pagamentos: $(ls "$DATA_DIR/pagamentos/"*.json.gz 2>/dev/null | wc -l) arquivos"
