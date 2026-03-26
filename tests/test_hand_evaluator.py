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
