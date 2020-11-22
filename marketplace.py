"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2020
"""


class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """
    def __init__(self, queue_size_per_producer):
        """
        Constructor

        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """
        # Numarul maxim de produse,
        # pe care le poate avea un producator pe "raft"
        self.max_size = queue_size_per_producer
        # ID-ul producatorului = -1 pentru ca nu s-a inregistrat niciun producer
        self.producer_id = -1
        # ID-ul cosului = -1 pentru ca nu avem niciun cos oferit
        self.cart_id = -1
        # Lista de cart-uri
        self.carts = list()
        # Lista de produse publicate in marketplace
        self.market = list()

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        # Am marcat inregistrarea producer-ului
        self.producer_id += 1
        # Am oferit producer-ului un "raft" in market
        self.market.insert(self.producer_id, list())

        # Am returnat id-ul folosit pentru producer-ul curent
        return self.producer_id

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """
        # Daca producer-ul nu mai are loc pe "raft",
        # va fi anuntat ca produsul sau nu a fost adaugat
        if len(self.market[producer_id]) >= self.max_size:
            return False

        # Daca mai este loc disponibil,
        # se adauga produsul pe raftul producatorului
        self.market[producer_id].append(product)

        # Produs publicat cu succes
        return True

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        # Am marcat oferirea unui cos de cumparaturi
        self.cart_id += 1
        # Am adaugat cart-ul consumer-ului in lista de cart-uri
        self.carts.insert(self.cart_id, list())

        # Am returnat id-ul cart-ului curent
        return self.cart_id

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """
        # Am retinut numarul de produse din market,
        # pentru a putea avea acces la id-ul producatorului
        # in timpul parcurgerii
        m_len = len(self.market)
        # Am folosit found pentru a marca faptul ca am gasit sau nu
        # produsul cautat in lista cu produse
        found = False

        # Am parcurs fiecare producator in ordinea inregistrarii
        for producer_id in range(0, m_len):
            producer = self.market[producer_id]

            # Am parcurs produsele fiecatrui producator
            for prod in producer:
                # Daca produsul pe care vreau sa il adaug
                # se afla pe raft-ul producatorului curent
                if prod == product:
                    # Am marcat gasirea produsului
                    found = True
                    # Am eliminat produsul de pe raft-ul producatorului,
                    # pentru ca aceasta urma sa fie adaugat in cart-ul consumer-ului
                    self.market[producer_id].remove(product)

                    # Am abandonat cautarea, intrucat am gasit produsul cautat
                    break

            # Inainte sa trecem la urmatorul producer,
            # verificam daca a fost gasit produsul cautat
            if found:
                # Abandonam cautarea in cazul in care produsul a fost gasit
                break

        # Daca produsul nu a fost gasit,
        # se va informa consumatorul in acest sens
        if not found:
            return False

        # Daca produsl a fost gasit,
        # l-am adaugat in cart-ul consumatorului
        # si am specificat producatorul de la care provine (id)
        self.carts[cart_id].append((producer_id, product))

        # Am informat consumer-ul ca produsul a fost adaugat in cart cu succes
        return True


    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """
        # Am extras cart-ul consumatorului cu id-ul primit ca argument
        cart = self.carts[cart_id]
        # Variabila pentru retinerea succesului / insuccesului cautarii
        found = False
        # Elementul curent din cosul cu produse
        item = (0, 0)

        # Am parcurs produsele din cart
        for item in cart:
            # Daca am gasit produsul cautat
            if item[1] == product:
                # Am marcat gasirea produsului
                found = True
                # Am terminat cautarea
                break

        # Daca am gasit produsul
        if found:
            # L-am eliminat din cos
            self.carts[cart_id].remove(item)
            # L-am adaugat pe raftul producatorului caruia ii apartine
            producer_id = item[0]
            product = item[1]
            self.market[producer_id].append(product)


    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        # Am returnat cart-ul consumer-ului cu id-ul specificat ca argument
        return self.carts[cart_id]
