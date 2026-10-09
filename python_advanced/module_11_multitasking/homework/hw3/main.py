import logging
import random
import threading
import time

TOTAL_TICKETS = 10
MAX_SEATS = 100
TICKET_THRESHOLD = 4
ADD_TICKETS = 6

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)


class Director(threading.Thread):
    """Главный директор с печатным станком."""

    def __init__(self, ticket_lock: threading.Lock):
        super().__init__(name='Director')
        self.ticket_lock = ticket_lock
        self.printed_batches = 0

    def run(self):
        global TOTAL_TICKETS
        logger.info('Director started monitoring tickets')

        while TOTAL_TICKETS <= MAX_SEATS:
            time.sleep(random.uniform(0.5, 2.0))

            with self.ticket_lock:
                if TOTAL_TICKETS <= TICKET_THRESHOLD and TOTAL_TICKETS < MAX_SEATS:
                    old_tickets = TOTAL_TICKETS
                    add = min(ADD_TICKETS, MAX_SEATS - TOTAL_TICKETS)
                    TOTAL_TICKETS += add
                    self.printed_batches += 1
                    logger.info(f'Director printed {add} tickets: {old_tickets} → {TOTAL_TICKETS}')

        logger.info(f'Director finished: printed {self.printed_batches} batches')


class Seller(threading.Thread):
    def __init__(self, ticket_lock: threading.Lock, seller_sem: threading.Semaphore):
        super().__init__()
        self.ticket_lock = ticket_lock
        self.seller_sem = seller_sem
        self.tickets_sold = 0
        logger.info(f'Seller {self.getName()} started work')

    def run(self):
        global TOTAL_TICKETS
        while True:
            self.random_sleep()

            with self.seller_sem:
                with self.ticket_lock:
                    if TOTAL_TICKETS <= 0:
                        logger.info(f'Seller {self.getName()} finished: no tickets left')
                        break
                    self.tickets_sold += 1
                    TOTAL_TICKETS -= 1
                    logger.info(f'{self.getName()} sold one; {TOTAL_TICKETS} left')

        logger.info(f'Seller {self.getName()} sold {self.tickets_sold} tickets TOTAL')

    def random_sleep(self):
        time.sleep(random.randint(0, 1))


def main():
    ticket_lock = threading.Lock()
    seller_sem = threading.Semaphore(3)

    sellers = [Seller(ticket_lock, seller_sem) for _ in range(4)]
    director = Director(ticket_lock)

    director.start()
    for seller in sellers:
        seller.start()

    director.join()
    for seller in sellers:
        seller.join()

    logger.info('All finished')


if __name__ == '__main__':
    main()