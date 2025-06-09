# Prompt para Implementação de POC - Obsidian Plugin com Python Server

## Objetivo
Criar uma prova de conceito (POC) minimalista para validar a integração entre um plugin Obsidian e um servidor Python local. O foco é testar o fluxo completo de forma simples e funcional.

## Requisitos da POC

### 1. Plugin Obsidian (TypeScript)
Criar um plugin Obsidian extremamente simples com:

- **Um único comando** no Command Palette: "Analyze Current Note with Python"
- **Funcionalidade**: 
  - Pega o texto da nota atual
  - Envia para servidor Python (se estiver rodando)
  - Recebe resposta com análise básica
  - Mostra resultado em um Notice ou Modal simples
- **Fallback**: Se servidor não estiver rodando, mostra mensagem explicativa

### 2. Servidor Python (FastAPI)
Criar servidor minimalista com:

- **Um único endpoint**: POST `/analyze`
- **Análise super básica**:
  - Contar palavras
  - Contar sentenças  
  - Identificar palavra mais frequente
  - Calcular sentimento básico (positivo/negativo/neutro)
- **Resposta JSON** simples e clara

### 3. Estrutura de Arquivos

```
obsidian-python-poc/
├── README.md              # Instruções de instalação e uso
├── manifest.json          # Metadata do plugin
├── main.ts               # Plugin (um arquivo só)
├── package.json          # Dependências
├── tsconfig.json         # Config TypeScript
│
└── python-server/
    ├── server.py         # Servidor FastAPI (um arquivo só)
    └── requirements.txt  # fastapi, uvicorn
```

### 4. Código do Plugin (main.ts)

O plugin deve:
```typescript
// Estrutura básica:
- Classe principal extends Plugin
- Um comando que:
  - Pega texto da nota ativa
  - Faz fetch para http://localhost:5000/analyze
  - Trata erros (servidor offline)
  - Mostra resultado
```

### 5. Código do Servidor (server.py)

O servidor deve:
```python
# Estrutura básica:
- FastAPI app
- Endpoint POST /analyze que recebe {"text": "..."}
- Função analyze_text() que retorna:
  {
    "word_count": 150,
    "sentence_count": 8,
    "most_common_word": "pesquisa",
    "sentiment": "positive",
    "message": "Análise completa!"
  }
- CORS habilitado para funcionar com Obsidian
```

### 6. Instruções no README

```markdown
## Como testar a POC

### 1. Instalar o Plugin
- Clone este repo
- Copie a pasta para .obsidian/plugins/
- Ative o plugin nas configurações

### 2. Rodar o Servidor Python
cd python-server
pip install -r requirements.txt
python server.py

### 3. Testar
- Abra uma nota no Obsidian
- Ctrl+P → "Analyze Current Note with Python"
- Veja o resultado!
```

## Critérios de Sucesso

1. ✅ Plugin instala e ativa sem erros
2. ✅ Comando aparece no Command Palette
3. ✅ Servidor Python roda com `python server.py`
4. ✅ Análise funciona quando servidor está rodando
5. ✅ Mensagem clara quando servidor está offline
6. ✅ Resultado aparece no Obsidian (Notice ou Modal)

## Simplicidade é Chave

- **Sem** interface complexa
- **Sem** configurações
- **Sem** dependências desnecessárias
- **Sem** features além do essencial
- **Foco**: Provar que a comunicação Plugin ↔ Python funciona

## Output Esperado

Quando funcionar, o usuário verá algo como:

```
📊 Análise Completa!
- Palavras: 523
- Sentenças: 24
- Palavra mais comum: "pesquisa" (12x)
- Sentimento: Positivo
```

## Objetivo Final

Esta POC deve responder: 
"É possível e prático ter um plugin Obsidian que usa processamento Python local?"

Se sim → Evoluir para o Transcript Analyzer completo
Se não → Avaliar alternativas (WASM, TypeScript puro, etc.)


----

# Prompt para POC - Plugin Obsidian com Executável Python Compilado

## Objetivo
Criar uma POC que valide o fluxo completo: Plugin Obsidian → Executável Python (PyInstaller) → Resultado no Obsidian. **Sem necessidade do usuário instalar Python**.

## Requisitos da POC

### 1. Adaptar o Transcript Analyzer Existente

**Criar wrapper FastAPI** para o projeto atual:
```python
# server_wrapper.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from engine.analyzer_core import analyze_text  # Seu código existente!

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"])

@app.post("/analyze")
async def analyze_endpoint(data: dict):
    # Usa sua análise existente
    results = analyze_text(data['text'])
    # Retorna versão simplificada para POC
    return {
        "sentiment": results.get('sentiment_global', 0),
        "topics": results.get('topics', [])[:3],  # Top 3 tópicos
        "word_count": results.get('word_count', 0),
        "processing": "python_compiled"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000)
```

### 2. Compilar com PyInstaller

**Script de build**:
```bash
# build_server.sh
# Cria executável standalone
pyinstaller --onefile \
    --name transcript-analyzer-server \
    --add-data "resources:resources" \
    --hidden-import uvicorn \
    --hidden-import fastapi \
    server_wrapper.py

# Resultado: dist/transcript-analyzer-server.exe (Windows)
#           dist/transcript-analyzer-server (Mac/Linux)
```

### 3. Plugin Obsidian Minimalista

```typescript
// main.ts - Plugin que baixa e executa o servidor
import { Plugin, Notice, FileSystemAdapter } from 'obsidian';
import { spawn, ChildProcess } from 'child_process';
import * as path from 'path';

export default class TranscriptAnalyzerPOC extends Plugin {
    private server: ChildProcess | null = null;
    private serverPath: string = '';

    async onload() {
        // Comando principal
        this.addCommand({
            id: 'analyze-with-compiled-python',
            name: 'Analisar nota (Python Compilado)',
            callback: () => this.runAnalysis()
        });

        // Verifica se servidor existe
        this.checkServerInstalled();
    }

    async checkServerInstalled() {
        const adapter = this.app.vault.adapter as FileSystemAdapter;
        const vaultPath = adapter.getBasePath();
        const pluginPath = path.join(vaultPath, '.obsidian/plugins/transcript-poc');
        
        // Caminho do executável
        const execName = process.platform === 'win32' ? 
            'transcript-analyzer-server.exe' : 
            'transcript-analyzer-server';
        
        this.serverPath = path.join(pluginPath, 'bin', execName);
        
        // Verifica se existe
        if (!await adapter.exists(this.serverPath)) {
            new Notice('⚠️ Servidor não encontrado. Baixe em: [link]');
        }
    }

    async runAnalysis() {
        // 1. Inicia servidor se necessário
        if (!this.server) {
            await this.startServer();
        }

        // 2. Pega texto da nota
        const activeFile = this.app.workspace.getActiveFile();
        if (!activeFile) {
            new Notice('Nenhuma nota ativa!');
            return;
        }

        const content = await this.app.vault.read(activeFile);

        // 3. Envia para análise
        try {
            const response = await fetch('http://localhost:5000/analyze', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text: content })
            });

            const results = await response.json();
            
            // 4. Mostra resultado
            new Notice(`
                📊 Análise Completa!
                Sentimento: ${results.sentiment > 0 ? '😊 Positivo' : '😐 Neutro'}
                Tópicos: ${results.topics.join(', ')}
                Palavras: ${results.word_count}
            `);

        } catch (error) {
            new Notice('❌ Erro na análise. Servidor está rodando?');
        }
    }

    async startServer() {
        new Notice('🚀 Iniciando servidor...');
        
        this.server = spawn(this.serverPath, [], {
            detached: false,
            stdio: 'ignore'  // Não mostra console
        });

        // Espera servidor iniciar
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        new Notice('✅ Servidor pronto!');
    }

    onunload() {
        // Mata o servidor ao desativar plugin
        if (this.server) {
            this.server.kill();
        }
    }
}
```

### 4. Estrutura Final

```
obsidian-transcript-poc/
├── README.md
├── manifest.json
├── main.ts
├── package.json
│
├── bin/                          # Executáveis compilados
│   ├── transcript-analyzer-server.exe     # Windows
│   ├── transcript-analyzer-server-mac     # macOS
│   └── transcript-analyzer-server-linux   # Linux
│
└── python-source/               # Código fonte (no repo)
    ├── server_wrapper.py
    └── build_server.sh
```

### 5. Fluxo de Instalação para Usuário

```markdown
## Instalação (Super Simples!)

1. **Instalar plugin via BRAT**
   - Add repo: github.com/seu-usuario/obsidian-transcript-poc
   - Install & Enable

2. **Baixar servidor** (uma vez só)
   - Windows: [Download transcript-analyzer-server.exe](link)
   - Mac: [Download transcript-analyzer-server-mac](link)
   - Linux: [Download transcript-analyzer-server-linux](link)
   
3. **Colocar na pasta do plugin**
   - Coloque em: `.obsidian/plugins/transcript-poc/bin/`

4. **Pronto!** 
   - Ctrl+P → "Analisar nota (Python Compilado)"
```

## Pontos Chave da POC

1. **Zero dependências Python** para o usuário
2. **Executável único** (~15-25MB)
3. **Inicia sob demanda** (não fica sempre rodando)
4. **Usa código existente** do Transcript Analyzer
5. **Instalação = copiar arquivo**

## Build Instructions (Para você)

```bash
# No seu ambiente com o projeto atual
cd transcript-analyser

# Cria o wrapper FastAPI
echo "criar server_wrapper.py com código acima"

# Instala PyInstaller
pip install pyinstaller

# Compila
pyinstaller --onefile --name transcript-analyzer-server \
    --add-data "resources;resources" \
    server_wrapper.py

# Testa o executável
./dist/transcript-analyzer-server

# Em outro terminal
curl -X POST http://localhost:5000/analyze \
    -H "Content-Type: application/json" \
    -d '{"text": "Teste de análise"}'
```

## Critérios de Sucesso

✅ Executável roda sem Python instalado
✅ Plugin detecta e inicia executável
✅ Análise retorna resultados do seu engine atual
✅ Processo fecha quando plugin desativa
✅ Funciona em Windows/Mac/Linux

## Próximos Passos (se POC funcionar)

1. Interface de download automático
2. Progress bar durante análise
3. Dashboard visual dos resultados
4. Integração completa com todas análises



---

Agora sim! O prompt está focado em:

Usar seu código existente - apenas adiciona um wrapper FastAPI
Compilar com PyInstaller - cria executável standalone
Plugin simples - só testa se consegue iniciar e comunicar
Zero dependências - usuário baixa um arquivo e pronto

O mais legal é que você pode testar isso hoje mesmo:

30 min para criar o server_wrapper.py
10 min para compilar com PyInstaller
1h para fazer o plugin básico
Pronto! POC funcionando

Se isso funcionar (e vai funcionar!), aí é só evoluir:

POC → Interface bonita → Download automático → Features completas