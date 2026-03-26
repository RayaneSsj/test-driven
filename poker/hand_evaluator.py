from enum import IntEnum
from typing import List
from poker.card import Card


class HandRank(IntEnum):
    """Rangs des mains de poker (valeur croissante)"""
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIR = 3


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
