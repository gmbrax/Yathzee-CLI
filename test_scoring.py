"""
Unit tests for the Yahtzee scoring module.
"""

import pytest
from scoring import (
    ones, twos, threes, fours, fives, sixes,
    three_of_a_kind, four_of_a_kind, full_house,
    small_straight, large_straight, yahtzee, chance,
)


# ── Upper section ─────────────────────────────────────────────────────────────

class TestOnes:
    def test_all_ones(self):
        assert ones([1, 1, 1, 1, 1]) == 5

    def test_some_ones(self):
        assert ones([1, 2, 1, 3, 4]) == 2

    def test_no_ones(self):
        assert ones([2, 3, 4, 5, 6]) == 0

    def test_single_one(self):
        assert ones([1, 2, 3, 4, 5]) == 1


class TestTwos:
    def test_all_twos(self):
        assert twos([2, 2, 2, 2, 2]) == 10

    def test_some_twos(self):
        assert twos([2, 2, 1, 3, 4]) == 4

    def test_no_twos(self):
        assert twos([1, 3, 4, 5, 6]) == 0


class TestThrees:
    def test_all_threes(self):
        assert threes([3, 3, 3, 3, 3]) == 15

    def test_some_threes(self):
        assert threes([3, 3, 1, 2, 5]) == 6

    def test_no_threes(self):
        assert threes([1, 2, 4, 5, 6]) == 0


class TestFours:
    def test_all_fours(self):
        assert fours([4, 4, 4, 4, 4]) == 20

    def test_some_fours(self):
        assert fours([4, 4, 1, 2, 5]) == 8

    def test_no_fours(self):
        assert fours([1, 2, 3, 5, 6]) == 0


class TestFives:
    def test_all_fives(self):
        assert fives([5, 5, 5, 5, 5]) == 25

    def test_some_fives(self):
        assert fives([5, 5, 1, 2, 3]) == 10

    def test_no_fives(self):
        assert fives([1, 2, 3, 4, 6]) == 0


class TestSixes:
    def test_all_sixes(self):
        assert sixes([6, 6, 6, 6, 6]) == 30

    def test_some_sixes(self):
        assert sixes([6, 6, 1, 2, 3]) == 12

    def test_no_sixes(self):
        assert sixes([1, 2, 3, 4, 5]) == 0


# ── Lower section ─────────────────────────────────────────────────────────────

class TestThreeOfAKind:
    def test_exactly_three(self):
        assert three_of_a_kind([3, 3, 3, 1, 2]) == 12

    def test_four_qualifies(self):
        assert three_of_a_kind([4, 4, 4, 4, 2]) == 18

    def test_five_qualifies(self):
        assert three_of_a_kind([5, 5, 5, 5, 5]) == 25

    def test_no_match(self):
        assert three_of_a_kind([1, 2, 3, 4, 5]) == 0

    def test_only_pairs(self):
        assert three_of_a_kind([1, 1, 2, 2, 3]) == 0


class TestFourOfAKind:
    def test_exactly_four(self):
        assert four_of_a_kind([2, 2, 2, 2, 5]) == 13

    def test_five_qualifies(self):
        assert four_of_a_kind([6, 6, 6, 6, 6]) == 30

    def test_three_does_not_qualify(self):
        assert four_of_a_kind([3, 3, 3, 1, 2]) == 0

    def test_no_match(self):
        assert four_of_a_kind([1, 2, 3, 4, 5]) == 0


class TestFullHouse:
    def test_valid_full_house(self):
        assert full_house([2, 2, 3, 3, 3]) == 25

    def test_valid_full_house_reversed(self):
        assert full_house([5, 5, 5, 4, 4]) == 25

    def test_five_of_a_kind_not_full_house(self):
        assert full_house([1, 1, 1, 1, 1]) == 0

    def test_three_of_a_kind_only(self):
        assert full_house([3, 3, 3, 1, 2]) == 0

    def test_two_pairs_not_full_house(self):
        assert full_house([1, 1, 2, 2, 3]) == 0


class TestSmallStraight:
    def test_1234(self):
        assert small_straight([1, 2, 3, 4, 6]) == 30

    def test_2345(self):
        assert small_straight([2, 3, 4, 5, 1]) == 30

    def test_3456(self):
        assert small_straight([3, 4, 5, 6, 2]) == 30

    def test_full_straight_counts(self):
        assert small_straight([1, 2, 3, 4, 5]) == 30

    def test_no_straight(self):
        assert small_straight([1, 1, 2, 2, 3]) == 0

    def test_gap_in_sequence(self):
        assert small_straight([1, 2, 4, 5, 6]) == 0

    def test_with_duplicates_still_qualifies(self):
        assert small_straight([1, 2, 3, 3, 4]) == 30


class TestLargeStraight:
    def test_12345(self):
        assert large_straight([1, 2, 3, 4, 5]) == 40

    def test_23456(self):
        assert large_straight([2, 3, 4, 5, 6]) == 40

    def test_small_straight_not_large(self):
        assert large_straight([1, 2, 3, 4, 6]) == 0

    def test_duplicate_not_large(self):
        assert large_straight([1, 2, 3, 4, 4]) == 0

    def test_no_straight(self):
        assert large_straight([1, 1, 2, 2, 3]) == 0


class TestYahtzee:
    def test_all_same(self):
        assert yahtzee([1, 1, 1, 1, 1]) == 50

    def test_all_sixes(self):
        assert yahtzee([6, 6, 6, 6, 6]) == 50

    def test_four_of_a_kind_not_yahtzee(self):
        assert yahtzee([1, 1, 1, 1, 2]) == 0

    def test_mixed(self):
        assert yahtzee([1, 2, 3, 4, 5]) == 0


class TestChance:
    def test_all_ones(self):
        assert chance([1, 1, 1, 1, 1]) == 5

    def test_all_sixes(self):
        assert chance([6, 6, 6, 6, 6]) == 30

    def test_mixed(self):
        assert chance([1, 2, 3, 4, 5]) == 15

    def test_max_chance(self):
        assert chance([6, 6, 6, 6, 6]) == 30

    def test_min_chance(self):
        assert chance([1, 1, 1, 1, 1]) == 5

    def test_arbitrary(self):
        assert chance([3, 3, 3, 3, 3]) == 15
