"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2020
"""

from threading import Thread
from time import sleep

class Consumer(Thread):
    """
    Class that represents a consumer.
    """

    def __init__(self, carts, marketplace, retry_wait_time, **kwargs):
        """
        Constructor.

        :type carts: List
        :param carts: a list of add and remove operations

        :type marketplace: Marketplace
        :param marketplace: a reference to the marketplace

        :type retry_wait_time: Time
        :param retry_wait_time: the number of seconds that a producer must wait
        until the Marketplace becomes available

        :type kwargs:
        :param kwargs: other arguments that are passed to the Thread's __init__()
        """
        # Am deschis un thread pentru fiecare Consumer
        # Am initializat carts, marketplace, retry_wait_time si kwargs,
        # cu valorile primite ca argument
        Thread.__init__(self, **kwargs)
        self.carts = carts
        self.marketplace = marketplace
        self.retry_wait_time = retry_wait_time
        self.kwargs = kwargs

    def run(self):
        # Pentru fiecare lista a cumparatorului
        for cart in self.carts:
            # Am cerut un cos pentru cumparaturi
            cart_id = self.marketplace.new_cart()
            # Pentru fiecare produs de pe lista
            for prod in cart:
                # Am extras cantitatea ceruta pentru produsul curent
                qty = prod['quantity']

                # Daca actiunea indicata produsului era de adaugare
                if prod['type'] == 'add':
                    # Cat timp nu s-a adaugat toata cantitatea ceruta
                    while qty:
                        # Cat timp produsul nu a fost adaugat
                        while not self.marketplace.add_to_cart(cart_id, prod['product']):
                            # Asteptam disponibilitatea acestuia
                            sleep(self.retry_wait_time)

                        # Daca s-a iesit din while, produsul a fost adaugat cu succes si
                        # am scazut numarul de produse adaugate
                        qty -= 1

                # Daca tipul comenzii este remove
                if prod['type'] == 'remove':
                    # Cat timp nu s-a eliminat cantitatea ceruta spre eliminare
                    while qty:
                        # Am inlaturat un produs din cos
                        self.marketplace.remove_from_cart(cart_id, prod['product'])

                        # Am marcat eliminarea produsului
                        qty -= 1

            # Cand am terminat de parcurs lista de cumparaturi,
            # am plasat comanda, primind la schimb produsele
            order = self.marketplace.place_order(cart_id)

            # Am afisat fiecare produs cumparat de pe lista curenta
            for product in order:
                print("%s bought %s" % (self.kwargs['name'], product[1]))
