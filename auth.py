#!/usr/bin/python
# -*- coding: utf-8 -*-

#######################################
# module: auth.py
# description: regulatory authority of the digital
# cash system outlined in CS5000: F24: Lecture 25.
# and based on references [1] and [2]
# bugs to vladimir kulyukin in canvas.
#######################################

from ntutils import is_prime
from ntutils import is_primitive_root_of_p
import random
from pubrepo import pubrepo

class auth(object):

    def __find_pq(self):
        """
        return p and q such that p is a prime, q is a prime and q = (p-1)/2.
        """
        return 227, 113

    def __choose_primitive_root_of_p(self, p):
        """
        13 is a primitive root of 227.
        """
        return 13

    def init_p_q_g_g1_g2_H_H0(self, pbr):
        """
        Creation of p, p, g, g1, H, and H0 by Authority.
        Cf. Slides 13 - 16 of Lecture 25.
        """
        ### 1. Auth chooses primes p, q.
        p, q = self.__find_pq()
        assert is_prime(p) and is_prime(q) and q == (p-1)/2        

        ### 2. Auth chooses a primitive root r of p
        r = self.__choose_primitive_root_of_p(p)
        assert is_primitive_root_of_p(r, p)
        ### and computes g = r^2
        g = r**2
        ### 3. Auth chooses 2 random exponents k1 and k2.
        ###    The larger the better of course, but
        ###    we'll keep fixed and small to make sure
        ###    that our unit tests pass w/o any buffer overflows.
        k1, k2 = 3, 5

        g1 = (g**k1) % p
        g2 = (g**k2) % p

        ### 4. Auth creates 2 hash functions.
        H = self.__create_H(q)
        H0 = self.__create_H0(q)

        ## 5. Autho publishes p, p, g, g1, g2, H, H0
        pbr.set_p(p)
        pbr.set_q(q)
        pbr.set_g(g)
        pbr.set_g1(g1)
        pbr.set_g2(g2)
        pbr.set_H(H)
        pbr.set_H0(H0)

        self.__display_init_results(pbr)

    def __create_H(self, q):
        """ 
        Create a crypto hash function that maps 5 tuples to an integer mod q.
        """
        import hashlib
        def H(int_5_tup):
            assert len(int_5_tup) == 5
            for i in range(5):
                assert isinstance(int_5_tup[i], int)
            return int(hashlib.sha3_512(bytes(int_5_tup)).hexdigest(), 16) % q
        return H

    def __create_H0(self, q):
        """
        Create a crypto hash function that maps 4 tuples to an integer mod q.
        """
        import hashlib
        def H0(int_4_tup):
            assert len(int_4_tup) == 4
            for i in range(4):
                assert isinstance(int_4_tup[i], int)
            return int(hashlib.sha3_384(bytes(int_4_tup)).hexdigest(), 16) % q
        return H0

    def __display_init_results(self, pbr):
        print('*** Authority initialization done...')
        print('p  == {}'.format(pbr.get_p()))
        print('q  == {}'.format(pbr.get_q()))
        print('g  == {}'.format(pbr.get_g()))
        print('g1 == {}'.format(pbr.get_g1()))
        print('g2 == {}'.format(pbr.get_g2()))
 

