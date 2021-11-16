from DES import DES
from bitarray import bitarray

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
        ciphertext = DES(k3, DES(k2, DES(k1, toEncrypt, True), False), True)
        return ciphertext
    if not encrypt:
        plaintext = DES(k1, DES(k2, DES(k3, toEncrypt, False), True), False)
        return plaintext


if __name__ == '__main__':
    # example usage
    key = bitarray("0"*192)
    toEncrypt = bitarray("0"*64)
    ciphertext = tripleDES(key, toEncrypt, encrypt = True)
    print("Encrypting")
    print(toEncrypt)
    print("Got:")
    print(ciphertext)
    print("Decrypting")
    plaintext = tripleDES(key, ciphertext, encrypt = False)
    print("Got:")
    print(plaintext)
