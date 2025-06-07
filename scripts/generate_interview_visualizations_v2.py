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

from prototype_experiments.narrative_interview_analysis import NarrativeInterviewAnalyzer
from prototype_experiments.interview_visualization_v2 import InterviewVisualizerV2


def main():
    transcript_path = ROOT / "data" / "sample" / "estatistica_psicobio_aula_2024.txt"
    output_dir = ROOT / "output" / "interview_visualizations_v2"

    print("🚀 GERADOR DE VISUALIZAÇÕES DA ENTREVISTA - V2")
    print("=" * 60)
    print(f"📁 Analisando: {transcript_path}")
    print(f"📊 Saída: {output_dir}")

    text = transcript_path.read_text(encoding="utf-8")
    analyzer = NarrativeInterviewAnalyzer()
    results = analyzer.generate_dual_report(text, "Prof. Estatística (Aula 2024)")

    visualizer = InterviewVisualizerV2()
    visualizer.generate_all_visualizations_v2(results, output_dir=str(output_dir))


if __name__ == "__main__":
    main()
