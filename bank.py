#!/usr/bin/python
# -*- coding: utf-8 -*-

#############################################################
# module: bank.py
# descrip: the bank of the digital cash system.
# bugs to vladimir kulyukin via canvas
##############################################################

import random
from pubrepo import pubrepo
from ntutils import mult_inv

class bank(object):

    def __init__(self):
        ### Initialization steps by the Bank on Slides 17,18.
        ### The bank chooses its secret identiy x.
        self.__x = 19
        ### The bank creates a table of spender accounts
        self.__spender_accounts = {}
        ### The bank creates a table of merchant accounts
        self.__merchant_accounts = {}
        ### The bank keeps track of the spent coins
        ### by mapping coins to their signatures.
        self.__spent_coins = {}
        ### The bank keeps track of generated w numbers
        ### for each coin (cf. Slide 21)
        self.__ws = set()
        ### the bank keeps track of generated gws for each
        ### coin. (cf. Slide 21).
        self.__gws = {}

    def create_h_h1_h2(self, pbr):
        """
        The creation by the Bank of h, h1, and h2 (cf. Slides 17, 18.
        pbr is a public repo object.
        """
        p  = pbr.get_p()
        h  = (pbr.get_g()**self.__x)  % p
        h1 = (pbr.get_g1()**self.__x) % p
        h2 = (pbr.get_g2()**self.__x) % p

        ### publish h, h1, h2 in the public repo.
        pbr.set_h(h)
        pbr.set_h1(h1)
        pbr.set_h2(h2)

        self.__display_init_results(pbr)

    def __display_init_results(self, pbr):
        print('*** Bank initialization done...')
        h = pbr.get_h()
        h1 = pbr.get_h1()
        h2 = pbr.get_h2()
        print('h  == {}'.format(h))
        print('h1 == {}'.format(h1))
        print('h2 == {}'.format(h2))
        

    def create_spender_account(self, I, pbr, num_credit_units = 10):
        ### by default each bank acount is credited with 10 units, each
        ### of which corresponds to 1 coin.
        assert num_credit_units == 10
        ### 1. the bank computes z' (cf. Slide 19) by looking up
        ### g2 and p in public repo pbr and using its secret idenity x
        ### and the number I provided by the spender.
        z_prime  = ((I*pbr.get_g2())**self.__x) % pbr.get_p()
        ### The bank maps I to the number of credit units.
        self.__spender_accounts[I] = num_credit_units
        print('Bank created the spender account {} with {} credit units'.format(I, num_credit_units))
        print('Bank computed z_prime == {}'.format(z_prime))
        return z_prime

    def create_merchant_account(self, account_id):
        """
        merchant accounts are created w/ 0 credits.
        """
        self.__merchant_accounts[account_id] = 0
        print('Bank created the merchant account {} with 0 credit units'.format(account_id))

    def __gen_w(self):
        """
        a generator for w created for each coin.
        """
        while True:
            w = random.randint(5, 15)
            if w not in self.__ws:
                self.__ws.add(w)
                print('Bank computed w == {}'.format(w))
                return w

    def compute_gw_beta(self, I, pbr):
        """
        The bank creats gw and beta (cf. Slide 21).
        g, g2, and p are looked up in public repo pbr.
        I is created by the spender.
        """
        w = self.__gen_w()
        gw   = (pbr.get_g()**w) % pbr.get_p()
        beta = ((I*pbr.get_g2())**w) % pbr.get_p()
        ## the bank saves gw in __gws table.
        self.__gws[gw] = w
        print('Bank computed gw == {} and beta == {}'.format(gw, beta))
        return gw, beta

    def compute_c1(self, I, c, gw, pbr):
        ## 6. The Bank computes c1 = cx + w (mod q), sends c1 to the Spender,
        ## and immediately deducts the amount equal to 1 coin from the Spender’s
        ## account. Cf. Slides 24, 25.
        if self.__spender_accounts[I] > 0:
            self.__spender_accounts[I] -= 1
            w  = self.__gws[gw]
            c1 = (c*self.__x + w) % pbr.get_q()
            print('Bank computed c1 == {}'.format(c1))
            return c1
        else:
            ## no coin if the spender has 0 credit.
            print('Bank cannot compute c1, because spender account {} has 0 credits'.format(I))
            return None

    def deposit_coin_for_merchant(self, merchant_id, coin, coin_signature, pbr):
        """
        If the coin has been deposited before, the bank initiates double
        spending fraud control. Otherwise, the bank checks the validity
        of the coin with the 3 congruences on Slide 30.
        """
        if coin in self.__spent_coins:
            return self.double_spending_faud_control(merchant_id, coin, coin_signature, pbr)
        else:
            g = pbr.get_g()
            g1 = pbr.get_g1()
            g2 = pbr.get_g2()
            A, B, z, a, b, r = coin
            p = pbr.get_p()
            H = pbr.get_H()
            h = pbr.get_h()
            r1, r2, d = coin_signature
            cond1 = g**r % p == a*(h**H((A,B,z,a,b)))   % p
            cond2 = A**r % p == ((z**H((A,B,z,a,b)))*b) % p
            cond3 = (g1**r1)*(g2**r2) % p == ((A**d)*B) % p
            ### if all conditions hold, the coin is added
            ### to the set of spent coins and the merchant's
            ### account is credited with 1 unit.
            if cond1 and cond2 and cond3:
                self.__spent_coins[coin] = coin_signature
                self.__merchant_accounts[merchant_id] += 1
                print('Bank deposited coin {} with signature {} to merchant account {}'.format(coin,
                                                                                               coin_signature,
                                                                                               merchant_id))
                return merchant_id
            else:
                print('Bank failed to deposit coin {} with signature {} to merchant account {}'.format(coin,
                                                                                                       coin_signature,
                                                                                                       merchant_id))
                return -1

    def balance_for_merchant_account(self, merchant_account_id):
        return self.__merchant_accounts[merchant_account_id]

    def balance_for_spender_account(self, I):
        return self.__spender_accounts[I]

    def double_spending_faud_control(self, merchant_id, coin, coin_signature, pbr):
        """
        The bank figures out the true identity u of the double spender.
        """
        print('Bank initiated double spending fraud control')
        ### 1. Bank looks up the signature for the coin.
        ### your code here

        ### 2. Bank extracts r1_prime, r2_prime, d_prime from that signature.
        
        ### 3. Bank computes the congruence for the spender's id u on Slide 34
        ###    puts it in double_spender_id and returns it.
        ### your code here.
        
        print('double spender id = {}'.format(double_spender_id))
        return double_spender_id

        
        
            
            
            
            
        
        
            
        
        
        
    

