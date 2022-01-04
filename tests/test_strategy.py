import pytest 

from src.card import Card
from src.deck import Deck
from src.hand import Hand
from src.strategy import SimpleStrategy, DealerStrategy


class TestSimpleStrategy:
    def test_simple_strategy_init(self):
        """Testing to see if two different strategies use the same
        deck. Which they should"""
        d = Deck(1)
        s1 = SimpleStrategy(d)
        s2 = SimpleStrategy(d)

        assert s1.deck == d
        assert s2.deck == d


    def test_simple_strategy_stand(self):
        c_2 = Card('Club', '2')
        c_5 = Card('Club', '5')
        c_j = Card('Heart', 'J')
        
        d = Deck(1)
        d.shuffle()
        d.cut()

        h1 = Hand()
        h1.add_card(c_5)
        h1.add_card(c_j)

        h2 = Hand()
        h2.add_card(c_2)
        h2.add_card(c_j)

        assert h1.get_value() == 15
        assert h2.get_value() == 12

        s1 = SimpleStrategy(d)
        s1.play(h1, None)

        s2 = SimpleStrategy(d)
        s2.play(h2, None)

        assert len(h1.cards) == 2
        assert len(h2.cards) == 2


    def test_simple_strategy_hit(self):
        c_3 = Card('Heart', '3')
        c_8 = Card('Club', '8')
        
        d = Deck(1)
        d.shuffle()
        d.cut()

        h = Hand()
        h.add_card(c_3)
        h.add_card(c_8)

        assert h.get_value() == 11

        s = SimpleStrategy(d)
        s.play(h, None)

        assert len(h.cards) == 3


class TestDealerStrategy():
    def test_dealer_strategy_init(self):
        d = Deck(1)
        s = DealerStrategy(d)

        assert s.deck == d


    def test_dealer_strategy_stand(self):
        c_7 = Card('Club', '7')
        c_j = Card('Heart', 'J')
        
        d = Deck(1)
        d.shuffle()
        d.cut()

        h = Hand()
        h.add_card(c_7)
        h.add_card(c_j)

        assert h.get_value() == 17

        s = DealerStrategy(d)
        s.play(h)

        assert len(h.cards) == 2


    def test_dealer_strategy_hit(self):
        c_6 = Card('Club', '6')
        c_j = Card('Heart', 'J')
       
        d = Deck(1)

        h = Hand()
        h.add_card(c_6)
        h.add_card(c_j)

        assert h.get_value() == 16

        s = DealerStrategy(d)
        s.play(h)

        assert len(h.cards) == 3
