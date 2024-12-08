#!/usr/bin/python
# -*- coding: utf-8 -*-

#############################################################
# module: digcash_uts.py
# descrip: unit tests for the digital cash system.
# bugs to vladimir kulyukin via canvas
##############################################################

import unittest
import random
from pubrepo import pubrepo
from auth import auth
from bank import bank
from spender import spender
from merchant import merchant
from vendor import vendor

class rsa_uts(unittest.TestCase):

    def test_digcash_system(self):
        """
        Test initialization of Authority, Bank, Spender, Merchant,
        the creation of the coin by the Bank, the spending of 
        the coin by the merchant,
        the double spending of the coin, the detection of the 
        double spending fraud by the bank.
        Cf. Slides 18 -- 35.
        """
        ## 1. Initialize public repo, authority
        pbr = pubrepo()
        aut = auth()
        aut.init_p_q_g_g1_g2_H_H0(pbr)

        ## 2. Bank initialization
        bnk = bank()
        bnk.create_h_h1_h2(pbr)

        ## 3. Spender initialization
        spr = spender()
        spr.create_bank_account(bnk, pbr)

        ## 4. Merchankt initialization
        mrt = merchant()
        mrt.create_bank_account(bnk)

        ## 5. merchant requests a coin from the bank.
        spr.request_coin(bnk, pbr)

        ## 6. spender spends a newly issued coin.
        spr.spend_unspent_coin(mrt, pbr)

        ## 7. merchant deposits the coin.
        mrt.deposit_coin(bnk, pbr)

        ## 8. spender's balance is now 10 - 1.
        assert spr.get_balance(bnk) == 9
        ## 9. the merchant's balance is now 0 + 1.
        assert mrt.get_balance(bnk) == 1

        ## 10. vendor is initialized
        vdr = vendor()
        vdr.create_bank_account(bnk)

        ### spender attempts to double spend a coin at the vendor vndr.
        spr.double_spend_coin(vdr, pbr)
        ### vendor deposits it at the bank.
        double_spender_id = vdr.deposit_coin(bnk, pbr)

        assert double_spender_id == spr.reveal_secret_id()

        ### spender's balance is still 9 because the bank
        ### did not withdraw a unit from the spender's account.
        assert spr.get_balance(bnk) == 9
        ### the vendor's balance is still 0, because
        ### the double spent coint was not deposited.
        assert vdr.get_balance(bnk) == 0
    
    def runTest(self):
        pass


if __name__ == '__main__':
    unittest.main()
