#!/usr/bin/python
# -*- coding: utf-8 -*-

#############################################################
# module: spender.py
# descrip: the spender of the digital cash system.
# bugs to vladimir kulyukin via canvas
##############################################################

import random
from pubrepo import pubrepo
from ntutils import mult_inv

class spender(object):

    def __init__(self):
        ### The spender chooses a secret identity u (cf. Slide 19).
        self.__u  = random.randint(3, 15)
        ### The spender keeps track of the spent coins.
        self.__spent_coins = set()
        ### This is the current unspent coin
        self.__unspent_coin = None
        ### This is the secret random 5 tuple created by
        ### the spender for each requested coin (cf. Slide 22).
        self.__secret_5_tup = None
        
    def create_bank_account(self, bnk, pbr):
        ### the sponder computes I by looking up g1 and p in public repo pbr
        ### and sends I to the bank bnk. (cf. Slide 19).
        self.__I = (pbr.get_g1()**self.__u) % pbr.get_p()
        ### the bank sends z' to the spender (cf. Slide 19) after
        ### it creates the spender's account.
        print('Spender {} requested Bank to create a spender account.'.format(self.__I))
        self.__z_prime = bnk.create_spender_account(self.__I, pbr)
        print('Spender {} received z_prime {} from Bank.'.format(self.__I, self.__z_prime))

    def __gen_secret_5_tup(self, pbr):
        """
        a generator for a random 5 tuple created by the spender.
        Cf. Slide 22. 
        """
        s = random.randint(3, 101)
        A = ((self.__I*pbr.get_g2())**s) % pbr.get_p()        
        while A == 1:
            s = random.randint(3, 101)
            print('I == {}'.format(self.__I))
            print('g2 == {}'.format(pbr.get_g2()))
            print('p == {}'.format(pbr.get_p()))
            print('s == {}'.format(s))
            A = ((self.__I*pbr.get_g2())**s) % pbr.get_p()
        x1, x2, alpha1, alpha2 = tuple(random.randint(3, 15) for i in range(4))
        print('Spender created secret random 5-tuple {}'.format(((s, x1, x2, alpha1, alpha2))))
        return (s, x1, x2, alpha1, alpha2)

    def request_coin(self, bnk, pbr):
        """
        The spender requests that a coin be created by the bank.
        Cf. Slides 22, 23.
        """
        ## the bank computes gw and beta and sends it to Spender
        print('Spender {} requested gw and beta from Bank.'.format(self.__I))
        gw, beta = bnk.compute_gw_beta(self.__I, pbr)
        ## The Spender generates a secret random 5-tuple. A new 5-tuple for every newly issued
        ## coin.
        s, x1, x2, alpha1, alpha2 = self.__gen_secret_5_tup(pbr)
        self.__secret_5_tup = s, x1, x2, alpha1, alpha2
        A = (self.__I*pbr.get_g2())**s % pbr.get_p()
        assert A != 1
        B = ((pbr.get_g1()**x1)*(pbr.get_g2()**x2)) % pbr.get_p()
        z = (self.__z_prime)**s % pbr.get_p()
        a = ((gw**alpha1)*(pbr.get_g()**alpha2)) % pbr.get_p()
        b = ((beta**(s*alpha1))*(A**alpha2)) % pbr.get_p()

        ### The Spender computes c ≡ alpha1^{−1} H(A, B, z, a, b) (mod q) and sends c
        ### to the bank. Cf. Slides 24, 25
        mult_inv_alpha1 = mult_inv(alpha1, pbr.get_q())
        c = (mult_inv_alpha1 * pbr.get_H()((A,B,z,a,b))) % pbr.get_q()
        print('Spender {} computed c == {}.'.format(self.__I, c))
        
        ### The Spender requests that the bank compute c1
        ### to create a coin. Cf. Slides 24, 25
        print('Spender {} requested c1 Bank.'.format(self.__I))
        c1 = bnk.compute_c1(self.__I, c, gw, pbr)
        ### The Spender computes r = (alpha1*c1 + alpha2) (mod q).
        r = (alpha1*c1 + alpha2) % pbr.get_q()
        print('Spender {} computed r == {}.'.format(self.__I, r))        
        ### the Spender now has one newly issued unspent coin
        self.__unspent_coin = (A,B,z,a,b,r)
        print('Spender {} received the unspent coin {}.'.format(self.__I, self.__unspent_coin))

    def spend_unspent_coin(self, mrt, pbr):
        """
        The newly issued unspent coin is spent by the spender at the merchant.
        """
        ### spender receives d from the merchant (cf. SLide 27).
        print('Spender {} requested Merchant {} to compute d'.format(self.__I, mrt.get_id()))
        d = mrt.compute_d(self.__unspent_coin, pbr)
        assert d is not None
        ### spender computes r1 and r2 (cf. Slide 27).
        s, x1, x2, _, _ = self.__secret_5_tup
        q = pbr.get_q()
        r1 = (d*self.__u*s + x1) % q
        r2 = (d*s + x2) % q
        ### spender requests the merchant to accept the coin
        ### r1, r2, and d are the coin signature.
        print('Spender {} requested Merchant {} to accept coin {} with signature {}'.format(self.__I,
                                                                                            mrt.get_id(),
                                                                                            self.__unspent_coin,
                                                                                            (r1, r2, d)))
        mrt.accept_coin(self.__unspent_coin, r1, r2, d, pbr)
        ### the sepnder adds the coin, the coin's signature, and the
        ### secret random 5 tuple for bookeeping to the set of spent coins.
        self.__spent_coins.add((self.__unspent_coin, (r1, r2, d), self.__secret_5_tup))
        ### the unspent coin is set to None.
        self.__unspent_coin = None

    def get_balance(self, bnk):
        return bnk.balance_for_spender_account(self.__I)

    def double_spend_coin(self, vdr, pbr):
        """
        Spender attempts to double spend a coin with the vendor vndr.
        Cf. Slides 32, 33, 34.
        """
        ### 1. get a spent coin from self.__spent_coins
        spent_coin = self.__spent_coins.pop()[0]
        print('Spender {} attempts to double spend coin = {}'.format(self.__I, spent_coin))
        
        ### 2. the spender requests the vendor to compute d_prime.
        ###    with compute_d() above.
        d_prime = vdr.compute_d(spent_coin, pbr)
        print('d_prime = {}'.format(d_prime))
        assert d_prime is not None
        
        ### 3. the spender computes r1_prime, r2_prime
        ### your code here
        s, x1, x2, _, _ = self.__secret_5_tup
        q = pbr.get_q()
        r1_prime = (d_prime*self.__u*s + x1) % q
        r2_prime = (d_prime*s + x2) % q

        ### 4. the spender requests the vendor to accept the spent coin.
        ###    with accept_coin() defined above. 
        vdr.accept_coin(spent_coin, r1_prime, r2_prime, d_prime, pbr)

    def reveal_secret_id(self):
        """
        This is for debugging and unit tests purposes only. It will never be defined in
        practice.
        """
        return self.__u
        
