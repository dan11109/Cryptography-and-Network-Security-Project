from bitarray import bitarray
from bitarray import util as bautil
import random
def inversePermutationArr(p):
    # takes in some permutation array eg P10 and returns the permutation array that would undo P10
    pInverse = [0]*len(p)
    for i in range(len(p)):
        val = p[i]
        pos = i+1
        tmp = val
        val = pos
        pos = tmp
        pInverse[pos-1] = val
    return pInverse

INITIAL_PERMUTATION = [
58, 50, 42, 34, 26, 18, 10, 2,
60, 52, 44, 36, 28, 20, 12, 4,
62, 54, 46, 38, 30, 22, 14, 6,
64, 56, 48, 40, 32, 24, 16, 8,
57, 49, 41, 33, 25, 17, 9, 1,
59, 51, 43, 35, 27, 19, 11, 3,
61, 53, 45, 37, 29, 21, 13, 5,
63, 55, 47, 39, 31, 23, 15, 7
]
FINAL_PERMUTATION = inversePermutationArr(INITIAL_PERMUTATION)
    # S1
EXPANSION_PERMUTATION = [
32, 1, 2, 3, 4, 5, 4, 5, 6, 7,
8, 9, 8, 9, 10, 11, 12, 13,
12, 13, 14, 15, 16, 17, 16, 17,
18, 19, 20, 21, 20, 21, 22, 23,
24, 25, 24, 25, 26, 27, 28, 29,
28, 29, 31, 31, 32, 1
]
STRAIGHT_PERMUTATION = [
16, 7, 20, 21, 29, 12, 28, 17, 1, 15, 23, 26, 5, 18, 31, 10, 2, 8, 24, 14, 32, 27, 3, 9, 19, 13, 30, 6, 22, 11, 4, 25
]
PARITY_BIT_PERMUTATION = [
57, 49, 41, 33, 25, 17, 9, 1,
58, 50, 42, 34, 26, 18, 10, 2,
59, 51, 43, 35, 27, 19, 11, 3,
60, 52, 44, 36, 63, 55, 47, 39,
31, 23, 15, 7, 62, 54, 46, 38,
30, 22, 14, 6, 61, 53, 45, 37,
29, 21, 13, 5, 28, 20, 12, 4
        ]
COMPRESSION_D_BOX = [
14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10, 23, 19, 12, 4, 26, 8, 16, 7, 27, 20, 13, 2, 41, 52, 31, 37, 47, 55, 30, 40, 51, 45, 33, 48, 44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32
        ]
S1 = [
        [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
 [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
 [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
 [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]]

# S2
S2 = [
       [ 15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
 [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
 [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
 [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]]

# S3
S3 = [
       [ 10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
 [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
 [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
 [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]]

# S4
S4 = [
        [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
 [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
 [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
 [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]]

# S5
S5 = [
        [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
 [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
 [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
 [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]]

# S6
S6 = [
        [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
 [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
 [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
 [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]]

# S7
S7 = [
       [ 4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
 [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
 [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
 [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]]

# S8
S8 = [
        [ 13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
 [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
 [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
 [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]


def permute(toPermute, permutationTable):
    return bitarray([toPermute[x-1] for x in permutationTable])

def circularLeftShift(inputBits, n):
    save = inputBits[0:n]
    return (inputBits << n) + save

def parityDrop(key):
    """
    key: length 64 bitarray representing key wiht parity bits
    drops bits 8, 16, 24, 32, 40, 48, 56, 64 from the 64 bit key 
    permutes the rest of the bits
    """
    res = permute(key, PARITY_BIT_PERMUTATION)
    assert(len(res) == 56)
    return res 

def keyGen(key):
    """
    key: length 64 bitarray representing key with parity bits
    returns: list of 16 length 48 bitarrays (round keys)
    """
    singleLeftShift = [0, 1, 8, 15]
    key56 = parityDrop(key)
    keys = []
    L = key56[0:27]
    R = key56[27:]
    shift = 2
    for i in range(16):
        if i in singleLeftShift:
            shift = 1
        else:
            shift = 2
        # circular left shift
        L = circularLeftShift(L, shift)
        R = circularLeftShift(R, shift)
        keys.append(permute(L+R, COMPRESSION_D_BOX))
        # combine, compress, add key to list
    # sanity check
    for k in keys:
        assert(len(k) == 48)
    assert(len(keys) == 16)
    return keys

def applySBox(inputBits, SBox):
    """
    inputBits: length 6 bitarray
    SBox: 4x16 2d python array containing integer values 0-15, each representing a potential 4 bit output
    returns: length 4 bitarray
    """
    assert(len(inputBits) == 6)
    # not sure if this works
    rowIndexBits = bitarray(str(inputBits[0]) + str(inputBits[5]))
    colIndexBits = inputBits[1:5]
    assert(len(rowIndexBits) == 2)
    assert(len(colIndexBits) == 4)
    rowIndex = bautil.ba2int(rowIndexBits)
    colIndex = bautil.ba2int(colIndexBits)
    assert(rowIndex >= 0 and rowIndex < 4)
    assert(colIndex >= 0 and rowIndex < 16)
    output = SBox[rowIndex][colIndex]
    outputBits = bautil.int2ba(output, length=4)
    return outputBits
def applySBoxes(inputBits):
    """
    inputBits: length 48 bitarray (Rprev expanded)
    uses global constants S1-8: 4x16 2d python array containing integer values 0-15, each representing a potential 4 bit output
    returns: length 32 bitarray 

    """
    assert(len(inputBits) == 48)
    in1 = inputBits[0:6]
    in2 = inputBits[6:12]
    in3 = inputBits[12:18]
    in4 = inputBits[18:24]
    in5 = inputBits[24:30]
    in6 = inputBits[30:36]
    in7 = inputBits[36:42]
    in8 = inputBits[42:48]
    out1 = applySBox(in1, S1)
    out2 = applySBox(in2, S2)
    out3 = applySBox(in3, S3)
    out4 = applySBox(in4, S4)
    out5 = applySBox(in5, S5)
    out6 = applySBox(in6, S6)
    out7 = applySBox(in7, S7)
    out8 = applySBox(in8, S8)
    output = out1 + out2 + out3 + out4 + out5 + out6 + out7 + out8
    assert(len(output)==32)
    return output
def f(Rprev, roundKey):
    """
    Rprev: length 32 bitarray 
    roundKey: length 48 bitarray 
    returns: length 64 bitarray 

    expands Rprev to 48 bits
    1.
    xors with the round key
    2.
    applies s boxes
    3.
    permutes
    """
    assert(len(Rprev) == 32)
    assert(len(roundKey)==48)
    return permute(applySBoxes(permute(Rprev, EXPANSION_PERMUTATION) ^ roundKey), STRAIGHT_PERMUTATION)

def mixer(inputBits, roundKey):
    """
    inputBits: length 64 bitarray 
    roundKey: length 48 bitarray 
    returns: length 64 bitarray 

    takes 64 input bits and "mixes" in the round key
    """
    Lprev = inputBits[0:32]
    Rprev = inputBits[32:]
    assert(len(Lprev) == 32)
    assert(len(Rprev) == 32)
    return (Lprev ^ f(Rprev, roundKey)) + Rprev
def swapper(inputBits):
    """
    inputBits: length 64 bitarray 
    swaps the right and left halves of inputBits
    """
    Lprev = inputBits[0:32]
    Rprev = inputBits[32:]
    return Rprev + Lprev

def round(inputBits, roundKey, i):
    """
    inputBits: length 64 bitarray 
    roundKey: length 48 bitarray 
    performs one round of our feistel cipher
    """
    # don't perform the swap on the last round
    if i == 15:
        return mixer(inputBits, roundKey)
    else:
        return swapper(mixer(inputBits, roundKey))
def DES(key, toEncrypt, encrypt):
    """
    key: length 64 bitarray (key)
    toEncrypt: length 64 bitarray (plaintext)
    returns: length 64 bitarray (ciphertext)
    """
    roundKeys = keyGen(key)
    if not encrypt:
        roundKeys.reverse()

    # initial permutation
    temp = permute(toEncrypt, INITIAL_PERMUTATION)
    # perform 16 rounds
    for i in range(16):
        temp = round(temp, roundKeys[i], i)
    # final permutation
    temp = permute(temp, FINAL_PERMUTATION)
    assert(len(temp) == 64)
    return temp
    

if __name__ == '__main__':
    # example usage
    key = bitarray("0"*64)
    toEncrypt = bitarray("0"*64)
    ciphertext = DES(key, toEncrypt, encrypt = True)
    print("Encrypting")
    print("Got:")
    print(ciphertext)
    print("Decrypting")
    plaintext = DES(key, ciphertext, encrypt = False)
    print("Got:")
    print(plaintext)
