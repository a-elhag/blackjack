import pytest
from src.card import Card


class TestCard:
    def test_card_init(self):
        c = Card("Spade", 5)
        assert "Spade" == c.suit
        assert 5 == c.value


    def test_card_value(self):
        c_A = Card("Heart", "A")
        c_K = Card("Club", "K")
        c_Q = Card("Club", "Q")
        c_J = Card("Club", "J")
        c_10 = Card("Club", "10")
        c_7 = Card("Club", "7")
        assert 11 == c_A.get_value()
        assert 10 == c_K.get_value()
        assert 10 == c_Q.get_value()
        assert 10 == c_J.get_value()
        assert 10 == c_10.get_value()
        assert 7 == c_7.get_value()


    def test_card_set_card(self):
        c = Card("Spade", "3")

        assert c.get_suit() == "Spade"
        assert c.get_rank() == "3"

        c.set_card("Diamond", "6")

        assert c.get_suit() == "Diamond"
        assert c.get_rank() == "6"
        
