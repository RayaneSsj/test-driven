import pytest
from poker.card import Card


class TestCard:
    """Tests pour la classe Card"""

    def test_create_card_with_numeric_value(self):
        """Test création d'une carte avec valeur numérique"""
        card = Card('7', '♠')
        assert card.value == '7'
        assert card.suit == '♠'

    def test_create_card_with_face_value(self):
        """Test création d'une carte avec figure"""
        card = Card('K', '♥')
        assert card.value == 'K'
        assert card.suit == '♥'

    def test_create_card_with_ace(self):
        """Test création d'un As"""
        card = Card('A', '♦')
        assert card.value == 'A'
        assert card.suit == '♦'

    def test_card_string_representation(self):
        """Test représentation textuelle d'une carte"""
        card = Card('Q', '♣')
        assert str(card) == 'Q♣'

    def test_card_equality(self):
        """Test égalité entre deux cartes identiques"""
        card1 = Card('10', '♠')
        card2 = Card('10', '♠')
        assert card1 == card2

    def test_card_inequality_different_value(self):
        """Test inégalité entre cartes de valeurs différentes"""
        card1 = Card('5', '♥')
        card2 = Card('6', '♥')
        assert card1 != card2

    def test_card_inequality_different_suit(self):
        """Test inégalité entre cartes de couleurs différentes"""
        card1 = Card('J', '♠')
        card2 = Card('J', '♥')
        assert card1 != card2

    def test_card_comparison_by_value(self):
        """Test comparaison de cartes par valeur"""
        card_2 = Card('2', '♠')
        card_5 = Card('5', '♥')
        card_10 = Card('10', '♦')
        card_j = Card('J', '♣')
        card_q = Card('Q', '♠')
        card_k = Card('K', '♥')
        card_a = Card('A', '♦')

        # Test ordre croissant
        assert card_2 < card_5
        assert card_5 < card_10
        assert card_10 < card_j
        assert card_j < card_q
        assert card_q < card_k
        assert card_k < card_a

    def test_card_comparison_same_value_different_suit(self):
        """Test comparaison de cartes de même valeur mais couleur différente"""
        card1 = Card('7', '♠')
        card2 = Card('7', '♥')
        # Même valeur = égalité pour la comparaison
        assert not (card1 < card2)
        assert not (card2 < card1)

    def test_invalid_card_value(self):
        """Test création d'une carte avec valeur invalide"""
        with pytest.raises(ValueError):
            Card('15', '♠')

    def test_invalid_card_suit(self):
        """Test création d'une carte avec couleur invalide"""
        with pytest.raises(ValueError):
            Card('7', '♪')
