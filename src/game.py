import logging

from src.round import Round
from src.strategy import SimpleStrategy, DealerStrategy

logging.basicConfig(level=logging.DEBUG)


if __name__ == "__main__":
    r = Round(6, SimpleStrategy, DealerStrategy)

    for _ in range(10000):
        r.play()
        r.round_info

    logging.debug(r.round_info)
    total = r.round_info['wins'] + r.round_info['ties'] + r.round_info['losses']
    logging.debug(f"\nRounds Played: {total}\nTotal Rounds: {r.round_info['rounds']}")
