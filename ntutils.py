########################################
# ntutils.py
# number theory utils 
########################################

import math

def xgcd(a,b):
    ''' 
    extended gcd that returns d, x, y such that
    d = ax + by.
    '''
    prevx, x = 1, 0
    prevy, y = 0, 1
    aa, bb = a, b
    while bb != 0:
        q = aa // bb
        x, prevx = prevx - q*x, x
        y, prevy = prevy - q*y, y
        aa, bb = bb, aa % bb
    return aa, prevx, prevy

def mult_inv(a, n):
    """
    multiplicative inverse of a in Z^{*}_{n}.
    """
    d, x, y = xgcd(a, n)
    if x < 0:
        xx = x + n
        while xx < 0:
            xx += n
            break
        return xx
    else:
        return x

def is_primitive_root_of_p(r, p):
    """
    Is r and primitive root of prime p?
    """
    assert is_prime(p)
    equiv_classes = set(r**i % p for i in range(1, p))
    for i in range(1, p):
        if not i in equiv_classes:
            return False
    return True

def find_primitive_roots_of_p(p):
    """
    Find all primitive roots of prime p.
    """
    return set(r for r in range(1, p) if is_primitive_root_of_p(r, p))

def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    if n > 2:
        for d in range(3, int(math.floor(math.sqrt(n)))+1, 2):
            if n % d == 0:
                return False
        return True

def ith_prime(i):
    assert i > 0
    pcount = 0
    pi = 0
    n = 1
    while pcount < i:
        if is_prime(n):
            pcount += 1
            pi = n
        n += 1
    return pi

def prime_factors_aux(n, i):
    if is_prime(n):
        return [n]
    else:
        pi = ith_prime(i)
        if n % pi == 0:
            return [pi] + prime_factors_aux(n//pi, i)
        else:
            return prime_factors_aux(n, i+1)

def prime_factors(n):
    assert n > 1
    return prime_factors_aux(n, 1)
        
def gen_perms(nums, n):
    if n == 0:
        return [[]]
    else:
        perms = gen_perms(nums, n-1)
        new_perms = []
        for p in perms:
            for n in nums:
                new_perms.append([n] + p)
        perms == None
        return new_perms
    
### the range is inclusive [a, b]
def find_primes_in_range(a, b):
    return [i for i in range(a, b+1) if is_prime(i)]

def find_n_digit_primes_in_range(a, b, n):
    return [i for i in find_primes_in_range2(a, b) if len(str(i)) == n]

def euler_phi(n):
    assert n >= 2
    rslt = 1
    for p in range(n+1):
        if is_prime2(p) and n % p == 0:
            rslt *= (p - 1)/p
    eu_phi = n * rslt
    f = math.floor(eu_phi)
    c = math.ceil(eu_phi)
    fdiff = abs(eu_phi - f)
    cdiff = abs(eu_phi - c)
    if fdiff < cdiff:
        return f
    else:
        return c

def euler_totient(n):
    return eulers_phi(n)

    
if __name__ == '__main__':
    pass
    
