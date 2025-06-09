# poc_obsidian.py
import sys
import json
from engine.analyzer_core import analyze_text

def analyze_for_obsidian(text):
    """Análise simplificada para POC Obsidian"""
    try:
        # Análise básica
        result = {
            "word_count": len(text.split()),
            "sentiment": "positive" if "bom" in text else "neutral",
            "top_words": ["palavra1", "palavra2", "palavra3"]
        }
        return json.dumps(result)
    except Exception as e:
        return json.dumps({"error": str(e)})

if __name__ == "__main__":
    text = sys.argv[1] if len(sys.argv) > 1 else ""
    print(analyze_for_obsidian(text))