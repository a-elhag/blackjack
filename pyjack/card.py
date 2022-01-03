"""Module for cards"""

class Card():
    """Basic unit of card
    Args:
        suit: suit of card
        value: number value of card
    """

    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

        if self.suit == "Spade":
            self.suit_symbol = "♠"
        elif self.suit == "Club":
            self.suit_symbol = "♣"
        elif self.suit == "Diamond":
            self.suit_symbol = "♦"
        elif self.suit == "Heart":
            self.suit_symbol = "♥"


    def get_value(self):
        """Get numeric value of card
        Returns card value
        """

        if self.value == "A":
            return 11
        if self.value == "J" or self.value == "Q" or self.value == "K":
            return 10
        return int(self.value)

    def __repr__(self):
        """Repr of card"""
        return repr(str(self.value) + " " + self.suit_symbol)

