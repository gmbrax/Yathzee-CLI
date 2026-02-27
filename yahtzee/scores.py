import json
import sys
from datetime import date
from pathlib import Path

SCORES_FILE = Path.home() / ".local" / "share" / "yahtzee" / "scores.json"


def load_scores() -> list[dict]:
    if not SCORES_FILE.exists():
        return []
    try:
        data = json.loads(SCORES_FILE.read_text(encoding="utf-8"))
        return data["scores"]
    except Exception as e:
        print(f"Warning: could not load scores: {e}", file=sys.stderr)
        return []


def save_score(name: str, score: int) -> None:
    scores = load_scores()
    scores.append({"name": name, "score": score, "date": date.today().strftime("%Y-%m-%d")})
    SCORES_FILE.parent.mkdir(parents=True, exist_ok=True)
    SCORES_FILE.write_text(json.dumps({"scores": scores}, indent=2), encoding="utf-8")


def get_top_10() -> list[dict]:
    return sorted(load_scores(), key=lambda e: e["score"], reverse=True)[:10]
