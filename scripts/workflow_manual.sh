#!/bin/bash
source transcript_env/bin/activate

# CUSTOMIZE AQUI OS NOMES DOS SEUS PROJETOS!
echo "📝 Digite o nome do projeto 1 (1 transcrição):"
read PROJ1
echo "📝 Digite o nome do projeto 2 (2 transcrições):"
read PROJ2
echo "📝 Digite o nome do projeto 3 (3 transcrições):"
read PROJ3

echo "🚀 Criando projetos..."
python run_analysis.py --create-project $PROJ1
python run_analysis.py --create-project $PROJ2
python run_analysis.py --create-project $PROJ3

echo ""
echo "📁 AGORA COPIE SUAS TRANSCRIÇÕES PARA:"
echo "  → projects/$PROJ1/arquivos/ (1 arquivo .txt)"
echo "  → projects/$PROJ2/arquivos/ (2 arquivos .txt)"
echo "  → projects/$PROJ3/arquivos/ (3 arquivos .txt)"
echo ""
echo "🔸 Dica: Abra o Finder com: open projects/"
echo ""
echo "Pressione ENTER quando terminar de copiar os arquivos..."
read

echo "🔍 Analisando projetos..."
python run_analysis.py --project $PROJ1
python run_analysis.py --project $PROJ2
python run_analysis.py --project $PROJ3

echo "📊 Deseja comparar os projetos? (s/n)"
read COMPARAR

if [ "$COMPARAR" = "s" ]; then
    python run_analysis.py --compare $PROJ1 $PROJ2 $PROJ3
fi

echo "✅ Abrindo resultados..."
open projects/$PROJ1/output/*/*.html
open projects/$PROJ2/output/*/*.html
open projects/$PROJ3/output/*/*.html

echo "🎉 Concluído!"
echo ""
echo "💡 Para deletar estes projetos depois:"
echo "   rm -rf projects/$PROJ1 projects/$PROJ2 projects/$PROJ3"