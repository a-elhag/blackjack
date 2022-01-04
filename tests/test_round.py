import pytest

from src.card import Card
from src.deck import Deck
from src.hand import Hand
from src.strategy import SimpleStrategy, DealerStrategy
from src.round import Round

class TestRound:
    def test_round_init(self):
        r = Round(6, SimpleStrategy, DealerStrategy)


    def test_round_new_hand(self):
        r = Round(1, SimpleStrategy, DealerStrategy)
        r.new_hand()

        assert r.player_hand.cards[0].suit == 'Spade'
        assert r.player_hand.cards[0].value == 'A'
        assert r.player_hand.cards[1].suit == 'Spade'
        assert r.player_hand.cards[1].value == '3'

        assert r.dealer_hand.cards[0].suit == 'Spade'
        assert r.dealer_hand.cards[0].value == '2'
        assert r.dealer_hand.cards[1].suit == 'Spade'
        assert r.dealer_hand.cards[1].value == '4'


    def test_round_check_blackjack(self):
        c_2 = Card('Club', '3')
        c_j = Card('Heart', 'J')
        c_A = Card('Club', 'A')

        h_player_nobj = Hand()
        h_player_nobj.add_card(c_2) 
        h_player_nobj.add_card(c_A) 

        h_dealer_nobj = Hand()
        h_dealer_nobj.add_card(c_2) 
        h_dealer_nobj.add_card(c_A) 

        h_player_bj = Hand()
        h_player_bj.add_card(c_j) 
        h_player_bj.add_card(c_A) 

        h_dealer_bj = Hand()
        h_dealer_bj.add_card(c_j) 
        h_dealer_bj.add_card(c_A) 

        flag_player_nobj, flag_dealer_nobj = Round.check_blackjack(
                h_player_nobj, h_dealer_nobj)

        flag_player_bj, flag_dealer_bj = Round.check_blackjack(
                h_player_bj, h_dealer_bj)

        assert flag_player_nobj == False
        assert flag_dealer_nobj == False
        assert flag_player_bj == True
        assert flag_dealer_bj == True


    def test_round_check_bust(self):
        c_2 = Card('Club', '3')
        c_j = Card('Heart', 'J')
        c_A = Card('Club', 'A')

        h_no_bust = Hand()
        h_no_bust.add_card(c_2) 
        h_no_bust.add_card(c_A) 

        h_bust = Hand()
        h_bust.add_card(c_j) 
        h_bust.add_card(c_j) 
        h_bust.add_card(c_j) 
        h_bust.add_card(c_A) 

        assert Round.check_bust(h_no_bust) == False
        assert Round.check_bust(h_bust) == True


    def test_round_play_init(self):
        r = Round(1, SimpleStrategy, DealerStrategy)

        assert r.round_info["wins"] == 0
        assert r.round_info["ties"] == 0
        assert r.round_info["losses"] == 0


    def test_round_play_loss(self):
        g = Round(1, SimpleStrategy, DealerStrategy)

        g.play()

        assert g.round_info["wins"] == 0
        assert g.round_info["ties"] == 0
        assert g.round_info["losses"] == 1


    def test_round_play_tie(self):
        r = Round(1, SimpleStrategy, DealerStrategy)
        
        for idx in range(4):
            r.deck.set_card(idx, "Club", "J")

        r.play()

        assert r.round_info["wins"] == 0
        assert r.round_info["ties"] == 1
        assert r.round_info["losses"] == 0


    def test_round_play_win(self):
        g = Round(1, SimpleStrategy, DealerStrategy)
        
        # Player gets cards first
        g.deck.set_card(0, "Heart", "J")
        # Then dealer
        g.deck.set_card(1, "Club", "8")
        # Then player
        g.deck.set_card(2, "Club", "J")
        # Then finally dealer
        g.deck.set_card(3, "Club", "J")


        g.play()

        # Player should win since dealer definitely cannot hit above 17
        assert g.round_info["wins"] == 1
        assert g.round_info["ties"] == 0
        assert g.round_info["losses"] == 0


    def test_round_play_blackjack_dealer(self):
        g = Round(1, SimpleStrategy, DealerStrategy)
        
        # Player gets cards first
        g.deck.set_card(0, "Heart", "2")
        # Then dealer
        g.deck.set_card(1, "Club", "J")
        # Then player
        g.deck.set_card(2, "Club", "2")
        # Then finally dealer
        g.deck.set_card(3, "Club", "A")

        g.play()

        # Dealer should automatically win since they have a blackjack
        assert g.round_info["wins"] == 0
        assert g.round_info["ties"] == 0
        assert g.round_info["losses"] == 1

        # Also, player should not have had time to implement their strategy
        # Thus they should still have the exact same hand that they started with

        assert g.player_hand.get_value() == 4


    def test_round_play_blackjack_player(self):
        g = Round(1, SimpleStrategy, DealerStrategy)
        
        # Player gets cards first
        g.deck.set_card(0, "Heart", "J")
        # Then dealer
        g.deck.set_card(1, "Club", "J")
        # Then player
        g.deck.set_card(2, "Club", "A")
        # Then finally dealer
        g.deck.set_card(3, "Club", "5")
        # Dealer will draw this last card since they are below < 17
        g.deck.set_card(4, "Diamond", "3")

        g.play()

        # Player should win since they have a blackjack
        assert g.round_info["wins"] == 1
        assert g.round_info["ties"] == 0
        assert g.round_info["losses"] == 0

        # And player should get the default payout multiplied by the payout for blackjack
        assert g.round_info["earnings"] == g.default_bet * g.payout_blackjack


        # And the dealer should have drawn up to 18
        assert g.dealer_hand.get_value() == 18


    def test_round_play_blackjack_push(self):
        g = Round(1, SimpleStrategy, DealerStrategy)
        
        # Player gets cards first
        g.deck.set_card(0, "Heart", "J")
        # Then dealer
        g.deck.set_card(1, "Club", "J")
        # Then player
        g.deck.set_card(2, "Club", "A")
        # Then finally dealer
        g.deck.set_card(3, "Club", "A")

        g.play()

        # Should be a tie
        assert g.round_info["wins"] == 0
        assert g.round_info["ties"] == 1
        assert g.round_info["losses"] == 0


    def test_round_play_dealer_bust(self):
        g = Round(1, SimpleStrategy, DealerStrategy)
        
        # Player gets cards first
        g.deck.set_card(0, "Heart", "J")
        # Then dealer
        g.deck.set_card(1, "Club", "J")
        # Then player
        g.deck.set_card(2, "Club", "K")
        # Then finally dealer
        g.deck.set_card(3, "Club", "6")
        # Then finally dealer
        g.deck.set_card(4, "Club", "Q")

        g.play()

        # The dealer should bust
        assert g.round_info["wins"] == 1
        assert g.round_info["ties"] == 0
        assert g.round_info["losses"] == 0

        assert g.dealer_hand.get_value() == 26
