#!/usr/bin/env python3
from pathlib import Path
import os
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
RUNTIME_CACHE = ROOT / ".runtime-cache"
os.environ.setdefault("MPLCONFIGDIR", str(RUNTIME_CACHE / "matplotlib"))
os.environ.setdefault("XDG_CACHE_HOME", str(RUNTIME_CACHE))

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from prototype_experiments.interview_analysis_with_visuals import (
    analyze_interview_with_visuals,
)


def main(input_path=None):
    transcript_path = Path(input_path) if input_path else (
        ROOT / "data" / "sample" / "estatistica_psicobio_aula_2024.txt"
    )
    output_dir = ROOT / "output" / "interview_visualizations_v2"
    participant_name = "Prof. Estatística (Aula 2024)"

    print("🚀 ANALISADOR DE ENTREVISTAS - NARRATIVA + VISUAL")
    print("=" * 60)
    print(f"📁 Analisando: {transcript_path}")
    print(f"👤 Participante: {participant_name}")
    print(f"📊 Saída visual: {output_dir}")
    print()

    result = analyze_interview_with_visuals(
        transcript_path,
        participant_name=participant_name,
        output_dir=output_dir,
        generate_visuals=True,
    )

    if result:
        print("\n✅ Análise concluída com sucesso!")
        print("📄 Relatório textual gerado no terminal")
        print("📊 Visualizações 2.0 salvas em output/interview_visualizations_v2/")
    else:
        print("\n❌ Falha na análise.")


if __name__ == "__main__":
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else None)
