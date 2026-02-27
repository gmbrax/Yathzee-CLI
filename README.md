# Yahtzee CLI

A single-player Yahtzee game running in your terminal, built with [Textual](https://textual.textualize.io/).

## Setup

```bash
pip install -r requirements.txt
python -m yahtzee
```

## How to Play

Yahtzee is a dice game where you score points by rolling five dice to make certain combinations. You get **13 turns**, one for each scoring category.

### Each Turn

1. Press `R` to roll all five dice (up to 3 rolls per turn).
2. After the first roll, click a die to **hold** it — held dice won't be re-rolled.
3. After rolling at least once, click a **scoring category** on the scorecard to commit your score for that turn.

Once a category is used, it's locked for the rest of the game.

### Scoring Categories

| Category | Score |
|---|---|
| Ones – Sixes | Sum of the matching dice |
| Three of a Kind | Sum of all dice (if 3+ match) |
| Four of a Kind | Sum of all dice (if 4+ match) |
| Full House | 25 pts — three of one, two of another |
| Small Straight | 30 pts — any 4 sequential values |
| Large Straight | 40 pts — 5 sequential values (1–5 or 2–6) |
| Yahtzee | 50 pts — all five dice match |
| Chance | Sum of all dice, no conditions |

**Upper section bonus:** Score 63+ points in the Ones–Sixes categories to earn a **35-point bonus**.

### Keybindings

| Key | Action |
|---|---|
| `R` | Roll dice |
| `N` | New game |
| `Q` | Quit |
