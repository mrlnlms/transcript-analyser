Perfeito! Vamos rodar o Transcript Analyzer do zero! 

Opa! O ambiente virtual não existe ainda. Vamos criar do zero:

### 1. **Primeiro, verifique se tem Python 3 instalado**
```bash
python3 --version
```

### 2. **Crie o ambiente virtual**
```bash
python3 -m venv transcript_env
```

### 3. **Ative o ambiente virtual**
```bash
source transcript_env/bin/activate
```

### 4. **Agora sim, instale as dependências**
```bash
pip install -r requirements_working.txt
```

### 5. **Teste se funcionou**
```bash
python run_analysis.py --help
```

## Se o python3 não estiver instalado:

### Opção 1: Instale via Homebrew (recomendado)
```bash
# Instala Homebrew se não tiver
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Instala Python
brew install python3
```

### Opção 2: Baixe do site oficial
- Vá para [python.org](https://python.org)
- Baixe a versão mais recente para macOS

## Alternativamente, use o setup automático:

O projeto tem um arquivo `setup_auto.py`! Tente:

```bash
python3 setup_auto.py
```

Esse script deve fazer tudo automaticamente para você!

Me avisa qual comando funcionou! 🚀


---
> Caso não tenha funcionado, siga o passo a passo abaixo.

## Passo a passo completo:


### 1. **Ative o ambiente virtual**
```bash
source transcript_env/bin/activate
```
Você deve ver `(transcript_env)` aparecer no início da linha do terminal.

### 2. **Verifique se está tudo OK**
```bash
# Testa se as dependências estão instaladas
python run_analysis.py --help
```

### 3. **Liste os projetos disponíveis**
```bash
python run_analysis.py --list-projects
```

### 4. **Se não tiver nenhum projeto, crie um**
```bash
python run_analysis.py --create-project teste_inicial
```

### 5. **Adicione uma transcrição para analisar**
```bash
# Opção A: Copie um arquivo .txt que você já tenha
cp caminho/do/seu/arquivo.txt projects/teste_inicial/arquivos/

# Opção B: Crie um arquivo de teste
echo "Esta é uma transcrição de teste. Estou muito feliz com o projeto. A análise está funcionando perfeitamente!" > projects/teste_inicial/arquivos/teste.txt
```

### 6. **Execute a análise**
```bash
python run_analysis.py --project teste_inicial
```

### 7. **Veja os resultados**
```bash
# Lista o que foi gerado
ls projects/teste_inicial/resultados/

# Abre o dashboard (se tiver gerado HTML)
open projects/teste_inicial/resultados/dashboard.html
```

## Comandos úteis extras:

```bash
# Testar as visualizações
python run_analysis.py --test-visuals

# Análise comparativa (se tiver múltiplos projetos)
python run_analysis.py --compare projeto1 projeto2

# Ver configurações do projeto
cat projects/teste_inicial/config_analise.json
```

## Se der algum erro:

1. **Dependências faltando**:
```bash
pip install -r requirements_working.txt
```

2. **Erro de módulo não encontrado**:
```bash
# Certifique-se de estar na pasta raiz
pwd  # Deve mostrar: /Users/mosx/Desktop/transcript-analyser
```

Me avisa o que aconteceu quando rodar! 🚀