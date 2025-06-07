#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from prototype_experiments.transcript_comparison import main


if __name__ == "__main__":
    main([Path(arg) for arg in sys.argv[1:]] or None)

