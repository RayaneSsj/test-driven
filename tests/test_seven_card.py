import pytest
from poker.card import Card
from poker.hand_evaluator import HandEvaluator, HandRank
from poker.seven_card_evaluator import SevenCardEvaluator


class TestSevenCardEvaluator:
    """Tests pour l'évaluation de 7 cartes (trouver la meilleure main de 5)"""

    def test_seven_cards_finds_straight_flush(self):
        """Trouve une quinte flush parmi 7 cartes"""
        cards = [
            Card('9', '♠'), Card('8', '♠'), Card('7', '♠'),
            Card('6', '♠'), Card('5', '♠'), Card('A', '♥'), Card('K', '♦')
        ]
        result = SevenCardEvaluator.best_hand(cards)
        assert result.rank == HandRank.STRAIGHT_FLUSH
        assert len(result.cards) == 5

    def test_seven_cards_finds_four_of_a_kind(self):
        """Trouve un carré parmi 7 cartes"""
        cards = [
            Card('K', '♠'), Card('K', '♥'), Card('K', '♦'),
            Card('K', '♣'), Card('A', '♠'), Card('Q', '♥'), Card('2', '♦')
        ]
        result = SevenCardEvaluator.best_hand(cards)
        assert result.rank == HandRank.FOUR_OF_A_KIND
        # Vérifie que le meilleur kicker (A) est sélectionné
        assert result.cards[4].value == 'A'

    def test_seven_cards_finds_full_house(self):
        """Trouve un full house parmi 7 cartes"""
        cards = [
            Card('K', '♠'), Card('K', '♥'), Card('K', '♦'),
            Card('Q', '♣'), Card('Q', '♠'), Card('J', '♥'), Card('2', '♦')
        ]
        result = SevenCardEvaluator.best_hand(cards)
        assert result.rank == HandRank.FULL_HOUSE

    def test_seven_cards_finds_flush(self):
        """Trouve une couleur parmi 7 cartes"""
        cards = [
            Card('A', '♠'), Card('J', '♠'), Card('9', '♠'),
            Card('7', '♠'), Card('3', '♠'), Card('K', '♥'), Card('Q', '♦')
        ]
        result = SevenCardEvaluator.best_hand(cards)
        assert result.rank == HandRank.FLUSH

    def test_seven_cards_finds_straight(self):
        """Trouve une suite parmi 7 cartes"""
        cards = [
            Card('9', '♠'), Card('8', '♥'), Card('7', '♦'),
            Card('6', '♣'), Card('5', '♠'), Card('A', '♥'), Card('K', '♦')
        ]
        result = SevenCardEvaluator.best_hand(cards)
        assert result.rank == HandRank.STRAIGHT

    def test_seven_cards_finds_three_of_a_kind(self):
        """Trouve un brelan parmi 7 cartes"""
        cards = [
            Card('K', '♠'), Card('K', '♥'), Card('K', '♦'),
            Card('A', '♣'), Card('Q', '♠'), Card('J', '♥'), Card('2', '♦')
        ]
        result = SevenCardEvaluator.best_hand(cards)
        assert result.rank == HandRank.THREE_OF_A_KIND

    def test_seven_cards_finds_two_pair(self):
        """Trouve deux paires parmi 7 cartes"""
        cards = [
            Card('K', '♠'), Card('K', '♥'), Card('Q', '♦'),
            Card('Q', '♣'), Card('A', '♠'), Card('J', '♥'), Card('2', '♦')
        ]
        result = SevenCardEvaluator.best_hand(cards)
        assert result.rank == HandRank.TWO_PAIR

    def test_seven_cards_finds_one_pair(self):
        """Trouve une paire parmi 7 cartes"""
        cards = [
            Card('K', '♠'), Card('K', '♥'), Card('A', '♦'),
            Card('Q', '♣'), Card('J', '♠'), Card('9', '♥'), Card('2', '♦')
        ]
        result = SevenCardEvaluator.best_hand(cards)
        assert result.rank == HandRank.ONE_PAIR

    def test_seven_cards_finds_high_card(self):
        """Trouve la meilleure carte haute parmi 7 cartes"""
        cards = [
            Card('A', '♠'), Card('K', '♥'), Card('Q', '♦'),
            Card('J', '♣'), Card('9', '♠'), Card('7', '♥'), Card('2', '♦')
        ]
        result = SevenCardEvaluator.best_hand(cards)
        assert result.rank == HandRank.HIGH_CARD

    def test_best_five_from_seven_picks_best_kickers(self):
        """Avec un carré, sélectionne le meilleur kicker parmi les 3 restantes"""
        cards = [
            Card('K', '♠'), Card('K', '♥'), Card('K', '♦'),
            Card('K', '♣'), Card('A', '♠'), Card('Q', '♥'), Card('J', '♦')
        ]
        result = SevenCardEvaluator.best_hand(cards)
        assert result.rank == HandRank.FOUR_OF_A_KIND
        # Le kicker doit être l'As (la meilleure carte restante)
        assert result.cards[4].value == 'A'

    def test_best_five_from_seven_picks_best_flush(self):
        """Avec 6 cartes de même couleur, sélectionne les 5 meilleures"""
        cards = [
            Card('A', '♠'), Card('K', '♠'), Card('Q', '♠'),
            Card('J', '♠'), Card('9', '♠'), Card('7', '♠'), Card('2', '♥')
        ]
        result = SevenCardEvaluator.best_hand(cards)
        assert result.rank == HandRank.FLUSH
        # Vérifie que c'est les 5 meilleures cartes
        assert result.cards[0].value == 'A'
        assert result.cards[1].value == 'K'
        assert result.cards[2].value == 'Q'
        assert result.cards[3].value == 'J'
        assert result.cards[4].value == '9'

    def test_invalid_seven_cards_less_than_seven(self):
        """Erreur si moins de 7 cartes"""
        cards = [
            Card('A', '♠'), Card('K', '♥'), Card('Q', '♦'),
            Card('J', '♣'), Card('9', '♠'), Card('7', '♥')
        ]
        with pytest.raises(ValueError):
            SevenCardEvaluator.best_hand(cards)

    def test_invalid_seven_cards_more_than_seven(self):
        """Erreur si plus de 7 cartes"""
        cards = [
            Card('A', '♠'), Card('K', '♥'), Card('Q', '♦'),
            Card('J', '♣'), Card('9', '♠'), Card('7', '♥'),
            Card('5', '♦'), Card('3', '♣')
        ]
        with pytest.raises(ValueError):
            SevenCardEvaluator.best_hand(cards)
