import json
import sha1
def readDB(jsonFileName):
    fileObj = open(jsonFileName, "r")
    db = json.loads(fileObj.read())
    fileObj.close()
    return db 

def writeDB(data, jsonFileName):
    fileObj = open(jsonFileName, "w")
    json.dump(data, fileObj)
    fileObj.close()
    
def withdraw(filename, username, amount):
    db = readDB(filename)
    currbal = db["accounts"][username]["balance"]
    if currbal - amount < 0:
        return (False, currbal)
    db["accounts"][username]["balance"] -= amount
    print(db)
    writeDB(db, filename)
    print("WITHDREW")
    return (True, db["accounts"][username]["balance"])

def deposit(filename, username, amount):
    db = readDB(filename)
    db["accounts"][username]["balance"] += amount
    writeDB(db, filename)
    print("DEPOSITED")
    return (True, db["accounts"][username]["balance"])

def checkBalance(filename, username):
    db = readDB(filename)
    return (True, db["accounts"][username]["balance"])

def verifyPassword(bankfile, username, password):
    db = readDB(bankfile)
    return sha1.sha1(password) == db["accounts"][username]["password"]

if __name__ == '__main__':
    username = "alpha"
    amount = 10.0
    filename = "accounts.json"
    res = withdraw(filename, username, 10.0)
    assert(res == (True, 10.0))
    print("banking file")
