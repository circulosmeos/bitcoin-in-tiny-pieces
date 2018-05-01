#!/usr/bin/env python
# (Python 2 & python 3 compatible)
# Construct a WIF private key from the hex secret key
# by circulosmeos https://github.com/circulosmeos/bitcoin-in-tiny-pieces
#
# https://en.bitcoin.it/wiki/Wallet_import_format

import hashlib
import base58
import sys
import fileinput
from re import match

privkey = ''
# See 'compressed form' at https://en.bitcoin.it/wiki/Protocol_documentation#Signatures
COMPRESS_PUBKEY = 2 # 0: uncompressed, 1: compressed, 2: print both!

VERBOSE = True

line = ''

# try to read parameters or stdin if they exist (in this order)
if (len(privkey)==0):

    # read parameters from cmdline
    if ( len(sys.argv) >= 2 ):
        line = sys.argv[1]
    else:
        # tries to read stdin
        try:
            for line in fileinput.input('-'):
                break
        except:
            pass

    # compose privkey from data read
    m = match(r'(?:0x)?(?:80)?([a-fA-F0-9]{1,64})L?', line)
    if ( m is not None ):
        privkey = '80' + m.group(1)
    else:
        if (VERBOSE): print("\n./bitcoin-wif-private-key [80][64 hex]\n")
        exit(1)

if (VERBOSE): print ('privkey = ' + privkey)

compress_pubkey = COMPRESS_PUBKEY
if (COMPRESS_PUBKEY == 2):
    compress_pubkey = 1

while (compress_pubkey <= COMPRESS_PUBKEY):

    key = privkey

    if (compress_pubkey==1):
        if (VERBOSE): print ("\nFor compressed public key:")
        key += '01'
    else:
        if (VERBOSE): print ("\nFor uncompressed public key:")

    # Obtain signature:

    sha = hashlib.sha256()
    sha.update( bytearray.fromhex(key) )
    checksum = sha.digest()
    sha = hashlib.sha256()
    sha.update(checksum)
    checksum = sha.hexdigest()[0:8]

    if (VERBOSE): print ( "checksum = \t" + sha.hexdigest() )

    if (VERBOSE): print ( "key + checksum = \t" + key + ' ' + checksum )
    if (VERBOSE): 
        sys.stdout.write ( "bitcoin address = \t" )
    print ( (base58.b58encode( bytes(bytearray.fromhex(key + checksum)) )).decode('utf-8') )

    compress_pubkey+=1