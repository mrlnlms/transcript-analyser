#!/bin/bash

echo "🧹 LIMPEZA FINAL - Últimos detalhes"
echo "==================================="

# 1. Remover todos os .bak
echo "🗑️  Removendo arquivos .bak..."
find . -name "*.bak" -type f ! -path "./transcript_env/*" -exec rm -f {} \;

# 2. Verificar tests/mock_data
echo -e "\n�� Mock data ainda é usado?"
grep -r "mock_data\|complete_analysis_result" . --include="*.py" --exclude-dir="transcript_env" | grep -v "test" | head -5

echo -e "\n✅ Limpeza concluída!"
