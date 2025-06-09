#!/bin/bash
# Script para criar novo gráfico automaticamente

if [ -z "$1" ]; then
    echo "Uso: $0 <nome_grafico> [descrição]"
    echo "Exemplo: $0 velocity_chart 'Gráfico de Velocidade'"
    exit 1
fi

NOME=$1
DESCRICAO=${2:-"Novo gráfico"}
SNAKE_CASE=$(echo "$NOME" | sed 's/[A-Z]/_&/g' | sed 's/^_//' | tr '[:upper:]' '[:lower:]')
CLASS_NAME=$(echo "$NOME" | sed 's/_\([a-z]\)/\U\1/g' | sed 's/^./\U&/')Chart

echo "🎨 Criando gráfico: $CLASS_NAME"
echo "📁 Arquivo: visuals/charts/${SNAKE_CASE}.py"
echo "⚙️ Config: config/visualization_configs/${SNAKE_CASE}_config.json"

# Copiar e personalizar template
cp visuals/charts/_template_chart.py visuals/charts/${SNAKE_CASE}.py
sed -i "s/TemplateChart/${CLASS_NAME}/g" visuals/charts/${SNAKE_CASE}.py
sed -i "s/Template para novos gráficos/${DESCRICAO}/g" visuals/charts/${SNAKE_CASE}.py

# Criar config personalizado
cp config/visualization_configs/_template.json config/visualization_configs/${SNAKE_CASE}_config.json
sed -i "s/Template para configuração de visualização/${DESCRICAO}/g" config/visualization_configs/${SNAKE_CASE}_config.json

echo "✅ Gráfico $CLASS_NAME criado!"
echo "📝 Próximo passo: editar visuals/charts/${SNAKE_CASE}.py"
