from pathlib import Path

from prototype_experiments.narrative_interview_analysis import NarrativeInterviewAnalyzer
from prototype_experiments.interview_visualization_v2 import InterviewVisualizerV2


def analyze_interview_with_visuals(
    transcript_path,
    participant_name=None,
    output_dir=None,
    generate_visuals=True,
):
    transcript_path = Path(transcript_path)
    text = transcript_path.read_text(encoding="utf-8")

    if participant_name is None:
        participant_name = transcript_path.stem.replace("_", " ").title()

    analyzer = NarrativeInterviewAnalyzer()
    results = analyzer.generate_dual_report(text, participant_name)

    if generate_visuals and results:
        print("\n" + "=" * 60)
        print("🎨 INICIANDO GERAÇÃO DE VISUALIZAÇÕES 2.0")
        print("=" * 60)

        visualizer = InterviewVisualizerV2()
        visualizer.generate_all_visualizations_v2(results, output_dir=str(output_dir))

    return results
