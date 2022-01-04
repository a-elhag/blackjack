import pytest
from src.card import Card
from src.hand import Hand

class TestHand():
    def test_hand_init(self):
        h = Hand()
        assert h.cards == []
        assert h.value == 0
        assert h.bet == 0.0


    def test_hand_add_card(self):
        h = Hand()
        c_a = Card('Spade', 'A')
        c_9 = Card('Heart', '9')

        h.add_card(c_a)
        h.add_card(c_9)

        assert h.cards[0].suit == 'Spade'
        assert h.cards[0].value == 'A'
        assert h.cards[1].suit == 'Heart'
        assert h.cards[1].value == '9'


    def test_hand_add_bet(self):
        h = Hand()

        h.add_bet(15)
        assert h.bet == 15

        h.add_bet(h.bet*2)
        assert h.bet == 15*2


    def test_hand_add_bet_negative(self):
        h = Hand()
        with pytest.raises(ValueError):
            h.add_bet(-10)


    def test_hand_calculate_value_simple(self):
        h = Hand()
        c_5 = Card('Club', '5')
        c_6 = Card('Diamond', '6')

        h.add_card(c_5)
        assert h.get_value() == 5

        h.add_card(c_5)
        assert h.get_value() == 10

        h.add_card(c_6)
        assert h.get_value() == 16


    def test_hand_calculate_value_j_q_k(self):
        h = Hand()

        c_10 = Card('Spade', '10')
        c_j = Card('Spade', 'J')
        c_q = Card('Spade', 'Q')
        c_k = Card('Spade', 'K')

        h.add_card(c_10)
        assert h.get_value() == 10

        h.add_card(c_j)
        assert h.get_value() == 20

        h.add_card(c_q)
        assert h.get_value() == 30

        h.add_card(c_k)
        assert h.get_value() == 40


    def test_hand_calculate_value_ace(self):
        h = Hand()

        c_a = Card('Heart', 'A')
        c_j = Card('Heart', 'J')

        h.add_card(c_a)
        assert h.get_value() == 11

        h.add_card(c_j)
        assert h.get_value() == 21

        h.add_card(c_j)
        assert h.get_value() == 21

        h.add_card(c_a)
        assert h.get_value() == 22

        h.add_card(c_a)
        assert h.get_value() == 23


    def test_hand_calculate_value_ace2(self):
        h = Hand()

        c_a = Card('Heart', 'A')

        h.add_card(c_a)
        h.add_card(c_a)
        assert h.get_value() == 12

        h.add_card(c_a)
        assert h.get_value() == 13
