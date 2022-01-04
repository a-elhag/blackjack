import pytest
from pyjack.deck import Deck


class TestDeck():
    def test_deck_init(self):
        d1 = Deck(1)
        assert len(d1.cards) == 52

        d4 = Deck(4)
        assert len(d4.cards) == 52*4


    def test_deck_shuffle(self):
        d1 = Deck(1)
        assert d1.cards[0].suit == 'Spade'
        assert d1.cards[0].value == 'A'
        d1.shuffle()


    def test_deck_cut(self):
        d1 = Deck(1)
        n_cards = len(d1.cards)
        d1.cut()
        n_cards_cut = len(d1.cards)

        assert n_cards > n_cards_cut


    def test_deck_deal(self):
        d1 = Deck(1)
        c1 = d1.deal()

        assert c1.suit == 'Spade'
        assert c1.value == 'A'


    def test_deck_change_card(self):
        d1 = Deck(1)
        d1.set_card(1, "Heart", "Q")

        assert d1.cards[1].suit == "Heart"
        assert d1.cards[1].value == "Q"

