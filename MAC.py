
'''
HMAC using SHA1 call MAC.hmac_fn(message, key) -> MAC value

'''

import sha1
def to_bin(s):
	num = ''
	for i in range(len(s)):
		c = s[i]
		n = ord(c)
		b = bin(n)
		num = num + b[2:]
	return num
	    


def hmac_fn(msg, key):
	
    #random generated pads 64
    opad = '1111010101000011010100011100111100100010011011001111100100010010'
    ipad = '0000101011011101000010001111101111001100101111111000010100111011'
    
    msg = to_bin(msg)

    tmp1 = bin(key ^ int(opad,2))[2:]
    tmp2 = bin(key ^ int(ipad,2))[2:]
  

    hmac = sha1.sha1(tmp1 + sha1.sha1( tmp2 + msg ) )
    return hmac

def vrfy(msg, mac, key):
    return hmac_fn(msg, key) == mac

if __name__ == "__main__":
    print(len(hmac_fn('10001010101010', 123)))

    print(hmac_fn('hello world', 123))

