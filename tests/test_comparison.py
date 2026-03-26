import pytest
from poker.card import Card
from poker.hand_evaluator import HandEvaluator, HandRank


class TestHandComparison:
    """Tests pour la comparaison de mains de catégories différentes"""

    def test_straight_flush_beats_four_of_a_kind(self):
        sf = HandEvaluator.evaluate([Card('9', '♠'), Card('8', '♠'), Card('7', '♠'), Card('6', '♠'), Card('5', '♠')])
        quad = HandEvaluator.evaluate([Card('A', '♠'), Card('A', '♥'), Card('A', '♦'), Card('A', '♣'), Card('K', '♠')])
        assert sf > quad

    def test_four_of_a_kind_beats_full_house(self):
        quad = HandEvaluator.evaluate([Card('3', '♠'), Card('3', '♥'), Card('3', '♦'), Card('3', '♣'), Card('Q', '♠')])
        fh = HandEvaluator.evaluate([Card('A', '♠'), Card('A', '♥'), Card('A', '♦'), Card('K', '♣'), Card('K', '♠')])
        assert quad > fh

    def test_full_house_beats_flush(self):
        fh = HandEvaluator.evaluate([Card('3', '♠'), Card('3', '♥'), Card('3', '♦'), Card('Q', '♣'), Card('Q', '♠')])
        flush = HandEvaluator.evaluate([Card('A', '♠'), Card('J', '♠'), Card('8', '♠'), Card('5', '♠'), Card('3', '♠')])
        assert fh > flush

    def test_flush_beats_straight(self):
        flush = HandEvaluator.evaluate([Card('A', '♠'), Card('J', '♠'), Card('8', '♠'), Card('5', '♠'), Card('3', '♠')])
        straight = HandEvaluator.evaluate([Card('9', '♠'), Card('8', '♥'), Card('7', '♦'), Card('6', '♣'), Card('5', '♠')])
        assert flush > straight

    def test_straight_beats_three_of_a_kind(self):
        straight = HandEvaluator.evaluate([Card('9', '♠'), Card('8', '♥'), Card('7', '♦'), Card('6', '♣'), Card('5', '♠')])
        trips = HandEvaluator.evaluate([Card('A', '♠'), Card('A', '♥'), Card('A', '♦'), Card('K', '♣'), Card('3', '♠')])
        assert straight > trips

    def test_three_of_a_kind_beats_two_pair(self):
        trips = HandEvaluator.evaluate([Card('3', '♠'), Card('3', '♥'), Card('3', '♦'), Card('K', '♣'), Card('Q', '♠')])
        two_pair = HandEvaluator.evaluate([Card('A', '♠'), Card('A', '♥'), Card('K', '♦'), Card('K', '♣'), Card('3', '♠')])
        assert trips > two_pair

    def test_two_pair_beats_one_pair(self):
        two_pair = HandEvaluator.evaluate([Card('9', '♠'), Card('9', '♥'), Card('5', '♦'), Card('5', '♣'), Card('2', '♠')])
        one_pair = HandEvaluator.evaluate([Card('A', '♠'), Card('A', '♥'), Card('K', '♦'), Card('8', '♣'), Card('3', '♠')])
        assert two_pair > one_pair

    def test_one_pair_beats_high_card(self):
        one_pair = HandEvaluator.evaluate([Card('2', '♠'), Card('2', '♥'), Card('K', '♦'), Card('8', '♣'), Card('3', '♠')])
        high_card = HandEvaluator.evaluate([Card('A', '♠'), Card('K', '♥'), Card('Q', '♦'), Card('J', '♣'), Card('9', '♠')])
        assert one_pair > high_card


class TestTiebreakers:
    """Tests pour les règles de départage"""

    def test_straight_compare_high_card(self):
        """Suite: compare la carte la plus haute"""
        high = HandEvaluator.evaluate([Card('9', '♠'), Card('8', '♥'), Card('7', '♦'), Card('6', '♣'), Card('5', '♠')])
        low = HandEvaluator.evaluate([Card('7', '♠'), Card('6', '♥'), Card('5', '♦'), Card('4', '♣'), Card('3', '♠')])
        assert high > low

    def test_four_of_a_kind_compare_quad_then_kicker(self):
        """Carré: compare le rang du carré, puis le kicker"""
        high_quad = HandEvaluator.evaluate([Card('K', '♠'), Card('K', '♥'), Card('K', '♦'), Card('K', '♣'), Card('2', '♠')])
        low_quad = HandEvaluator.evaluate([Card('3', '♠'), Card('3', '♥'), Card('3', '♦'), Card('3', '♣'), Card('A', '♠')])
        assert high_quad > low_quad

        # Même carré, kicker différent
        high_kicker = HandEvaluator.evaluate([Card('K', '♠'), Card('K', '♥'), Card('K', '♦'), Card('K', '♣'), Card('A', '♠')])
        low_kicker = HandEvaluator.evaluate([Card('K', '♠'), Card('K', '♥'), Card('K', '♦'), Card('K', '♣'), Card('2', '♠')])
        assert high_kicker > low_kicker

    def test_full_house_compare_trips_then_pair(self):
        """Full house: compare le brelan, puis la paire"""
        high_trips = HandEvaluator.evaluate([Card('K', '♠'), Card('K', '♥'), Card('K', '♦'), Card('2', '♣'), Card('2', '♠')])
        low_trips = HandEvaluator.evaluate([Card('3', '♠'), Card('3', '♥'), Card('3', '♦'), Card('A', '♣'), Card('A', '♠')])
        assert high_trips > low_trips

        # Même brelan, paire différente
        high_pair = HandEvaluator.evaluate([Card('K', '♠'), Card('K', '♥'), Card('K', '♦'), Card('Q', '♣'), Card('Q', '♠')])
        low_pair = HandEvaluator.evaluate([Card('K', '♠'), Card('K', '♥'), Card('K', '♦'), Card('2', '♣'), Card('2', '♠')])
        assert high_pair > low_pair

    def test_flush_compare_all_cards(self):
        """Couleur: compare les 5 cartes en ordre décroissant"""
        high = HandEvaluator.evaluate([Card('A', '♠'), Card('J', '♠'), Card('8', '♠'), Card('5', '♠'), Card('3', '♠')])
        low = HandEvaluator.evaluate([Card('K', '♠'), Card('Q', '♠'), Card('9', '♠'), Card('7', '♠'), Card('2', '♠')])
        assert high > low

    def test_three_of_a_kind_compare_trips_then_kickers(self):
        """Brelan: compare le brelan, puis les 2 kickers"""
        high_trips = HandEvaluator.evaluate([Card('K', '♠'), Card('K', '♥'), Card('K', '♦'), Card('2', '♣'), Card('3', '♠')])
        low_trips = HandEvaluator.evaluate([Card('3', '♠'), Card('3', '♥'), Card('3', '♦'), Card('A', '♣'), Card('K', '♠')])
        assert high_trips > low_trips

        # Même brelan, kickers différents
        high_kicker = HandEvaluator.evaluate([Card('K', '♠'), Card('K', '♥'), Card('K', '♦'), Card('A', '♣'), Card('Q', '♠')])
        low_kicker = HandEvaluator.evaluate([Card('K', '♠'), Card('K', '♥'), Card('K', '♦'), Card('2', '♣'), Card('3', '♠')])
        assert high_kicker > low_kicker

    def test_two_pair_compare_high_low_kicker(self):
        """Deux paires: compare paire haute, paire basse, kicker"""
        high_pair = HandEvaluator.evaluate([Card('A', '♠'), Card('A', '♥'), Card('3', '♦'), Card('3', '♣'), Card('2', '♠')])
        low_pair = HandEvaluator.evaluate([Card('K', '♠'), Card('K', '♥'), Card('Q', '♦'), Card('Q', '♣'), Card('A', '♠')])
        assert high_pair > low_pair

    def test_one_pair_compare_pair_then_kickers(self):
        """Une paire: compare la paire, puis les 3 kickers"""
        high_pair = HandEvaluator.evaluate([Card('A', '♠'), Card('A', '♥'), Card('2', '♦'), Card('3', '♣'), Card('4', '♠')])
        low_pair = HandEvaluator.evaluate([Card('K', '♠'), Card('K', '♥'), Card('A', '♦'), Card('Q', '♣'), Card('J', '♠')])
        assert high_pair > low_pair

    def test_high_card_compare_all_cards(self):
        """Carte haute: compare les 5 cartes en ordre décroissant"""
        high = HandEvaluator.evaluate([Card('A', '♠'), Card('K', '♥'), Card('Q', '♦'), Card('J', '♣'), Card('9', '♠')])
        low = HandEvaluator.evaluate([Card('A', '♠'), Card('K', '♥'), Card('Q', '♦'), Card('J', '♣'), Card('8', '♠')])
        assert high > low

    def test_tie_all_equal(self):
        """Égalité parfaite"""
        hand1 = HandEvaluator.evaluate([Card('A', '♠'), Card('K', '♥'), Card('Q', '♦'), Card('J', '♣'), Card('9', '♠')])
        hand2 = HandEvaluator.evaluate([Card('A', '♥'), Card('K', '♦'), Card('Q', '♣'), Card('J', '♠'), Card('9', '♥')])
        assert hand1 == hand2
