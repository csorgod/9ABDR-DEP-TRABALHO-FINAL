#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DATA_DIR="$SCRIPT_DIR/data"
TMP_DIR="$SCRIPT_DIR/.tmp_download"

# ==============================
# 1. Download dos datasets
# ==============================
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

echo "Pedidos:    $(ls "$DATA_DIR/pedidos/"*.csv.gz 2>/dev/null | wc -l) arquivos"
echo "Pagamentos: $(ls "$DATA_DIR/pagamentos/"*.json.gz 2>/dev/null | wc -l) arquivos"

# ==============================
# 2. Instalação do pipenv (caso não exista ainda)
# ==============================
echo ""
echo "=== Configurando ambiente Python ==="

if ! command -v pipenv &> /dev/null; then
    echo "Instalando pipenv..."
    pip install pipenv
else
    echo "pipenv já instalado: $(pipenv --version)"
fi

# ==============================
# 3. Criação do ambiente virtual e instalação de dependências
# ==============================
echo ""
echo "=== Criando ambiente virtual e instalando dependências ==="

PYTHON_BIN="$(command -v python3.11 || command -v python3 || command -v python)"
if [ -z "$PYTHON_BIN" ]; then
    echo "Nenhum interpretador Python encontrado no PATH." >&2
    exit 1
fi
echo "Usando interpretador Python: $PYTHON_BIN"

cd "$SCRIPT_DIR"
pipenv install --dev --python "$PYTHON_BIN"

# ==============================
# 4. Execução do pipeline
# ==============================
echo ""
echo "=== Executando pipeline via spark-submit ==="

pipenv run spark-submit src/main.py

echo ""
echo "=== Pipeline concluído com sucesso ==="
