"""Main module"""
import logging
from pyjack.deck import Deck
from pyjack.game import Game
from pyjack.strategy import SimpleStrategy, DealerStrategy

logging.basicConfig(level=logging.DEBUG)

def new_deck(num_decks):
    """Create new deck, shuffle it and cut it
    Args:
        num_decks: number of decks to use for the shuffle
    """

    deck = Deck(num_decks)
    deck.shuffle()
    deck.cut()
    return deck


def simulate(batch_size, num_decks, shuffle_perc):
    """Run single batch of simulations
    Args:
        batch_size: the batch size of games to run
        num_decks: number of decks to use in the game
        shuffle_perc: at percentage used, reshuffle deck
    Adds results of sims to queue
    """
    deck = new_deck(num_decks)

    batch_info = {"wins": 0, "ties": 0, "losses": 0, "earnings": 0, "num_hands": 0}

    for _ in range(batch_size):
        game = Game(deck, SimpleStrategy, DealerStrategy)
        # re-shuffle new deck 
        if (float(len(game.deck.cards)) / (52 * num_decks)) < shuffle_perc:
            game.deck = new_deck(num_decks)

        game.play()
        batch_info["ties"] += game.game_info["ties"]
        batch_info["wins"] += game.game_info["wins"]
        batch_info["losses"] += game.game_info["losses"]
        batch_info["earnings"] += game.game_info["earnings"]

    batch_info["num_hands"] += (batch_info["wins"] + batch_info["losses"] + batch_info["ties"])
    return batch_info

def main():
    """Main method"""
    batch_info = simulate(100000, 6, 0.75)
    logging.debug(batch_info)

if __name__ == "__main__":
    main()
