"""
Pure-function scoring module for Yahtzee.

Each function accepts a list of 5 integers (die values 1–6) and returns an integer score.
"""

from collections import Counter


def ones(dice: list[int]) -> int:
    """Return the sum of dice showing 1."""
    return sum(d for d in dice if d == 1)


def twos(dice: list[int]) -> int:
    """Return the sum of dice showing 2."""
    return sum(d for d in dice if d == 2)


def threes(dice: list[int]) -> int:
    """Return the sum of dice showing 3."""
    return sum(d for d in dice if d == 3)


def fours(dice: list[int]) -> int:
    """Return the sum of dice showing 4."""
    return sum(d for d in dice if d == 4)


def fives(dice: list[int]) -> int:
    """Return the sum of dice showing 5."""
    return sum(d for d in dice if d == 5)


def sixes(dice: list[int]) -> int:
    """Return the sum of dice showing 6."""
    return sum(d for d in dice if d == 6)


def three_of_a_kind(dice: list[int]) -> int:
    """Return sum of all 5 dice if any value appears >= 3 times, else 0."""
    counts = Counter(dice)
    if any(v >= 3 for v in counts.values()):
        return sum(dice)
    return 0


def four_of_a_kind(dice: list[int]) -> int:
    """Return sum of all 5 dice if any value appears >= 4 times, else 0."""
    counts = Counter(dice)
    if any(v >= 4 for v in counts.values()):
        return sum(dice)
    return 0


def full_house(dice: list[int]) -> int:
    """Return 25 if dice contain exactly three of one value and two of another, else 0."""
    counts = Counter(dice)
    if sorted(counts.values()) == [2, 3]:
        return 25
    return 0


def small_straight(dice: list[int]) -> int:
    """Return 30 if dice contain any 4 sequential values, else 0."""
    unique = set(dice)
    straights = [{1, 2, 3, 4}, {2, 3, 4, 5}, {3, 4, 5, 6}]
    if any(s.issubset(unique) for s in straights):
        return 30
    return 0


def large_straight(dice: list[int]) -> int:
    """Return 40 if dice are exactly 1-2-3-4-5 or 2-3-4-5-6, else 0."""
    unique = set(dice)
    if unique in [{1, 2, 3, 4, 5}, {2, 3, 4, 5, 6}]:
        return 40
    return 0


def yahtzee(dice: list[int]) -> int:
    """Return 50 if all 5 dice show the same value, else 0."""
    if len(set(dice)) == 1:
        return 50
    return 0


def chance(dice: list[int]) -> int:
    """Return sum of all 5 dice, always."""
    return sum(dice)
