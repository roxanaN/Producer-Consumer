"""
This module represents the Producer.

Computer Systems Architecture Course
Assignment 1
March 2020
"""

from threading import Thread
from time import sleep

class Producer(Thread):
    """
    Class that represents a producer.
    """

    def __init__(self, products, marketplace, republish_wait_time, **kwargs):
        """
        Constructor.

        @type products: List()
        @param products: a list of products that the producer will produce

        @type marketplace: Marketplace
        @param marketplace: a reference to the marketplace

        @type republish_wait_time: Time
        @param republish_wait_time: the number of seconds that a producer must
        wait until the marketplace becomes available

        @type kwargs:
        @param kwargs: other arguments that are passed to the Thread's __init__()
        """
        # Am deschis un thread pentru fiecare Producer
        # Am initializat products, marketplace, retry_wait_time si kwargs,
        # cu valorile primite ca argument
        Thread.__init__(self, **kwargs)
        self.products = products
        self.marketplace = marketplace
        self.republish_wait_time = republish_wait_time
        self.kwargs = kwargs

    def run(self):
        # Am inregistrat producatorul in marketplace,
        # obtinand un id pentru acesta
        producer_id = self.marketplace.register_producer()

        # Am asigurat publicarea permanenta de produse
        while True:
            # Pentru fiecare produs pe care un producator trebuie sa il fabrice
            for prod in self.products:
                # Am extras tipul produsului
                product = prod[0]
                # Am extras  numarul de produse necesare, de acel tip
                qty = prod[1]
                # Am extras timpul de asteptare pana se trece la urmatorul produs
                time = prod[2]

                # Cat timp nu s-au publicat suficiente produse
                while qty:
                    # Cat timp produsul nu a fost adaugat,
                    # deoarece "raftul" marketplace-ului este plin
                    while not self.marketplace.publish(producer_id, product):
                        # Asteptam un timp si reincercam
                        sleep(self.republish_wait_time)

                    # Daca s-a iesit din while, produsul a fost publicat si
                    # trebuie sa asteptam un timp, pentru a trece la urmatorul produs
                    sleep(time)

                    # Am scazut numarul de produse adaugate
                    qty -= 1
