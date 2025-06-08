#!/bin/bash
echo "🗑️  Projetos disponíveis:"
ls -d projects/*/ 2>/dev/null | sed 's/projects\///' | sed 's/\///'

echo ""
echo "Digite os nomes dos projetos para deletar (separados por espaço):"
echo "Ou digite 'todos' para limpar tudo:"
read PROJETOS

if [ "$PROJETOS" = "todos" ]; then
    echo "⚠️  Deletando TODOS os projetos..."
    rm -rf projects/*
    echo "✅ Todos os projetos foram removidos!"
else
    for proj in $PROJETOS; do
        if [ -d "projects/$proj" ]; then
            rm -rf "projects/$proj"
            echo "✅ Removido: $proj"
        else
            echo "❌ Não encontrado: $proj"
        fi
    done
fi