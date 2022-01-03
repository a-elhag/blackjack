"""Module for hands"""

class Hand():
    """Basic hand gameplay
    """

    def __init__(self):
        self.cards = []
        self.value = 0
        self.bet = 0.0


    def __str__(self):
        cards = "Cards: "
        cards = cards + " ".join([card.__str__() for card in self.cards])
        cards = cards + " (" + str(self.get_value()) + ")"
        bet = "Bet: " + str(self.bet)

        output = cards + "\n" + bet
        return output


    def add_card(self, card):
        """Add card to given hand
        Args:
            card: card to add
        """
        self.cards.append(card)


    def add_bet(self, bet):
        """Add bet amount to given hand
        Args:
            bet: bet to add
        """
        if bet < 0:
            raise ValueError(f'Bet should be positive and it is currently: {bet}')
        self.bet = bet;


    def calculate_value(self):
        """Calculate value of the hand
        """

        self.value = 0

        counter_ace = 0
        for card in self.cards:
            if card.value.isnumeric():
                self.value += int(card.value)
            else:
                if card.value == "A":
                    counter_ace += 1
                    self.value += 11

                else:
                    self.value += 10

        if counter_ace > 0:
            while (self.value > 21):
                if counter_ace == 0:
                    break
                self.value -= 10
                counter_ace -= 1


    def get_value(self):
        """Calculate value of hand and then return it"""

        self.calculate_value()
        return self.value
