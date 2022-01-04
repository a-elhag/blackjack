import logging
import math
from multiprocessing import Process, cpu_count, Queue
import time

from src.round import Round
from src.strategy import SimpleStrategy, DealerStrategy


def game(queue, batch_size, num_decks):
    """Run single batch of simulations
    Args:
        batch_size: the batch size of games to run
        num_decks: number of decks to use
    Adds results of sims to queue
    """
    batch_info = {"ties": 0, "wins": 0, "losses": 0, "earnings": 0, "rounds": 0}

    r = Round(num_decks, SimpleStrategy, DealerStrategy)
    for _ in range(batch_size):
        r.play()
        r.round_info

    batch_info["ties"] = r.round_info["ties"]
    batch_info["wins"] = r.round_info["wins"]
    batch_info["losses"] = r.round_info["losses"]
    batch_info["earnings"] = r.round_info["earnings"]
    batch_info["rounds"] = r.round_info["rounds"]
    queue.put(batch_info)


if __name__ == "__main__":
    num_sims = 1e5
    num_decks = 6

    start_time = time.time()
    cpus = cpu_count()
    batch_size = int(math.ceil(num_sims / float(cpus)))
    queue = Queue()

    processes = []
    for _ in range(cpus):
        process = Process(target=game, args=(queue, batch_size, num_decks))
        processes.append(process)
        process.start()

    for proc in processes:
        proc.join()

    finish_time = time.time() - start_time

    ties, wins, losses, total, rounds, earnings = 0, 0, 0, 0, 0, 0.0
    for _ in range(0, cpus):
        results = queue.get()
        wins += results["wins"]
        ties += results["ties"]
        losses += results["losses"]
        rounds += results["rounds"]
        earnings += results["earnings"]
    total = wins + ties + losses

    logging.info(f'wins: {wins}')
    logging.info(f'ties: {ties}')
    logging.info(f'losses: {losses}')
    logging.info(f'total: {total}')
    logging.info(f'rounds: {rounds}')
    logging.info(f'earnings: {earnings}\n')

    logging.info('Simulations per second: %d', (float(num_sims) / finish_time))
    logging.info('Execution time: %.2fs\n', finish_time)

    logging.info('Hand win percentage: %.2f%%', ((wins / float(total)) * 100))
    logging.info('Hand draw percentage: %.2f%%', ((ties / float(total)) * 100))
    logging.info('Hand lose percentage: %.2f%%\n', ((losses / float(total)) * 100))

    logging.info('Total Earnings: %.2f', earnings)
    logging.info('Expected Earnings per hand: %.2f\n', (earnings / total))
