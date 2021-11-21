
import hmac
import hashlib
'''
HMAC using SHA1: 
Create a hash object with private key and message to be hashed
	Hash_function = hmac.new(b'key', b'message to hash', hashlib.sha1)
	
To get the has value call:
	Hash_function.hexdigest()

'''
Hash_function = hmac.new(b'1234', b'Deposit $100', hashlib.sha1)

print ("Hash: " + Hash_function.hexdigest())



Hash_function = hmac.new(b'1234', b'Withdraw $250', hashlib.sha1)

print ("Hash: " + Hash_function.hexdigest())


Hash_function = hmac.new(b'1234', b'Deposit $100', hashlib.sha1)

print ("Hash: " + Hash_function.hexdigest())


