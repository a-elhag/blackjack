from pyjack.card import Card

HIT = "H"
DOUBLE = "D"
STAND = "St"
SPLIT = "Sp"

class SimpleStrategy():
    """Simplest strategy possible
    Stand 12 or over
    Args:
        deck: deck of cards to deal from
    """

    def __init__(self, deck):
        self.deck = deck
        self.split_hands = []


    def play(self, player_hand, dealer_hand):
        """Play strategy
        Adds cards to hand based on strategy
        Args:
            hand: hand to use with strategy
            dealer_hand: shown dealer card to use with strategy
        """


        while player_hand.get_value() < 12 and player_hand.get_value() > 2:
            c = self.deck.deal()
            player_hand.add_card(c)

            if c == None:
                break


class DealerStrategy():
    """Dealer basic casino rules strategy
    If total hand value >= 17, stand
    If total is < 17, must hit
    Continue to take cards until total is >= 17
    If ace would bring total to >=17 must use as 11

    Args:
        deck: deck of cards to deal from
    """

    def __init__(self, deck):
        self.deck = deck


    def play(self, hand):
        """Play strategy
        Add cards to hand based on strategy
        Args:
            hand: hand to use with strategy
        """

        while hand.get_value() < 17 and hand.get_value() > 2:
            hand.add_card(self.deck.deal())

