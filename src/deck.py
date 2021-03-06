import random

from src.card import Card

SUITS = ["Spade", "Club", "Heart", "Diamond"]
CARD_VALUES = ["A", "2", "3", "4", "5", "6", "7", "8",
                "9", "10", "J", "Q", "K"]


class Deck():
    """Basic deck of gameplay
    Args:
        num_decks: number of decks to use
    """

    def __init__(self, num_decks):
        self.cards = [Card(s,v) for s in SUITS for v in CARD_VALUES] * num_decks


    def shuffle(self):
        """Shuffles deck"""
        if len(self.cards) > 1:
            random.shuffle(self.cards)

    
    def cut(self):
        """Cuts deck at uniform random dist around first 15 cards or so"""
        if len(self.cards) > 1:
            n_cards = len(self.cards)
            cut_point = random.randint(round(n_cards*0.7), round(n_cards*0.9))
            self.cards = self.cards[:cut_point]


    def deal(self):
        """Gets first card from deck by returning it"""
        if len(self.cards) > 1:
            return self.cards.pop(0)
        else:
            return None


    def set_card(self, location, suit, value):
        """Changes one of the cards
        Args:
            location: location of the card change
            suit: suit of the desired card
            value: value of the desired card
        """
        self.cards[location].set_card(suit, value)
