#!/bin/bash

echo "🧹 LIMPEZA COMPLETA DO TRANSCRIPT ANALYZER"
echo "========================================"
echo ""

# 1. Mostrar o que será limpo
echo "📊 Analisando o que será removido..."
echo ""

# Projetos de teste automático
TEST_AUTO=$(ls -d projects/teste_auto_* 2>/dev/null | wc -l)
if [ $TEST_AUTO -gt 0 ]; then
    echo "📁 Projetos teste_auto_*: $TEST_AUTO projetos"
    du -sh projects/teste_auto_* 2>/dev/null | head -5
fi

# Projetos teste_real
TEST_REAL=$(ls -d projects/teste_real_* 2>/dev/null | wc -l)
if [ $TEST_REAL -gt 0 ]; then
    echo "📁 Projetos teste_real_*: $TEST_REAL projetos"
    du -sh projects/teste_real_* 2>/dev/null | head -5
fi

# Comparações de teste
COMPARISONS=$(ls projects/comparisons/*_test* 2>/dev/null | wc -l)
if [ $COMPARISONS -gt 0 ]; then
    echo "📊 Comparações de teste: $COMPARISONS arquivos"
    ls -lh projects/comparisons/*_test* 2>/dev/null | head -5
fi

# Outros projetos (opcional)
echo ""
echo "📂 Outros projetos existentes:"
ls -d projects/* 2>/dev/null | grep -v teste_auto | grep -v teste_real | grep -v comparisons || echo "  Nenhum"

echo ""
echo "⚠️  O que deseja limpar?"
echo "  1) Apenas projetos de teste (teste_auto_* e teste_real_*)"
echo "  2) Projetos de teste + comparações"
echo "  3) TUDO em projects/ (CUIDADO!)"
echo "  4) Escolher projetos específicos"
echo "  0) Cancelar"
echo ""
read -p "Escolha [0-4]: " OPCAO

case $OPCAO in
    1)
        echo "🗑️  Removendo projetos de teste..."
        rm -rf projects/teste_auto_*
        rm -rf projects/teste_real_*
        echo "✅ Projetos de teste removidos!"
        ;;
    2)
        echo "🗑️  Removendo projetos de teste e comparações..."
        rm -rf projects/teste_auto_*
        rm -rf projects/teste_real_*
        rm -rf projects/comparisons/*_test*
        echo "✅ Projetos de teste e comparações removidos!"
        ;;
    3)
        echo "⚠️  ATENÇÃO: Isso removerá TODOS os projetos!"
        read -p "Tem certeza? Digite 'SIM' para confirmar: " CONFIRMA
        if [ "$CONFIRMA" = "SIM" ]; then
            rm -rf projects/*
            echo "✅ Todos os projetos removidos!"
        else
            echo "❌ Operação cancelada"
        fi
        ;;
    4)
        echo "📝 Projetos disponíveis:"
        ls -d projects/* 2>/dev/null | grep -v comparisons | nl
        echo ""
        read -p "Digite os números dos projetos a remover (separados por espaço): " NUMS
        for NUM in $NUMS; do
            PROJ=$(ls -d projects/* 2>/dev/null | grep -v comparisons | sed -n "${NUM}p")
            if [ -n "$PROJ" ]; then
                echo "🗑️  Removendo: $PROJ"
                rm -rf "$PROJ"
            fi
        done
        echo "✅ Projetos selecionados removidos!"
        ;;
    0)
        echo "❌ Limpeza cancelada"
        exit 0
        ;;
    *)
        echo "❌ Opção inválida"
        exit 1
        ;;
esac

echo ""
echo "📊 Espaço liberado:"
echo "  Projects: $(du -sh projects 2>/dev/null | cut -f1)"
echo ""
echo "🎉 Limpeza concluída!"
