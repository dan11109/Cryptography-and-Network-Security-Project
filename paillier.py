
'''
Implementation of pailler pkc

returns (g,p,q,lambd,u)

c = g^m * r^n mod n^2

m = L(c^λ mod n^2) * μ mod n

'''


from Crypto.Util import number #NOTE: only used to generate large prime numbers 
import random
 
def computeGCD(x, y):
  
   while(y):
       x, y = y, x % y
  
   return x

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

def compute_lcm(x, y):

   # choose the greater number
   if x > y:
       greater = x
   else:
       greater = y

   while(True):
       if((greater % x == 0) and (greater % y == 0)):
           lcm = greater
           break
       greater += 1

   return lcm


def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        return -1
        print(g)
        raise Exception('modular inverse does not exist')
    else:
        return x % m

def L(x,n):
	tmp = (x-1) % n**2
	den = n #modInverse(n, n**2)

	return (tmp // den) % (n**2)

def pailler(n):

	while(True):
	    p =  number.getPrime(n)
	    q = number.getPrime(n)
	    while(p == q):
	        q = number.getPrime(n)

	    N = p*q

	    phi_n = (p-1) * (q-1)
	   
	    lambd = compute_lcm(p-1,q-1)
	
	    g = random.randrange(1,N**2)

	    tmp = L(pow(g,lambd,N**2),N)
	    
	    u = modinv( L(pow(g,lambd,N**2),N)%N ,N)

	    if(u != -1):
	  	    break

	return (g,p,q,lambd,u)
	

if __name__ == '__main__':
	
	(g,p,q,lambd,u) = pailler(8)

	N = p*q

	r = random.randrange(1,N)
	m = 1234 

	c = pow(g,m,N**2) * pow(r,N,N**2) % N**2
	print(c)

	m = L(pow(c,lambd,N**2),N ) * u % N
	print(m)




