from DES import DES
from bitarray import bitarray
import random
import pickle
from Crypto.Util.Padding import pad, unpad

def genRandomKey(n, seed=None):
    if seed is not None:
        random.seed(seed)
    bits = ['0','1']
    return  "".join([ random.choice(bits) for _ in range(n) ] )

def tripleDES(key, toEncrypt, encrypt):
    """
    key: a length 192 bitarray representing K1K2K3 for triple des
    toEncrypt: length 64 bitarray representing the message to be encrypted
    """
    k1 = key[0:64]
    k2 = key[64:128]
    k3 = key[128:192]
    assert(len(k1) == len(k2))
    assert(len(k1) == len(k3))
    assert(len(k1) == 64)
    if encrypt:
        cipherText = DES(k3, DES(k2, DES(k1, toEncrypt, True), False), True)
        return cipherText
    else: # decrypt
        plainText = DES(k1, DES(k2, DES(k3, toEncrypt, False), True), False)
        return plainText
def _tripleDESCBCEncrypt(message, key):
    """
    message: len N%64==0 bitarray (padded encoded plainText)
    key: length 192 bitarray
    returns: length N >= 8*len(message) bitarray
    encrypts message w key using tDES in CBC mode
    """
    assert(len(message)%64==0)
    assert(len(key) == 192)
    # use an initialization vector of all zeros cus uhh
    IV = bitarray("0"*64)
    # divide the message bitarray into 64 bit chunks
    unencryptedChunks = []
    left = 0
    right = 64
    while right < len(message)+1:
        unencryptedChunks.append(message[left:right])
        left = left + 64
        right = right + 64
    # sanity check
    assert(len(unencryptedChunks) == len(message)/64)
    for chunk in unencryptedChunks:
        assert(len(chunk) == 64)

    # encrypt
    encryptedChunks = []
    XORVec = IV
    for i in range(len(unencryptedChunks)):
        chunk = unencryptedChunks[i]
        encryptedChunks.append(tripleDES(key, XORVec ^ chunk, True))
        XORVec = encryptedChunks[i]
    ret = bitarray()
    for chunk in encryptedChunks:
        ret = ret + chunk
    return ret 

def _tripleDESCBCDecrypt(cipherText, key):
    """
    cipherText: len N%64==0 bitarray (padded encoded plainText)
    key: length 192 bitarray
    returns: length N >= 8*len(message) bitarray
    decrypts message w key using tDES in CBC mode
    """
    assert(len(key) == 192)
    assert(len(cipherText) % 64 == 0)
    # use an initialization vector of all zeros cus uhh
    IV = bitarray("0"*64)
    # divide the cipherText bitarray into 64 bit chunks
    encryptedChunks = []
    left = 0
    right = 64
    while right < len(cipherText)+1:
        encryptedChunks.append(cipherText[left:right])
        left = left + 64
        right = right + 64

    # sanity check
    assert(len(encryptedChunks) == len(cipherText)/64)
    for chunk in encryptedChunks:
        assert(len(chunk) == 64)

    # decrypt
    unencryptedChunks = []
    XORVec = IV
    for i in range(len(encryptedChunks)):
        chunk = encryptedChunks[i]
        unencryptedChunks.append(XORVec ^ tripleDES(key, chunk, False))
        XORVec = encryptedChunks[i]

    ret = bitarray()
    for chunk in unencryptedChunks:
        ret = ret + chunk
    return ret

def tripleDESCBCEncrypt(message, key):
    """
    message: arbitrary length string to encrypt
    key: length 192 string of 1s and 0s 
    returns: length N >= 8*len(message) string of 1s and zeros
    (we pad the message to the nearest 64 bits using whitespace- the cipherText might be a bit longer)
    """
    key = bitarray(key)
    assert(len(key) == 192)
    # pad string to the nearest 64 bits by adding whitespace bytes
    while (len(message)*8) % 64 != 0:
        message = message + " "

    # sanitize?
    assert(len(message)%8==0)
    assert(len(message)> 0)
    # convert string to bitarray
    messageBits = bitarray()
    messageBits.frombytes(message.encode("utf-8"))
    assert(len(messageBits)%64 == 0)
    res = _tripleDESCBCEncrypt(messageBits, key)
    return res.to01()

def tripleDESCBCDecrypt(cipherText, key):
    """
    cipherText: string of 1s and 0s w. len%8==0
    key: length 192 string of 1s and 0s 
    returns: length k < N string representing the plainText
    (whitespace stripped from the resulting plainText)
    """
    cipherText = bitarray(cipherText)
    key = bitarray(key)
    # convert bitarray to bytes and decode to utf-8
    ret = _tripleDESCBCDecrypt(cipherText, key).tobytes().decode("utf-8")
    # strip our whitespace padding
    return ret.rstrip()

def tripleDESCBCEncryptAny(anyObject, key):
    key = bitarray(key)
    pickled = pickle.dumps(anyObject)
    pickledPadded = pad(pickled, 8)
    messageBits = bitarray()
    messageBits.frombytes(pickledPadded)
    res = _tripleDESCBCEncrypt(messageBits, key)
    return res.to01()

def tripleDESCBCDecryptAny(bitarrayString, key):
    key = bitarray(key)
    cipherText = bitarray(bitarrayString)
    plaintext = _tripleDESCBCDecrypt(cipherText, key)
    # convert to bytes from bitarray
    plaintextBytes = plaintext.tobytes()
    # unpad
    pickled = unpad(plaintextBytes, 8)
    # unpickle
    return pickle.loads(pickled)


def singleTripleDESExample():
    # example usage of single tripleDES
    print("Single triple DES:")
    key = bitarray("0"*192)
    toEncrypt = bitarray("0"*64)
    cipherText = tripleDES(key, toEncrypt, encrypt = True)
    print("Encrypting")
    print(toEncrypt)
    print("Got:")
    print(cipherText)
    print("Decrypting")
    plainText = tripleDES(key, cipherText, encrypt = False)
    print("Got:")
    print(plainText)
def tripleDESCBCTest():
    # example usage of CBC tripleDES (use this)
    print("CBC triple DES:")
    # generate a random key
    key = "".join(random.choices(["0", "1"], k=192))
    toEncrypt = "plaintext of arbitrary length1234"
    print("Encrypting:\n{}\nusing a random key:\n{}".format(toEncrypt, key))
    cipherText = tripleDESCBCEncrypt(toEncrypt, key)
    print("Found ciphertext:")
    print(cipherText)
    print("Decrypting")
    plainText = tripleDESCBCDecrypt(cipherText, key)
    print("Found plaintext:")
    print(plainText)

def tripleDESCBCAnyTest():
    # example usage of CBC tripleDES (use this)
    print("CBC triple DES:")
    # generate a random key
    key = "".join(random.choices(["0", "1"], k=192))
    toEncrypt = (1, 2, 3)
    print("Encrypting:\n{}\nusing a random key:\n{}".format(toEncrypt, key))
    cipherText = tripleDESCBCEncryptAny(toEncrypt, key)
    print("Found ciphertext:")
    print(cipherText)
    print("Decrypting")
    plainText = tripleDESCBCDecryptAny(cipherText, key)
    print("Found plaintext:")
    print(plainText)

if __name__ == '__main__':
    # single triple DES example
    # singleTripleDESExample()
    tripleDESCBCAnyTest()

