"""Module for cards"""

class Card():
    """Basic unit of card
    Args:
        suit: suit of card
        value: number value of card
    """

    def __init__(self, suit, value):
        self.set_card(suit, value)


    def set_card(self, suit, value):
        self.suit = suit
        self.value = value
        self.set_suite()


    def set_suite(self):
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

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.value

    def __repr__(self):
        """Repr of card"""
        return repr(str(self.value) + " " + self.suit_symbol)

