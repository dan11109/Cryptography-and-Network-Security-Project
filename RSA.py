


# Generates p,q,e,and d for RSA given length of primes

'''
RSA parameter generation
	call RSA_params(n) with n being the length of p and q generated and it will return (p,q,e,d). You can then calculate N = pq. 
'''

from Crypto.Util import number #NOTE: only used to generate large prime numbers 
import random
 


def modInverse(a, m): #more efficient version 
    m0 = m
    y = 0
    x = 1
 
    if (m == 1):
        return 0
 
    while (a > 1):
 
        # q is quotient
        q = a // m
        t = m
 
        # m is remainder now, process
        # same as Euclid's algo
        m = a % m
        a = t
        t = y
 
        # Update x and y
        y = x - q * y
        x = t
 
    # Make x positive
    if (x < 0):
        x = x + m0
 
    return x


def RSA_params(n):

    p = number.getPrime(n)
    q = number.getPrime(n)
    while(p == q):
        q = number.getPrime(n)

    N = p*q

    phi_n = (p-1) * (q-1)

    e = number.getPrime(n)
    d = modInverse(e, phi_n)

    return(p,q,e,d)



 
if __name__ == '__main__':
    
    (p,q,e,d) = RSA_params(512)
    
    N = p*q

    c = pow(1234,e,N)

    print(c)
    print()
    
    d = pow(c,d,N)

    print(d)


    

