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

        # Pour l'instant, on retourne toujours HIGH_CARD
        # Les autres combinaisons seront ajoutées progressivement
        return HandResult(
            rank=HandRank.HIGH_CARD,
            cards=sorted_cards,
            rank_name="High Card"
        )
