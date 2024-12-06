#!/usr/bin/python
# -*- coding: utf-8 -*-

#############################################################
# module: vendor.py
# descrip: the vendor of the digital cash system.
#          same as merchant.py except the id is different.
#          it's set to self__V = 31.
# bugs to vladimir kulyukin via canvas
##############################################################

from pubrepo import pubrepo
from bank import bank

class vendor(object):

    def __init__(self):
        """
        the merchant chooses its identity.
        """
        self.__V = 31

    def get_id(self):
        return self.__V

    def create_bank_account(self, bnk):
        """
        The merchant requests the bank to create 
        a merchant account.
        """
        print('Merchant {} requested Bank to create a merchant account.'.format(self.__V))
        bnk.create_merchant_account(self.__V)

    ## coin is (A,B,z,a,b,r)        
    def __is_coin_valid(self, coin, pbr):
        """
        The merchant checks the validity of the coin. Cf. Slide 27.
        pbr is public repo.
        """
        A,B,z,a,b,r = coin
        p = pbr.get_p()
        g = pbr.get_g()
        h = pbr.get_h()
        H = pbr.get_H()
        cond1 = (g**r % p) == (a*(h**H((A,B,z,a,b)))) % p
        cond2 = (A**r % p) == ((z**H((A,B,z,a,b)))*b) % p
        return (cond1 and cond2)

    def compute_d(self, coin, pbr):
        """
        the merchant checks the validity of the coin and
        if the coin is valid computes d (Cf. Slide 27).
        """
        if self.__is_coin_valid(coin, pbr):
            H0 = pbr.get_H0()
            t  = pbr.get_time()
            A, B = coin[0], coin[1]
            d  = H0((A,B,self.__V,t))
            print('Merchant {} computed d == {}.'.format(self.__V, d))
            return d
        else:
            print('Merchant {} failed to computed d, because coin {} is not valid.'.format(self.__V, coin))
            return None

    def accept_coin(self, coin, r1, r2, d, pbr):
        """
        the merchant accepts the coin (cf. Slide 28).
        """
        A, B = coin[0], coin[1]
        g1 = pbr.get_g1()
        g2 = pbr.get_g2()
        p  = pbr.get_p()
        ## The Merchant checks if the assertion below holds
        #  and only then accepts the coin.
        coin_acceptable =  (g1**r1)*(g2**r2) % p == (A**d)*B % p
        assert coin_acceptable
        self.__accepted_coin = coin
        self.__accepted_coin_signature = r1, r2, d
        print('Merchant {} found coin {} with signature {} acceptable.'.format(self.__V,
                                                                               coin,
                                                                               (r1, r2, d)))

    def deposit_coin(self, bnk, pbr):
        """ 
        The merchant asks the bank to deposit the coin. Cf. Slide 30.
        """
        id = self.__V
        coin, coin_sign = self.__accepted_coin, self.__accepted_coin_signature
        print('Merchant {} requested Bank to deposit coin {} with signature {}'.format(self.__V, coin, coin_sign))
        return bnk.deposit_coin_for_merchant(self.__V,
                                             self.__accepted_coin,
                                             self.__accepted_coin_signature,
                                             pbr)

    def get_balance(self, bnk):
        return bnk.balance_for_merchant_account(self.__V)
        
        


