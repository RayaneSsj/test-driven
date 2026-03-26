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


class TestStraight:
    """Tests pour la détection de Straight"""

    def test_straight_detection(self):
        """Test détection d'une suite classique"""
        cards = [
            Card('9', '♠'),
            Card('8', '♥'),
            Card('7', '♦'),
            Card('6', '♣'),
            Card('5', '♠')
        ]
        result = HandEvaluator.evaluate(cards)
        assert result.rank == HandRank.STRAIGHT
        assert result.rank_name == "Straight"

    def test_straight_high_ace(self):
        """Test suite avec As haut (10-J-Q-K-A)"""
        cards = [
            Card('A', '♠'),
            Card('K', '♥'),
            Card('Q', '♦'),
            Card('J', '♣'),
            Card('10', '♠')
        ]
        result = HandEvaluator.evaluate(cards)
        assert result.rank == HandRank.STRAIGHT
        # L'As devrait être la carte la plus haute
        assert result.cards[0].value == 'A'

    def test_straight_low_ace(self):
        """Test suite avec As bas (A-2-3-4-5), aussi appelée wheel"""
        cards = [
            Card('A', '♠'),
            Card('2', '♥'),
            Card('3', '♦'),
            Card('4', '♣'),
            Card('5', '♠')
        ]
        result = HandEvaluator.evaluate(cards)
        assert result.rank == HandRank.STRAIGHT
        # Dans la wheel, le 5 est la carte haute
        assert result.cards[0].value == '5'

    def test_straight_middle_values(self):
        """Test suite avec valeurs moyennes"""
        cards = [
            Card('7', '♠'),
            Card('6', '♥'),
            Card('5', '♦'),
            Card('4', '♣'),
            Card('3', '♠')
        ]
        result = HandEvaluator.evaluate(cards)
        assert result.rank == HandRank.STRAIGHT

    def test_not_straight_when_gap(self):
        """Test qu'une suite avec trou n'est pas détectée comme suite"""
        cards = [
            Card('9', '♠'),
            Card('8', '♥'),
            Card('7', '♦'),
            Card('6', '♣'),
            Card('4', '♠')  # Il manque le 5
        ]
        result = HandEvaluator.evaluate(cards)
        assert result.rank != HandRank.STRAIGHT
        assert result.rank == HandRank.HIGH_CARD

    def test_not_straight_wraparound(self):
        """Test que Q-K-A-2-3 n'est pas une suite valide"""
        cards = [
            Card('Q', '♠'),
            Card('K', '♥'),
            Card('A', '♦'),
            Card('2', '♣'),
            Card('3', '♠')
        ]
        result = HandEvaluator.evaluate(cards)
        assert result.rank != HandRank.STRAIGHT
        assert result.rank == HandRank.HIGH_CARD

    def test_not_straight_when_pair(self):
        """Test qu'une paire dans la séquence empêche la suite"""
        cards = [
            Card('9', '♠'),
            Card('8', '♥'),
            Card('7', '♦'),
            Card('7', '♣'),
            Card('6', '♠')
        ]
        result = HandEvaluator.evaluate(cards)
        assert result.rank != HandRank.STRAIGHT
        assert result.rank == HandRank.ONE_PAIR


class TestFlush:
    """Tests pour la détection de Flush"""

    def test_flush_detection(self):
        """Test détection d'une couleur (flush)"""
        cards = [
            Card('A', '♠'),
            Card('J', '♠'),
            Card('8', '♠'),
            Card('5', '♠'),
            Card('3', '♠')
        ]
        result = HandEvaluator.evaluate(cards)
        assert result.rank == HandRank.FLUSH
        assert result.rank_name == "Flush"

    def test_flush_with_hearts(self):
        """Test flush avec cœurs"""
        cards = [
            Card('K', '♥'),
            Card('Q', '♥'),
            Card('9', '♥'),
            Card('6', '♥'),
            Card('2', '♥')
        ]
        result = HandEvaluator.evaluate(cards)
        assert result.rank == HandRank.FLUSH

    def test_flush_with_diamonds(self):
        """Test flush avec carreaux"""
        cards = [
            Card('10', '♦'),
            Card('8', '♦'),
            Card('7', '♦'),
            Card('4', '♦'),
            Card('3', '♦')
        ]
        result = HandEvaluator.evaluate(cards)
        assert result.rank == HandRank.FLUSH

    def test_flush_with_clubs(self):
        """Test flush avec trèfles"""
        cards = [
            Card('J', '♣'),
            Card('9', '♣'),
            Card('7', '♣'),
            Card('5', '♣'),
            Card('2', '♣')
        ]
        result = HandEvaluator.evaluate(cards)
        assert result.rank == HandRank.FLUSH

    def test_flush_cards_sorted_by_value(self):
        """Test que les cartes du flush sont triées par valeur décroissante"""
        cards = [
            Card('3', '♠'),
            Card('A', '♠'),
            Card('5', '♠'),
            Card('J', '♠'),
            Card('8', '♠')
        ]
        result = HandEvaluator.evaluate(cards)
        assert result.rank == HandRank.FLUSH
        # Les cartes devraient être triées: A, J, 8, 5, 3
        assert result.cards[0].value == 'A'
        assert result.cards[1].value == 'J'
        assert result.cards[2].value == '8'
        assert result.cards[3].value == '5'
        assert result.cards[4].value == '3'

    def test_not_flush_when_different_suits(self):
        """Test qu'une main avec couleurs différentes n'est pas un flush"""
        cards = [
            Card('A', '♠'),
            Card('K', '♠'),
            Card('Q', '♠'),
            Card('J', '♠'),
            Card('9', '♥')  # Une carte d'une couleur différente
        ]
        result = HandEvaluator.evaluate(cards)
        assert result.rank != HandRank.FLUSH
        assert result.rank == HandRank.HIGH_CARD


class TestFullHouse:
    """Tests pour la détection de Full House"""

    def test_full_house_detection(self):
        """Test détection d'un full house (brelan + paire)"""
        cards = [
            Card('A', '♠'),
            Card('A', '♥'),
            Card('A', '♦'),
            Card('K', '♣'),
            Card('K', '♠')
        ]
        result = HandEvaluator.evaluate(cards)
        assert result.rank == HandRank.FULL_HOUSE
        assert result.rank_name == "Full House"

    def test_full_house_with_low_trips(self):
        """Test full house avec brelan de cartes basses"""
        cards = [
            Card('3', '♠'),
            Card('3', '♥'),
            Card('3', '♦'),
            Card('Q', '♣'),
            Card('Q', '♠')
        ]
        result = HandEvaluator.evaluate(cards)
        assert result.rank == HandRank.FULL_HOUSE

    def test_full_house_identifies_trips_and_pair(self):
        """Test que le brelan et la paire sont identifiés correctement"""
        cards = [
            Card('J', '♠'),
            Card('J', '♥'),
            Card('J', '♦'),
            Card('7', '♣'),
            Card('7', '♠')
        ]
        result = HandEvaluator.evaluate(cards)
        assert result.rank == HandRank.FULL_HOUSE
        # Les trois premières cartes devraient être le brelan
        assert result.cards[0].value == 'J'
        assert result.cards[1].value == 'J'
        assert result.cards[2].value == 'J'
        # Les deux suivantes devraient être la paire
        assert result.cards[3].value == '7'
        assert result.cards[4].value == '7'

    def test_full_house_trips_over_pair(self):
        """Test full house avec brelan plus faible que la paire"""
        cards = [
            Card('5', '♠'),
            Card('5', '♥'),
            Card('5', '♦'),
            Card('K', '♣'),
            Card('K', '♠')
        ]
        result = HandEvaluator.evaluate(cards)
        assert result.rank == HandRank.FULL_HOUSE
        # Le brelan devrait être en premier (5)
        assert result.cards[0].value == '5'
        assert result.cards[1].value == '5'
        assert result.cards[2].value == '5'

    def test_not_full_house_when_three_of_a_kind(self):
        """Test qu'un brelan simple n'est pas un full"""
        cards = [
            Card('K', '♠'),
            Card('K', '♥'),
            Card('K', '♦'),
            Card('Q', '♣'),
            Card('9', '♠')
        ]
        result = HandEvaluator.evaluate(cards)
        assert result.rank != HandRank.FULL_HOUSE
        assert result.rank == HandRank.THREE_OF_A_KIND
