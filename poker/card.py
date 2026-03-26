class Card:
    """Représente une carte de poker avec une valeur et une couleur"""

    VALID_VALUES = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    VALID_SUITS = ['♠', '♥', '♦', '♣']

    # Ordre des valeurs pour la comparaison (index = force de la carte)
    VALUE_ORDER = {
        '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
        'J': 11, 'Q': 12, 'K': 13, 'A': 14
    }

    def __init__(self, value: str, suit: str):
        """
        Initialise une carte

        Args:
            value: Valeur de la carte (2-10, J, Q, K, A)
            suit: Couleur de la carte (♠, ♥, ♦, ♣)

        Raises:
            ValueError: Si la valeur ou la couleur n'est pas valide
        """
        if value not in self.VALID_VALUES:
            raise ValueError(f"Valeur invalide: {value}. Doit être parmi {self.VALID_VALUES}")
        if suit not in self.VALID_SUITS:
            raise ValueError(f"Couleur invalide: {suit}. Doit être parmi {self.VALID_SUITS}")

        self.value = value
        self.suit = suit

    def __str__(self) -> str:
        """Retourne la représentation textuelle de la carte"""
        return f"{self.value}{self.suit}"

    def __repr__(self) -> str:
        """Retourne la représentation pour le débogage"""
        return f"Card('{self.value}', '{self.suit}')"

    def __eq__(self, other) -> bool:
        """Test d'égalité entre deux cartes (même valeur ET même couleur)"""
        if not isinstance(other, Card):
            return False
        return self.value == other.value and self.suit == other.suit

    def __lt__(self, other) -> bool:
        """Test si cette carte est inférieure à une autre (basé sur la valeur uniquement)"""
        if not isinstance(other, Card):
            return NotImplemented
        return self.VALUE_ORDER[self.value] < self.VALUE_ORDER[other.value]

    def __le__(self, other) -> bool:
        """Test si cette carte est inférieure ou égale à une autre"""
        if not isinstance(other, Card):
            return NotImplemented
        return self.VALUE_ORDER[self.value] <= self.VALUE_ORDER[other.value]

    def __gt__(self, other) -> bool:
        """Test si cette carte est supérieure à une autre"""
        if not isinstance(other, Card):
            return NotImplemented
        return self.VALUE_ORDER[self.value] > self.VALUE_ORDER[other.value]

    def __ge__(self, other) -> bool:
        """Test si cette carte est supérieure ou égale à une autre"""
        if not isinstance(other, Card):
            return NotImplemented
        return self.VALUE_ORDER[self.value] >= self.VALUE_ORDER[other.value]
