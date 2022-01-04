import logging
from pyjack.deck import Deck
from pyjack.hand import Hand
from pyjack.strategy import SimpleStrategy, DealerStrategy

logging.basicConfig(level=logging.DEBUG)

class Game():
    """Blackjack game
    Args:
        deck: finalized deck to use
        player_strategy: strategy for player to inject
        dealer_strategy: strategy for dealer to use
    """

    def __init__(self, deck, player_strategy, dealer_strategy):
        self.deck = deck
        self.player_strategy = player_strategy(deck)
        self.dealer_strategy = dealer_strategy(deck)
        self.default_bet = 5.0
        self.payout_blackjack = 1.5
        self.game_info = {"wins": 0, "ties": 0, "losses": 0, "earnings": 0.0}
        self.has_split = False


    def new_hand(self):
        """Set up a new hand for the dealer and the player"""
        # Step 0: Initialize
        player_hand = Hand()
        dealer_hand = Hand()

        # Step 1: Deal inital cards
        for _ in range(2):
            player_hand.add_card(self.deck.deal())
            dealer_hand.add_card(self.deck.deal())

        # Step 2: Initialize default bet
        player_hand.add_bet(self.default_bet)

        return player_hand, dealer_hand

    def play(self):
        """Play a game
        Returns game obj with stats
        """

        self.player_hand, self.dealer_hand = self.new_hand()

        # Step 3: Check if there is a blackjack
        flag_player_blackjack, flag_dealer_blackjack = Game.check_blackjack(
                self.player_hand, self.dealer_hand)
        if flag_player_blackjack and flag_dealer_blackjack:
            """This is a tie"""
            self.game_info["ties"] += 1
            return
        elif flag_player_blackjack:
            """Player gets a 'natural win', usually meaning a 3-2 payout"""
            self.game_info["wins"] += 1
            self.game_info["earnings"] += self.default_bet*self.payout_blackjack
            return
        elif flag_dealer_blackjack:
            """Dealer has a blackjack, game automatically ends and player loses 
            their bet"""
            self.game_info["losses"] += 1
            self.game_info["earnings"] -= self.default_bet
            return

        # Step 4: Have the player use their strategy
        self.player_strategy.play(self.player_hand, self.dealer_hand)

        # Step 5: Check if the player busts
        if Game.check_bust(self.player_hand):
            self.game_info["losses"] += 1
            self.game_info["earnings"] -= self.default_bet
            return

        # Step 6: Have the dealer use their strategy
        self.dealer_strategy.play(self.dealer_hand)

        # Step 7: Check if the dealer busts
        if Game.check_bust(self.dealer_hand):
            self.game_info["wins"] += 1
            self.game_info["earnings"] += self.default_bet
            return

        # Step 8: Check to see who won
        if self.player_hand.get_value() == self.dealer_hand.get_value():
            self.game_info["ties"] += 1
            return
        elif self.player_hand.get_value() > self.dealer_hand.get_value():
            self.game_info["wins"] += 1
            self.game_info["earnings"] += self.default_bet
            return
        else:
            self.game_info["losses"] += 1
            self.game_info["earnings"] -= self.default_bet
            return


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
        logging.debug("(Player) " + g.player_hand.__str__())
        logging.debug("(Dealer) " + g.dealer_hand.__str__())
        logging.debug("(Results) " + str(self.game_info))
        


d = Deck(1)
d.shuffle()
d.cut()

g = Game(d, SimpleStrategy, DealerStrategy)

for _ in range(5):
    g.display_a_hand()
