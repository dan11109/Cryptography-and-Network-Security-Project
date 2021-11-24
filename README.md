# Cryptography-and-Network-Security-Project

Project for encrypted banking trasactions using RSA and triple DES. 

Group Members:
- Will Hawkins (hawkiw2@rpi.edu)
- Brian Hotopp (hotopb@rpi.edu)
- Dan Stevens (steved7@rpi.edu)


Overview: 

1. Bank establishes server
2. Client connects to server
3. Client sends public RSA keys [e,N]
4. Bank encrypts DES key using RSA and sends to Client
    Client decrypts DES key using private RSA keys.
    All future communication uses DES.
5. Client sends username and passwords to the Bank.
6. Bank verifies username and passwords.
    a) If login credentials are valid, proceed to ATM mode.
    b) If invalid, terminate connection and exit.






