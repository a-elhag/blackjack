import logging

from src.deck import Deck
from src.hand import Hand
from src.strategy import SimpleStrategy, DealerStrategy

logging.basicConfig(level=logging.DEBUG)

class Round():
    """Blackjack game
    Args:
        num_decks: number of decks
        player_strategy: strategy for player to inject
        dealer_strategy: strategy for dealer to use
    """

    def __init__(self, num_decks, player_strategy, dealer_strategy):
        self.num_decks = num_decks
        self.deck = Deck(self.num_decks)

        self.player_strategy = player_strategy(self.deck)
        self.dealer_strategy = dealer_strategy(self.deck)

        self.default_bet = 5.0
        self.payout_blackjack = 1.5
        self.round_info = {"wins": 0, "ties": 0, "losses": 0, "earnings": 0.0, "rounds": 0}
        self.has_split = False

        self.player_hand = Hand()
        self.dealer_hand = Hand()

        self.flag_deck_done = False


    def calculate_round(self):
        # Step 3: Check if there is a blackjack
        flag_player_blackjack, flag_dealer_blackjack = Round.check_blackjack(
                self.player_hand, self.dealer_hand)
        if flag_player_blackjack and flag_dealer_blackjack:
            """This is a tie (push)"""
            self.round_info["ties"] += 1
            return
        elif flag_dealer_blackjack:
            """Dealer has a blackjack, game automatically ends and player loses 
            their bet"""
            self.round_info["losses"] += 1
            self.round_info["earnings"] -= self.default_bet
            return

        # Step 4: Have the player use their strategy
        self.player_strategy.play(self.player_hand, self.dealer_hand)

        # Step 5: Check if the player busts
        if Round.check_bust(self.player_hand):
            self.round_info["losses"] += 1
            self.round_info["earnings"] -= self.default_bet
            return

        # Step 6: Have the dealer use their strategy
        self.dealer_strategy.play(self.dealer_hand)

        # Step 7: See if there is no cards left (Hand.get_value == -1)
        if self.player_hand.get_value() == -1 or self.dealer_hand.get_value() == -1:
            self.flag_deck_done = True
            return

        # Step 8: Check if the dealer busts
        if Round.check_bust(self.dealer_hand):
            if flag_player_blackjack:
                """Player gets a 'natural win', usually meaning a 3-2 payout"""
                self.round_info["wins"] += 1
                self.round_info["earnings"] += self.default_bet*self.payout_blackjack
                return

            self.round_info["wins"] += 1
            self.round_info["earnings"] += self.default_bet
            return

        # Step 9: Check to see who won
        if self.player_hand.get_value() == self.dealer_hand.get_value():
            self.round_info["ties"] += 1
            return
        elif self.player_hand.get_value() > self.dealer_hand.get_value():
            if flag_player_blackjack:
                """Player gets a 'natural win', usually meaning a 3-2 payout"""
                self.round_info["wins"] += 1
                self.round_info["earnings"] += self.default_bet*self.payout_blackjack
                return
            self.round_info["wins"] += 1
            self.round_info["earnings"] += self.default_bet
            return
        else:
            self.round_info["losses"] += 1
            self.round_info["earnings"] -= self.default_bet
            return


    def new_hand(self):
        """Set up a new hand for the dealer and the player"""
        # Step 0: Reset Hand
        self.player_hand.clear_cards()
        self.dealer_hand.clear_cards()

        # Step 1: Deal inital cards
        for _ in range(2):
            self.player_hand.add_card(self.deck.deal())
            self.dealer_hand.add_card(self.deck.deal())

        # Step 2: Initialize default bet
        self.player_hand.add_bet(self.default_bet)


    def play(self):
        """Play a game
        Returns game obj with stats
        """
        self.round_info["rounds"] += 1

        # Shuffle deck if deck is finished
        self.shuffle_deck()

        # Deal a New Hand
        self.new_hand()

        # Calculate who won
        self.calculate_round()


    def shuffle_deck(self):
        if self.flag_deck_done == True:
            self.deck = Deck(self.num_decks)
            self.deck.shuffle()
            self.deck.cut()
            self.flag_deck_done = False


    @staticmethod
    def check_blackjack(player_hand, dealer_hand):
        """Check if player or the dealer has blackjack
        Args:
            player_hand: hand of player
            dealer_hand: hand of dealer
        Returns:
            flag_player_blackjack: TRUE if player has blackjack
            flag_dealer_blackjack: TRUE if dealer has blackjack
        """

        flag_player_blackjack = bool(player_hand.get_value() == 21)
        flag_dealer_blackjack = bool(dealer_hand.get_value() == 21)

        return flag_player_blackjack, flag_dealer_blackjack


    @staticmethod
    def check_bust(hand):
        """Check if the hand is greater than 21 (bust)
        Args:
            hand: hand to check
        """
        return bool(hand.get_value() > 21)


    def display_a_hand(self):
        self.play()
        logging.debug("(Player) " + self.player_hand.__str__())
        logging.debug("(Dealer) " + self.dealer_hand.__str__())
        logging.debug("(Results) " + str(self.round_info))
        

def main():
    d = Deck(1)
    d.shuffle()
    d.cut()

    r = Round(d, SimpleStrategy, DealerStrategy)

    for _ in range(5):
        r.display_a_hand()


if __name__ == "__main__":
    main()
