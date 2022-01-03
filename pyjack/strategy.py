from hand import Hand
from deck import Deck

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


    def play(self, hand):
        """Play strategy
        Adds cards to hand based on strategy
        Args:
            hand: hand to use with strategy
            dealer_hand: shown dealer card to use with strategy
        """
        while hand.get_value() < 13:
            hand.add_card(self.deck.deal())


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

        while hand.get_value() < 18:
            hand.add_card(self.deck.deal())


 
# d1 = Deck(1)
# d1.shuffle()
# 
# h_player = Hand()
# h_dealer = Hand()
# 
# S_player = SimpleStrategy(d1)
# S_dealer = SimpleStrategy(d1)
# 
# S_player.play(h_player)
# S_dealer.play(h_dealer)
# 
# print("Dealer \n", h_dealer, "\n")
# print("Player \n", h_player)
