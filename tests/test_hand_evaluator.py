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


class TestTwoPair:
    """Tests pour la détection de Two Pair"""

    def test_two_pair_detection(self):
        """Test détection de deux paires"""
        cards = [
            Card('A', '♠'),
            Card('A', '♥'),
            Card('K', '♦'),
            Card('K', '♣'),
            Card('3', '♠')
        ]
        result = HandEvaluator.evaluate(cards)
        assert result.rank == HandRank.TWO_PAIR
        assert result.rank_name == "Two Pair"

    def test_two_pair_with_low_pairs(self):
        """Test deux paires avec des cartes basses"""
        cards = [
            Card('9', '♠'),
            Card('9', '♥'),
            Card('5', '♦'),
            Card('5', '♣'),
            Card('2', '♠')
        ]
        result = HandEvaluator.evaluate(cards)
        assert result.rank == HandRank.TWO_PAIR

    def test_two_pair_identifies_pairs_correctly(self):
        """Test que les deux paires sont identifiées dans le bon ordre"""
        cards = [
            Card('J', '♠'),
            Card('J', '♥'),
            Card('7', '♦'),
            Card('7', '♣'),
            Card('4', '♠')
        ]
        result = HandEvaluator.evaluate(cards)
        assert result.rank == HandRank.TWO_PAIR
        # Les deux premières cartes devraient être la paire la plus haute (Valets)
        assert result.cards[0].value == 'J'
        assert result.cards[1].value == 'J'
        # Les deux suivantes devraient être la deuxième paire (7)
        assert result.cards[2].value == '7'
        assert result.cards[3].value == '7'
        # La dernière devrait être le kicker
        assert result.cards[4].value == '4'

    def test_two_pair_with_high_kicker(self):
        """Test deux paires avec un kicker élevé"""
        cards = [
            Card('8', '♠'),
            Card('8', '♥'),
            Card('3', '♦'),
            Card('3', '♣'),
            Card('A', '♠')
        ]
        result = HandEvaluator.evaluate(cards)
        assert result.rank == HandRank.TWO_PAIR
        # La dernière carte devrait être l'As (kicker)
        assert result.cards[4].value == 'A'

    def test_not_two_pair_when_one_pair(self):
        """Test qu'une seule paire n'est pas détectée comme deux paires"""
        cards = [
            Card('K', '♠'),
            Card('K', '♥'),
            Card('Q', '♦'),
            Card('J', '♣'),
            Card('9', '♠')
        ]
        result = HandEvaluator.evaluate(cards)
        assert result.rank != HandRank.TWO_PAIR
        assert result.rank == HandRank.ONE_PAIR


class TestThreeOfAKind:
    """Tests pour la détection de Three of a Kind"""

    def test_three_of_a_kind_detection(self):
        """Test détection d'un brelan"""
        cards = [
            Card('A', '♠'),
            Card('A', '♥'),
            Card('A', '♦'),
            Card('K', '♣'),
            Card('3', '♠')
        ]
        result = HandEvaluator.evaluate(cards)
        assert result.rank == HandRank.THREE_OF_A_KIND
        assert result.rank_name == "Three of a Kind"

    def test_three_of_a_kind_with_low_trips(self):
        """Test brelan avec des cartes basses"""
        cards = [
            Card('5', '♠'),
            Card('5', '♥'),
            Card('5', '♦'),
            Card('K', '♣'),
            Card('Q', '♠')
        ]
        result = HandEvaluator.evaluate(cards)
        assert result.rank == HandRank.THREE_OF_A_KIND

    def test_three_of_a_kind_identifies_trips_correctly(self):
        """Test que le brelan est identifié correctement"""
        cards = [
            Card('J', '♠'),
            Card('J', '♥'),
            Card('J', '♦'),
            Card('9', '♣'),
            Card('4', '♠')
        ]
        result = HandEvaluator.evaluate(cards)
        assert result.rank == HandRank.THREE_OF_A_KIND
        # Les trois premières cartes devraient être le brelan
        assert result.cards[0].value == 'J'
        assert result.cards[1].value == 'J'
        assert result.cards[2].value == 'J'

    def test_three_of_a_kind_kickers_sorted(self):
        """Test que les kickers sont triés par ordre décroissant"""
        cards = [
            Card('8', '♠'),
            Card('8', '♥'),
            Card('8', '♦'),
            Card('3', '♣'),
            Card('A', '♠')
        ]
        result = HandEvaluator.evaluate(cards)
        assert result.rank == HandRank.THREE_OF_A_KIND
        # Le kicker le plus haut devrait être l'As
        assert result.cards[3].value == 'A'
        assert result.cards[4].value == '3'

    def test_not_three_of_a_kind_when_two_pair(self):
        """Test qu'une double paire n'est pas détectée comme brelan"""
        cards = [
            Card('K', '♠'),
            Card('K', '♥'),
            Card('Q', '♦'),
            Card('Q', '♣'),
            Card('9', '♠')
        ]
        result = HandEvaluator.evaluate(cards)
        assert result.rank != HandRank.THREE_OF_A_KIND
        assert result.rank == HandRank.TWO_PAIR
