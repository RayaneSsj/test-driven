from enum import IntEnum
from typing import List
from poker.card import Card


class HandRank(IntEnum):
    """Rangs des mains de poker (valeur croissante)"""
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    STRAIGHT = 5
    FLUSH = 6
    FULL_HOUSE = 7
    FOUR_OF_A_KIND = 8
    STRAIGHT_FLUSH = 9


class HandResult:
    """Résultat de l'évaluation d'une main"""

    def __init__(self, rank: HandRank, cards: List[Card], rank_name: str):
        """
        Initialise le résultat d'une main

        Args:
            rank: Le rang de la main (HIGH_CARD, ONE_PAIR, etc.)
            cards: Les cartes triées par importance (carte la plus forte en premier)
            rank_name: Le nom du rang en français
        """
        self.rank = rank
        self.cards = cards
        self.rank_name = rank_name

    def __repr__(self) -> str:
        cards_str = ', '.join(str(card) for card in self.cards)
        return f"HandResult({self.rank_name}, [{cards_str}])"

    def __gt__(self, other: 'HandResult') -> bool:
        """Compare deux mains (plus grand que)"""
        if self.rank != other.rank:
            return self.rank > other.rank
        # Même rang: comparer carte par carte
        for my_card, other_card in zip(self.cards, other.cards):
            if Card.VALUE_ORDER[my_card.value] != Card.VALUE_ORDER[other_card.value]:
                return Card.VALUE_ORDER[my_card.value] > Card.VALUE_ORDER[other_card.value]
        return False

    def __lt__(self, other: 'HandResult') -> bool:
        """Compare deux mains (plus petit que)"""
        return other > self

    def __eq__(self, other: 'HandResult') -> bool:
        """Égalité entre deux mains"""
        if self.rank != other.rank:
            return False
        for my_card, other_card in zip(self.cards, other.cards):
            if Card.VALUE_ORDER[my_card.value] != Card.VALUE_ORDER[other_card.value]:
                return False
        return True

    def __ge__(self, other: 'HandResult') -> bool:
        return self > other or self == other

    def __le__(self, other: 'HandResult') -> bool:
        return self < other or self == other


class HandEvaluator:
    """Évaluateur de mains de poker"""

    @staticmethod
    def evaluate(cards: List[Card]) -> HandResult:
        """
        Évalue une main de 5 cartes et retourne son rang

        Args:
            cards: Liste de 5 cartes

        Returns:
            HandResult contenant le rang et les cartes triées

        Raises:
            ValueError: Si le nombre de cartes n'est pas égal à 5
        """
        if len(cards) != 5:
            raise ValueError(f"Une main doit contenir exactement 5 cartes, {len(cards)} fournie(s)")

        # Trier les cartes par valeur décroissante
        sorted_cards = sorted(cards, key=lambda c: Card.VALUE_ORDER[c.value], reverse=True)

        # Compter les occurrences de chaque valeur
        value_counts = HandEvaluator._count_values(cards)

        # Vérifier Straight Flush (doit être la première vérification car c'est la meilleure main)
        straight_flush_result = HandEvaluator._check_straight_flush(sorted_cards)
        if straight_flush_result:
            return straight_flush_result

        # Vérifier Four of a Kind (doit être vérifié avant Full House)
        four_of_a_kind_result = HandEvaluator._check_four_of_a_kind(sorted_cards, value_counts)
        if four_of_a_kind_result:
            return four_of_a_kind_result

        # Vérifier Full House (doit être vérifié avant Flush car Full House > Flush)
        full_house_result = HandEvaluator._check_full_house(sorted_cards, value_counts)
        if full_house_result:
            return full_house_result

        # Vérifier Flush (doit être vérifié avant Straight car Flush > Straight)
        flush_result = HandEvaluator._check_flush(sorted_cards)
        if flush_result:
            return flush_result

        # Vérifier Straight (doit être vérifié avant les combinaisons avec paires)
        straight_result = HandEvaluator._check_straight(sorted_cards)
        if straight_result:
            return straight_result

        # Vérifier Three of a Kind (doit être vérifié avant Two Pair et One Pair)
        three_of_a_kind_result = HandEvaluator._check_three_of_a_kind(sorted_cards, value_counts)
        if three_of_a_kind_result:
            return three_of_a_kind_result

        # Vérifier Two Pair (doit être vérifié avant One Pair)
        two_pair_result = HandEvaluator._check_two_pair(sorted_cards, value_counts)
        if two_pair_result:
            return two_pair_result

        # Vérifier One Pair
        pair_result = HandEvaluator._check_one_pair(sorted_cards, value_counts)
        if pair_result:
            return pair_result

        # Par défaut, retourner HIGH_CARD
        return HandResult(
            rank=HandRank.HIGH_CARD,
            cards=sorted_cards,
            rank_name="High Card"
        )

    @staticmethod
    def _count_values(cards: List[Card]) -> dict:
        """
        Compte le nombre d'occurrences de chaque valeur

        Args:
            cards: Liste de cartes

        Returns:
            Dictionnaire {valeur: nombre d'occurrences}
        """
        value_counts = {}
        for card in cards:
            value_counts[card.value] = value_counts.get(card.value, 0) + 1
        return value_counts

    @staticmethod
    def _check_one_pair(sorted_cards: List[Card], value_counts: dict) -> HandResult | None:
        """
        Vérifie si la main contient une paire (et pas deux paires)

        Args:
            sorted_cards: Cartes triées par valeur décroissante
            value_counts: Dictionnaire des occurrences de chaque valeur

        Returns:
            HandResult si une paire est trouvée, None sinon
        """
        # Trouver les paires
        pairs = [value for value, count in value_counts.items() if count == 2]

        # Une seule paire (pas deux paires ou plus)
        if len(pairs) == 1:
            pair_value = pairs[0]

            # Séparer les cartes de la paire et les autres
            pair_cards = [card for card in sorted_cards if card.value == pair_value]
            kickers = [card for card in sorted_cards if card.value != pair_value]

            # Organiser les cartes : paire en premier, puis kickers par ordre décroissant
            result_cards = pair_cards + kickers

            return HandResult(
                rank=HandRank.ONE_PAIR,
                cards=result_cards,
                rank_name="One Pair"
            )

        return None

    @staticmethod
    def _check_two_pair(sorted_cards: List[Card], value_counts: dict) -> HandResult | None:
        """
        Vérifie si la main contient deux paires

        Args:
            sorted_cards: Cartes triées par valeur décroissante
            value_counts: Dictionnaire des occurrences de chaque valeur

        Returns:
            HandResult si deux paires sont trouvées, None sinon
        """
        # Trouver les paires
        pairs = [value for value, count in value_counts.items() if count == 2]

        # Deux paires exactement
        if len(pairs) == 2:
            # Trier les paires par valeur décroissante
            pairs_sorted = sorted(pairs, key=lambda v: Card.VALUE_ORDER[v], reverse=True)
            high_pair_value = pairs_sorted[0]
            low_pair_value = pairs_sorted[1]

            # Séparer les cartes
            high_pair_cards = [card for card in sorted_cards if card.value == high_pair_value]
            low_pair_cards = [card for card in sorted_cards if card.value == low_pair_value]
            kicker = [card for card in sorted_cards if card.value not in pairs]

            # Organiser les cartes : paire haute, paire basse, puis kicker
            result_cards = high_pair_cards + low_pair_cards + kicker

            return HandResult(
                rank=HandRank.TWO_PAIR,
                cards=result_cards,
                rank_name="Two Pair"
            )

        return None

    @staticmethod
    def _check_three_of_a_kind(sorted_cards: List[Card], value_counts: dict) -> HandResult | None:
        """
        Vérifie si la main contient un brelan

        Args:
            sorted_cards: Cartes triées par valeur décroissante
            value_counts: Dictionnaire des occurrences de chaque valeur

        Returns:
            HandResult si un brelan est trouvé, None sinon
        """
        # Trouver les brelans
        trips = [value for value, count in value_counts.items() if count == 3]

        # Un brelan trouvé
        if len(trips) == 1:
            trips_value = trips[0]

            # Séparer les cartes du brelan et les kickers
            trips_cards = [card for card in sorted_cards if card.value == trips_value]
            kickers = [card for card in sorted_cards if card.value != trips_value]

            # Organiser les cartes : brelan en premier, puis kickers par ordre décroissant
            result_cards = trips_cards + kickers

            return HandResult(
                rank=HandRank.THREE_OF_A_KIND,
                cards=result_cards,
                rank_name="Three of a Kind"
            )

        return None

    @staticmethod
    def _check_straight(sorted_cards: List[Card]) -> HandResult | None:
        """
        Vérifie si la main contient une suite

        Args:
            sorted_cards: Cartes triées par valeur décroissante

        Returns:
            HandResult si une suite est trouvée, None sinon
        """
        # Extraire les valeurs numériques
        values = [Card.VALUE_ORDER[card.value] for card in sorted_cards]

        # Vérifier si c'est une suite normale (chaque carte = précédente - 1)
        is_straight = all(values[i] == values[i + 1] + 1 for i in range(len(values) - 1))

        if is_straight:
            # Suite normale, cartes déjà triées par ordre décroissant
            return HandResult(
                rank=HandRank.STRAIGHT,
                cards=sorted_cards,
                rank_name="Straight"
            )

        # Vérifier la wheel (A-2-3-4-5)
        # Les valeurs doivent être [14, 5, 4, 3, 2] (A en premier car trié par ordre décroissant)
        if values == [14, 5, 4, 3, 2]:
            # Dans la wheel, le 5 est la carte haute, donc réorganiser les cartes
            # 5-4-3-2-A
            wheel_cards = sorted_cards[1:] + [sorted_cards[0]]
            return HandResult(
                rank=HandRank.STRAIGHT,
                cards=wheel_cards,
                rank_name="Straight"
            )

        return None

    @staticmethod
    def _check_flush(sorted_cards: List[Card]) -> HandResult | None:
        """
        Vérifie si la main contient un flush (5 cartes de même couleur)

        Args:
            sorted_cards: Cartes triées par valeur décroissante

        Returns:
            HandResult si un flush est trouvé, None sinon
        """
        # Vérifier si toutes les cartes ont la même couleur
        first_suit = sorted_cards[0].suit
        is_flush = all(card.suit == first_suit for card in sorted_cards)

        if is_flush:
            # Les cartes sont déjà triées par valeur décroissante
            return HandResult(
                rank=HandRank.FLUSH,
                cards=sorted_cards,
                rank_name="Flush"
            )

        return None

    @staticmethod
    def _check_full_house(sorted_cards: List[Card], value_counts: dict) -> HandResult | None:
        """
        Vérifie si la main contient un full house (brelan + paire)

        Args:
            sorted_cards: Cartes triées par valeur décroissante
            value_counts: Dictionnaire des occurrences de chaque valeur

        Returns:
            HandResult si un full house est trouvé, None sinon
        """
        # Trouver les brelans et les paires
        trips = [value for value, count in value_counts.items() if count == 3]
        pairs = [value for value, count in value_counts.items() if count == 2]

        # Full house = 1 brelan + 1 paire
        if len(trips) == 1 and len(pairs) == 1:
            trips_value = trips[0]
            pair_value = pairs[0]

            # Séparer les cartes du brelan et de la paire
            trips_cards = [card for card in sorted_cards if card.value == trips_value]
            pair_cards = [card for card in sorted_cards if card.value == pair_value]

            # Organiser les cartes : brelan en premier, puis paire
            result_cards = trips_cards + pair_cards

            return HandResult(
                rank=HandRank.FULL_HOUSE,
                cards=result_cards,
                rank_name="Full House"
            )

        return None

    @staticmethod
    def _check_four_of_a_kind(sorted_cards: List[Card], value_counts: dict) -> HandResult | None:
        """
        Vérifie si la main contient un carré (four of a kind)

        Args:
            sorted_cards: Cartes triées par valeur décroissante
            value_counts: Dictionnaire des occurrences de chaque valeur

        Returns:
            HandResult si un carré est trouvé, None sinon
        """
        # Trouver les carrés
        quads = [value for value, count in value_counts.items() if count == 4]

        # Un carré trouvé
        if len(quads) == 1:
            quads_value = quads[0]

            # Séparer les cartes du carré et le kicker
            quads_cards = [card for card in sorted_cards if card.value == quads_value]
            kicker = [card for card in sorted_cards if card.value != quads_value]

            # Organiser les cartes : carré en premier, puis kicker
            result_cards = quads_cards + kicker

            return HandResult(
                rank=HandRank.FOUR_OF_A_KIND,
                cards=result_cards,
                rank_name="Four of a Kind"
            )

        return None

    @staticmethod
    def _check_straight_flush(sorted_cards: List[Card]) -> HandResult | None:
        """
        Vérifie si la main contient une quinte flush (suite de même couleur)

        Args:
            sorted_cards: Cartes triées par valeur décroissante

        Returns:
            HandResult si une quinte flush est trouvée, None sinon
        """
        # Vérifier d'abord si toutes les cartes sont de la même couleur (flush)
        first_suit = sorted_cards[0].suit
        is_flush = all(card.suit == first_suit for card in sorted_cards)

        if not is_flush:
            return None

        # Si c'est un flush, vérifier si c'est aussi une suite
        values = [Card.VALUE_ORDER[card.value] for card in sorted_cards]

        # Vérifier si c'est une suite normale (chaque carte = précédente - 1)
        is_straight = all(values[i] == values[i + 1] + 1 for i in range(len(values) - 1))

        if is_straight:
            # Suite flush normale, cartes déjà triées par ordre décroissant
            return HandResult(
                rank=HandRank.STRAIGHT_FLUSH,
                cards=sorted_cards,
                rank_name="Straight Flush"
            )

        # Vérifier la wheel (A-2-3-4-5)
        if values == [14, 5, 4, 3, 2]:
            # Dans la wheel, le 5 est la carte haute, donc réorganiser les cartes
            wheel_cards = sorted_cards[1:] + [sorted_cards[0]]
            return HandResult(
                rank=HandRank.STRAIGHT_FLUSH,
                cards=wheel_cards,
                rank_name="Straight Flush"
            )

        return None
