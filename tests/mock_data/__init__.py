import json
from pathlib import Path

def load_mock_result(filename: str = "default") -> dict:
    """Carrega resultado mockado para testes"""
    mock_dir = Path(__file__).parent
    mock_file = mock_dir / "complete_analysis_result.json"
    
    with open(mock_file, 'r', encoding='utf-8') as f:
        result = json.load(f)
    
    # Personaliza o filename
    result['filename'] = filename
    return result