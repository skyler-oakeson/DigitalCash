#!/usr/bin/python
# -*- coding: utf-8 -*-

#############################################################
# module: pubrepo.py
# descrip: public repository initialized by the Authority
# and the Bank and used by all participants.
# bugs to vladimir kulyukin via canvas
##############################################################

class pubrepo(object):
    
    def __init__(self):
        ### p, q, g, g1, H, H0 are
        ### published by the Authority.
        self.p = None
        self.q = None
        self.g = None
        self.g1 = None
        self.g2 = None
        self.H = None
        self.H0 = None
        ## we start the time count at 1
        self.__time = 1
        
        ### h, h1, h2 are the parameters
        ### published by the Bank
        self.h  = None
        self.h1 = None
        self.h2 = None

    def set_p(self, p):
        self.p = p

    def get_p(self):
        return self.p

    def set_q(self, q):
        self.q = q

    def get_q(self):
        return self.q

    def set_g(self, g):
        self.g = g

    def get_g(self):
        return self.g

    def set_g1(self, g1):
        self.g1 = g1

    def get_g1(self):
        return self.g1

    def set_g2(self, g2):
        self.g2 = g2

    def get_g2(self):
        return self.g2

    def set_H(self, H):
        self.H = H

    def get_H(self):
        return self.H

    def set_H0(self, H0):
        self.H0 = H0

    def get_H0(self):
        return self.H0

    def set_h(self, h):
        self.h = h

    def get_h(self):
        return self.h

    def set_h1(self, h1):
        self.h1 = h1

    def get_h1(self):
        return self.h1

    def set_h2(self, h2):
        self.h2 = h2

    def get_h2(self):
        return self.h2

    def get_time(self):
        t = self.__time
        self.__time += 1
        return t
    




    

    

    



        
        



