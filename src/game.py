import logging

from src.round import Round
from src.strategy import SimpleStrategy, DealerStrategy

logging.basicConfig(level=logging.DEBUG)



if __name__ == "__main__":
    r = Round(6, SimpleStrategy, DealerStrategy)

    no_sim = 100000
    total_n = [0, 0]

    for _ in range(no_sim):
        r.play()
        r.round_info

    logging.debug(r.round_info)
    total = r.round_info['wins'] + r.round_info['ties'] + r.round_info['losses']
    logging.debug(f"\nTotal Rounds: {total}\nTotal Simulated: {no_sim}\nTotal Rounds: {r.round_info['rounds']}")
    
    
    
