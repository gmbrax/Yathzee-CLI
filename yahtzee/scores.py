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
        raw = data["scores"] if isinstance(data, dict) else []
        if not isinstance(raw, list):
            raw = []
        cleaned = []
        for entry in raw:
            if not isinstance(entry, dict):
                print(f"Warning: skipping non-dict score entry: {entry!r}", file=sys.stderr)
                continue
            raw_score = entry.get("score")
            if raw_score is None:
                print(f"Warning: skipping entry missing 'score': {entry!r}", file=sys.stderr)
                continue
            try:
                entry = {**entry, "score": int(raw_score)}
            except (ValueError, TypeError):
                try:
                    entry = {**entry, "score": float(raw_score)}
                except (ValueError, TypeError):
                    print(f"Warning: skipping entry with non-numeric score: {entry!r}", file=sys.stderr)
                    continue
            cleaned.append(entry)
        return cleaned
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
