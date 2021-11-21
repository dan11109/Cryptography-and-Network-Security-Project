# Cryptography-and-Network-Security-Project

Project for encrypted banking trasactions using RSA and triple DES. 

Group Members:
- Will Hawkins (hawkiw2@rpi.edu)
- Brian Hotopp (hotopb@rpi.edu)
- Dan Stevens (steved7@rpi.edu)


Overview: 

-1. Bank Establishes Communication Channel

0. Client connects to channel.

1. Client: generate p,q,e,d using RSA and send {e,N} to Bank. 

2. Bank: Receive {e,N}, send {CDES,Chmac} where CDES = KDES^e mod N and CHMAC = KHMAC^e mod N

3. Client: Receive {CDES,CHMAC} and decrypt them where KDES = CDES^d mod N and KHMAC = CHMAC^d mod N. Now both the bank and cleint have DES and HMAC keys. 

4. Client: sends bank DES\[username, password + HMAC(username, password)] using DES to encrypt the message 

5. Bank: decrypts this message and validates that this user has an account and the password is correct. (the usernames and passwords are set before hand)

6. Bank: send DES\[ok / invalid credentials  + HMAC(ok / invalid credentials  )] to client

7. Client: if received ok send bank transaction, if invalid credentials quit connection and start back at step 1 again. 

8. Bank: send confirmation of transaction when received from client





