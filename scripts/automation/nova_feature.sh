#!/bin/bash
# Script para criar análise + gráfico de uma vez

if [ -z "$1" ]; then
    echo "Uso: $0 <nome_feature> [descrição]"
    echo "Exemplo: $0 emotion_phases 'Análise de Fases Emocionais'"
    exit 1
fi

NOME=$1
DESCRICAO=${2:-"Nova feature"}

echo "🚀 Criando feature completa: $NOME"
echo "📊 Análise + 📈 Gráfico"

# Criar análise
./scripts/automation/nova_analise.sh "${NOME}_analysis" "$DESCRICAO"

# Criar gráfico
./scripts/automation/novo_grafico.sh "${NOME}_chart" "Gráfico de $DESCRICAO"

echo ""
echo "✅ Feature $NOME criada completamente!"
echo "📝 Próximos passos:"
echo "   1. Editar engine/analyzers/${NOME}_analysis.py"
echo "   2. Editar visuals/charts/${NOME}_chart.py"
echo "   3. Testar: python run_analysis.py --test-analysis ${NOME}_analysis"
