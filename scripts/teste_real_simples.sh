#!/bin/bash

# Ativar ambiente
source transcript_env/bin/activate

# Limpar projetos teste_real anteriores
echo "🧹 Limpando projetos teste_real anteriores..."
rm -rf projects/teste_real_*
echo ""

# Nome do projeto de teste
PROJETO="teste_real_$(date +%H%M%S)"

echo "🚀 Criando projeto: $PROJETO"
python run_analysis.py --create-project $PROJETO

echo ""
echo "📁 Copie UM arquivo .txt para:"
echo "  → projects/$PROJETO/arquivos/"
echo ""
echo "🔸 Abrindo pasta no Finder..."
open -R projects/$PROJETO/arquivos/

echo ""
echo "Pressione ENTER após copiar o arquivo..."
read

echo "🔍 Analisando..."
python run_analysis.py --project $PROJETO

echo "✅ Abrindo resultados..."
open projects/$PROJETO/output/

echo ""
echo "🎉 Análise concluída!"
echo "💡 Para limpar: rm -rf projects/$PROJETO"
