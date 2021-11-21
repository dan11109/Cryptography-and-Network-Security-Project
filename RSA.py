


# Generates p,q,e,and d for RSA given length of primes
# Code for generating large primes from: https://www.geeksforgeeks.org/how-to-generate-large-prime-numbers-for-rsa-algorithm/
'''
RSA parameter generation
	call RSA_params(n) with n being the length of p and q generated and it will return (p,q,e,d). You can then calculate N = pq. 
'''


import random
 
# Pre generated primes
first_primes_list = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
                     31, 37, 41, 43, 47, 53, 59, 61, 67,
                     71, 73, 79, 83, 89, 97, 101, 103,
                     107, 109, 113, 127, 131, 137, 139,
                     149, 151, 157, 163, 167, 173, 179,
                     181, 191, 193, 197, 199, 211, 223,
                     227, 229, 233, 239, 241, 251, 257,
                     263, 269, 271, 277, 281, 283, 293,
                     307, 311, 313, 317, 331, 337, 347, 349]
 
def nBitRandom(n):
    return random.randrange(2**(n-1)+1, 2**n - 1)
 
def getLowLevelPrime(n):
    '''Generate a prime candidate divisible
    by first primes'''
    while True:
        # Obtain a random number
        pc = nBitRandom(n)
 
         # Test divisibility by pre-generated
         # primes
        for divisor in first_primes_list:
            if pc % divisor == 0 and divisor**2 <= pc:
                break
        else: return pc
 
def isMillerRabinPassed(mrc):
    '''Run 20 iterations of Rabin Miller Primality test'''
    maxDivisionsByTwo = 0
    ec = mrc-1
    while ec % 2 == 0:
        ec >>= 1
        maxDivisionsByTwo += 1
    assert(2**maxDivisionsByTwo * ec == mrc-1)
 
    def trialComposite(round_tester):
        if pow(round_tester, ec, mrc) == 1:
            return False
        for i in range(maxDivisionsByTwo):
            if pow(round_tester, 2**i * ec, mrc) == mrc-1:
                return False
        return True
 
    # Set number of trials here
    numberOfRabinTrials = 20
    for i in range(numberOfRabinTrials):
        round_tester = random.randrange(2, mrc)
        if trialComposite(round_tester):
            return False
    return True

def egcd(a, b):
    #helper funtion  for modinv
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    #finds the modular inverse 
    g, x, y = egcd(a, m)
    if g != 1:
        print(g)
        raise Exception('modular inverse does not exist')
    else:
        return x % m

def GCD(x, y):
    #computes GCD
    if x > y:
        small = y
    else:
        small = x
    for i in range(1, small+1):
        if((x % i == 0) and (y % i == 0)):
            gcd = i       
    return gcd


def RSA_params(n):

	p = getLowLevelPrime(n)
	while(not isMillerRabinPassed(p)):
		p = getLowLevelPrime(n)

	q = getLowLevelPrime(n)
	while(not isMillerRabinPassed(p) or p == q):
		q = getLowLevelPrime(n)
	
	n = p*q
	phi_n = (p-1) * (q-1)

	e = 0   #gcd(e,phi_n) == 1
	while(True):
		e = random.randrange(2,phi_n)
		if(GCD(e,phi_n) == 1):
			break

	d = modinv(e, phi_n)

	return(p,q,e,d)


 
if __name__ == '__main__':
    
    #print(RSA_params(8))




