# Criar wrapper simplificado
cat > obsidian_server.py << 'EOF'
from fastapi import FastAPI
from engine.analyzer_core import TranscriptAnalyzer
import uvicorn

app = FastAPI()

@app.post("/analyze-simple")
async def analyze(data: dict):
    analyzer = TranscriptAnalyzer({})
    result = analyzer.analyze(data['text'])
    return {
        "sentiment": result.get('sentiment_global', 0),
        "words": result.get('word_count', 0)
    }

if __name__ == "__main__":
    uvicorn.run(app, port=5000)
EOF

# Compilar
pyinstaller --onefile obsidian_server.py