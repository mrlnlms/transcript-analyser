#!/bin/bash
# Script para criar nova análise automaticamente

if [ -z "$1" ]; then
    echo "Uso: $0 <nome_analise> [descrição]"
    echo "Exemplo: $0 speech_velocity 'Análise de Velocidade de Fala'"
    exit 1
fi

NOME=$1
DESCRICAO=${2:-"Nova análise"}

# Conversão correta para snake_case
SNAKE_CASE=$(echo "$NOME" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/_/g' | sed 's/__*/_/g' | sed 's/^_\|_$//g')

# Conversão correta para PascalCase
CLASS_NAME=$(echo "$SNAKE_CASE" | awk -F'_' '{for(i=1;i<=NF;i++){$i=toupper(substr($i,1,1)) substr($i,2)}} 1' OFS='')Analyzer

echo "🔧 Criando análise: $CLASS_NAME"
echo "📁 Arquivo: engine/analyzers/${SNAKE_CASE}.py"
echo "⚙️ Config: config/analysis_configs/${SNAKE_CASE}_config.json"

# Copiar template
cp engine/analyzers/_template_analyzer.py engine/analyzers/${SNAKE_CASE}.py

# Personalizar
sed -i '' "s/TemplateAnalyzer/${CLASS_NAME}/g" engine/analyzers/${SNAKE_CASE}.py
sed -i '' "s/Template para novos analisadores/${DESCRICAO}/g" engine/analyzers/${SNAKE_CASE}.py

# Criar config
cp config/analysis_configs/_template.json config/analysis_configs/${SNAKE_CASE}_config.json
sed -i '' "s/Template para configuração de análise/${DESCRICAO}/g" config/analysis_configs/${SNAKE_CASE}_config.json

echo "✅ Análise $CLASS_NAME criada!"
echo "📝 Próximo passo: editar engine/analyzers/${SNAKE_CASE}.py"
