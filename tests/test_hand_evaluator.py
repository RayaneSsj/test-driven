import pytest
from poker.card import Card
from poker.hand_evaluator import HandEvaluator, HandRank


class TestHighCard:
    """Tests pour la détection de High Card"""

    def test_high_card_detection(self):
        """Test détection d'une main High Card basique"""
        cards = [
            Card('A', '♠'),
            Card('K', '♥'),
            Card('8', '♦'),
            Card('5', '♣'),
            Card('3', '♠')
        ]
        result = HandEvaluator.evaluate(cards)
        assert result.rank == HandRank.HIGH_CARD
        assert result.rank_name == "High Card"

    def test_high_card_with_different_values(self):
        """Test High Card avec différentes valeurs"""
        cards = [
            Card('J', '♠'),
            Card('9', '♥'),
            Card('7', '♦'),
            Card('4', '♣'),
            Card('2', '♠')
        ]
        result = HandEvaluator.evaluate(cards)
        assert result.rank == HandRank.HIGH_CARD

    def test_high_card_identifies_highest_card(self):
        """Test que High Card identifie correctement la carte la plus haute"""
        cards = [
            Card('Q', '♠'),
            Card('10', '♥'),
            Card('8', '♦'),
            Card('6', '♣'),
            Card('3', '♠')
        ]
        result = HandEvaluator.evaluate(cards)
        assert result.rank == HandRank.HIGH_CARD
        # La carte la plus haute devrait être la Dame
        assert result.cards[0].value == 'Q'


class TestOnePair:
    """Tests pour la détection de One Pair"""

    def test_one_pair_detection(self):
        """Test détection d'une paire"""
        cards = [
            Card('A', '♠'),
            Card('A', '♥'),
            Card('K', '♦'),
            Card('8', '♣'),
            Card('3', '♠')
        ]
        result = HandEvaluator.evaluate(cards)
        assert result.rank == HandRank.ONE_PAIR
        assert result.rank_name == "One Pair"

    def test_one_pair_with_low_pair(self):
        """Test paire avec des cartes basses"""
        cards = [
            Card('K', '♠'),
            Card('Q', '♥'),
            Card('7', '♦'),
            Card('5', '♣'),
            Card('5', '♠')
        ]
        result = HandEvaluator.evaluate(cards)
        assert result.rank == HandRank.ONE_PAIR

    def test_one_pair_identifies_pair_value(self):
        """Test que la paire est identifiée correctement"""
        cards = [
            Card('J', '♠'),
            Card('J', '♥'),
            Card('9', '♦'),
            Card('4', '♣'),
            Card('2', '♠')
        ]
        result = HandEvaluator.evaluate(cards)
        assert result.rank == HandRank.ONE_PAIR
        # Les deux premières cartes devraient être la paire de Valets
        assert result.cards[0].value == 'J'
        assert result.cards[1].value == 'J'

    def test_not_one_pair_when_high_card(self):
        """Test qu'une High Card n'est pas détectée comme paire"""
        cards = [
            Card('A', '♠'),
            Card('K', '♥'),
            Card('Q', '♦'),
            Card('J', '♣'),
            Card('9', '♠')
        ]
        result = HandEvaluator.evaluate(cards)
        assert result.rank != HandRank.ONE_PAIR
        assert result.rank == HandRank.HIGH_CARD
