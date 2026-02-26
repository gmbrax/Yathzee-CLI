"""Unit tests for the GameState class (game.py)."""

import pytest
from game import GameState, ALL_CATEGORIES, UPPER_CATEGORIES


# ---------------------------------------------------------------------------
# Initialization
# ---------------------------------------------------------------------------

class TestInit:
    def test_dice_all_zero(self):
        gs = GameState()
        assert gs.dice == [0, 0, 0, 0, 0]

    def test_held_all_false(self):
        gs = GameState()
        assert gs.held == [False, False, False, False, False]

    def test_roll_count_zero(self):
        gs = GameState()
        assert gs.roll_count == 0

    def test_scores_all_none(self):
        gs = GameState()
        assert all(v is None for v in gs.scores.values())

    def test_scores_has_all_13_categories(self):
        gs = GameState()
        assert set(gs.scores.keys()) == set(ALL_CATEGORIES)

    def test_game_over_false(self):
        gs = GameState()
        assert gs.game_over is False


# ---------------------------------------------------------------------------
# roll()
# ---------------------------------------------------------------------------

class TestRoll:
    def test_first_roll_randomizes_all_dice(self):
        gs = GameState()
        gs.roll()
        assert gs.roll_count == 1
        assert all(1 <= d <= 6 for d in gs.dice)

    def test_roll_increments_count(self):
        gs = GameState()
        gs.roll()
        assert gs.roll_count == 1
        gs.roll()
        assert gs.roll_count == 2
        gs.roll()
        assert gs.roll_count == 3

    def test_roll_noop_at_three(self):
        gs = GameState()
        gs.roll()
        gs.roll()
        gs.roll()
        dice_snapshot = gs.dice[:]
        gs.roll()  # should be a no-op
        assert gs.roll_count == 3
        assert gs.dice == dice_snapshot

    def test_held_dice_not_rerolled(self):
        gs = GameState()
        gs.roll()
        # Force a known die value and hold it
        gs.dice[2] = 6
        gs.held[2] = True
        gs.roll()
        assert gs.dice[2] == 6

    def test_unheld_dice_may_change_on_reroll(self):
        # Statistical: with enough tries at least one unheld die should change.
        # We force all dice to 1, hold none, reroll — values should be 1–6.
        gs = GameState()
        gs.roll()
        gs.dice = [1, 1, 1, 1, 1]
        gs.roll()
        # All dice must still be valid
        assert all(1 <= d <= 6 for d in gs.dice)


# ---------------------------------------------------------------------------
# toggle_hold()
# ---------------------------------------------------------------------------

class TestToggleHold:
    def test_toggle_before_first_roll_has_no_effect(self):
        gs = GameState()
        gs.toggle_hold(0)
        assert gs.held[0] is False

    def test_toggle_after_roll_flips_held(self):
        gs = GameState()
        gs.roll()
        gs.toggle_hold(0)
        assert gs.held[0] is True

    def test_toggle_twice_restores_original(self):
        gs = GameState()
        gs.roll()
        gs.toggle_hold(3)
        gs.toggle_hold(3)
        assert gs.held[3] is False

    def test_toggle_each_index(self):
        gs = GameState()
        gs.roll()
        for i in range(5):
            gs.toggle_hold(i)
        assert gs.held == [True, True, True, True, True]


# ---------------------------------------------------------------------------
# commit()
# ---------------------------------------------------------------------------

class TestCommit:
    def _state_after_roll(self, dice=None):
        gs = GameState()
        gs.roll()
        if dice is not None:
            gs.dice = dice
        return gs

    def test_commit_stores_score(self):
        gs = self._state_after_roll([1, 1, 1, 1, 1])
        gs.commit("ones")
        assert gs.scores["ones"] == 5  # five 1s

    def test_commit_resets_dice(self):
        gs = self._state_after_roll([3, 3, 3, 3, 3])
        gs.commit("chance")
        assert gs.dice == [0, 0, 0, 0, 0]

    def test_commit_resets_held(self):
        gs = self._state_after_roll()
        gs.toggle_hold(0)
        gs.commit("chance")
        assert gs.held == [False, False, False, False, False]

    def test_commit_resets_roll_count(self):
        gs = self._state_after_roll()
        gs.commit("chance")
        assert gs.roll_count == 0

    def test_commit_raises_if_already_committed(self):
        gs = self._state_after_roll([1, 1, 1, 1, 1])
        gs.commit("ones")
        gs.roll()
        with pytest.raises(ValueError):
            gs.commit("ones")

    def test_commit_raises_if_roll_count_zero(self):
        gs = GameState()
        with pytest.raises(ValueError):
            gs.commit("ones")

    def test_commit_raises_for_unknown_category(self):
        gs = self._state_after_roll()
        with pytest.raises((ValueError, KeyError)):
            gs.commit("not_a_category")

    def test_commit_chance_scores_sum(self):
        gs = self._state_after_roll([2, 3, 4, 5, 6])
        gs.commit("chance")
        assert gs.scores["chance"] == 20

    def test_commit_full_house_scores_25(self):
        gs = self._state_after_roll([2, 2, 3, 3, 3])
        gs.commit("full_house")
        assert gs.scores["full_house"] == 25

    def test_commit_yahtzee_scores_50(self):
        gs = self._state_after_roll([4, 4, 4, 4, 4])
        gs.commit("yahtzee")
        assert gs.scores["yahtzee"] == 50


# ---------------------------------------------------------------------------
# reset()
# ---------------------------------------------------------------------------

class TestReset:
    def test_reset_clears_dice(self):
        gs = GameState()
        gs.roll()
        gs.reset()
        assert gs.dice == [0, 0, 0, 0, 0]

    def test_reset_clears_held(self):
        gs = GameState()
        gs.roll()
        gs.toggle_hold(1)
        gs.reset()
        assert gs.held == [False, False, False, False, False]

    def test_reset_clears_roll_count(self):
        gs = GameState()
        gs.roll()
        gs.roll()
        gs.reset()
        assert gs.roll_count == 0

    def test_reset_clears_scores(self):
        gs = GameState()
        gs.roll()
        gs.commit("chance")
        gs.reset()
        assert all(v is None for v in gs.scores.values())

    def test_reset_clears_game_over(self):
        gs = GameState()
        gs.game_over = True
        gs.reset()
        assert gs.game_over is False


# ---------------------------------------------------------------------------
# upper_subtotal property
# ---------------------------------------------------------------------------

class TestUpperSubtotal:
    def test_zero_when_nothing_committed(self):
        gs = GameState()
        assert gs.upper_subtotal == 0

    def test_sums_only_committed_upper_categories(self):
        gs = GameState()
        gs.roll()
        gs.dice = [1, 1, 1, 1, 1]
        gs.commit("ones")   # scores 5
        gs.roll()
        gs.dice = [2, 2, 2, 2, 2]
        gs.commit("twos")   # scores 10
        assert gs.upper_subtotal == 15

    def test_ignores_lower_categories(self):
        gs = GameState()
        gs.roll()
        gs.dice = [1, 2, 3, 4, 5]
        gs.commit("chance")  # lower category
        assert gs.upper_subtotal == 0


# ---------------------------------------------------------------------------
# bonus property
# ---------------------------------------------------------------------------

class TestBonus:
    def test_no_bonus_below_63(self):
        gs = GameState()
        gs.roll()
        gs.dice = [1, 1, 1, 1, 1]
        gs.commit("ones")  # 5 points
        assert gs.bonus == 0

    def test_bonus_35_at_exactly_63(self):
        gs = GameState()
        # Commit upper categories summing to exactly 63: 3+6+9+12+15+18=63
        data = [
            ("ones",   [1, 1, 1, 0, 0]),   # 3
            ("twos",   [2, 2, 2, 0, 0]),   # 6
            ("threes", [3, 3, 3, 0, 0]),   # 9
            ("fours",  [4, 4, 4, 0, 0]),   # 12
            ("fives",  [5, 5, 5, 0, 0]),   # 15
            ("sixes",  [6, 6, 6, 0, 0]),   # 18
        ]
        for cat, dice in data:
            gs.roll()
            gs.dice = dice
            gs.commit(cat)
        assert gs.upper_subtotal == 63
        assert gs.bonus == 35

    def test_bonus_35_above_63(self):
        gs = GameState()
        # All upper categories with max values: 5+10+15+20+25+30 = 105
        data = [
            ("ones",   [1, 1, 1, 1, 1]),   # 5
            ("twos",   [2, 2, 2, 2, 2]),   # 10
            ("threes", [3, 3, 3, 3, 3]),   # 15
            ("fours",  [4, 4, 4, 4, 4]),   # 20
            ("fives",  [5, 5, 5, 5, 5]),   # 25
            ("sixes",  [6, 6, 6, 6, 6]),   # 30
        ]
        for cat, dice in data:
            gs.roll()
            gs.dice = dice
            gs.commit(cat)
        assert gs.bonus == 35


# ---------------------------------------------------------------------------
# grand_total property
# ---------------------------------------------------------------------------

class TestGrandTotal:
    def test_zero_initially(self):
        gs = GameState()
        assert gs.grand_total == 0

    def test_sums_committed_scores(self):
        gs = GameState()
        gs.roll()
        gs.dice = [1, 1, 1, 1, 1]
        gs.commit("ones")   # 5
        gs.roll()
        gs.dice = [2, 2, 2, 2, 2]
        gs.commit("chance") # 10
        assert gs.grand_total == 15

    def test_includes_bonus(self):
        gs = GameState()
        data = [
            ("ones",   [1, 1, 1, 1, 1]),   # 5
            ("twos",   [2, 2, 2, 2, 2]),   # 10
            ("threes", [3, 3, 3, 3, 3]),   # 15
            ("fours",  [4, 4, 4, 4, 4]),   # 20
            ("fives",  [5, 5, 5, 5, 5]),   # 25
            ("sixes",  [6, 6, 6, 6, 6]),   # 30
        ]
        for cat, dice in data:
            gs.roll()
            gs.dice = dice
            gs.commit(cat)
        # upper sum = 105, bonus = 35, grand_total = 140
        assert gs.grand_total == 140


# ---------------------------------------------------------------------------
# is_game_over property
# ---------------------------------------------------------------------------

class TestIsGameOver:
    def test_false_initially(self):
        gs = GameState()
        assert gs.is_game_over is False

    def test_false_with_some_categories_committed(self):
        gs = GameState()
        gs.roll()
        gs.commit("chance")
        assert gs.is_game_over is False

    def test_true_when_all_13_committed(self):
        gs = GameState()
        dice_sets = {
            "ones":           [1, 1, 1, 1, 1],
            "twos":           [2, 2, 2, 2, 2],
            "threes":         [3, 3, 3, 3, 3],
            "fours":          [4, 4, 4, 4, 4],
            "fives":          [5, 5, 5, 5, 5],
            "sixes":          [6, 6, 6, 6, 6],
            "three_of_a_kind":[3, 3, 3, 1, 2],
            "four_of_a_kind": [4, 4, 4, 4, 1],
            "full_house":     [2, 2, 3, 3, 3],
            "small_straight": [1, 2, 3, 4, 6],
            "large_straight": [1, 2, 3, 4, 5],
            "yahtzee":        [5, 5, 5, 5, 5],
            "chance":         [1, 2, 3, 4, 5],
        }
        for cat in ALL_CATEGORIES:
            gs.roll()
            gs.dice = dice_sets[cat]
            gs.commit(cat)
        assert gs.is_game_over is True

    def test_game_over_flag_set_after_last_commit(self):
        gs = GameState()
        dice_sets = {
            "ones":           [1, 1, 1, 1, 1],
            "twos":           [2, 2, 2, 2, 2],
            "threes":         [3, 3, 3, 3, 3],
            "fours":          [4, 4, 4, 4, 4],
            "fives":          [5, 5, 5, 5, 5],
            "sixes":          [6, 6, 6, 6, 6],
            "three_of_a_kind":[3, 3, 3, 1, 2],
            "four_of_a_kind": [4, 4, 4, 4, 1],
            "full_house":     [2, 2, 3, 3, 3],
            "small_straight": [1, 2, 3, 4, 6],
            "large_straight": [1, 2, 3, 4, 5],
            "yahtzee":        [5, 5, 5, 5, 5],
            "chance":         [1, 2, 3, 4, 5],
        }
        for cat in ALL_CATEGORIES:
            gs.roll()
            gs.dice = dice_sets[cat]
            gs.commit(cat)
        assert gs.game_over is True
