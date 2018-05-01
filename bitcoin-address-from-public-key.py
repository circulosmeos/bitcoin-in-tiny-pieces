#!/usr/bin/env python
# (Python 2 & python 3 compatible)
# Construct a Bitcoin address from the public key
# by circulosmeos //github.com/circulosmeos/bitcoin-in-tiny-pieces
#
# patched from //bitcoin.stackexchange.com/questions/56923/is-this-how-to-generate-a-bitcoin-address-with-python
# //en.bitcoin.it/wiki/Protocol_documentation#Addresses

import hashlib
import base58
import sys
import fileinput
from re import match

# ECDSA bitcoin Public Key
pubkey = ''
# See 'compressed form' at https://en.bitcoin.it/wiki/Protocol_documentation#Signatures
COMPRESS_PUBKEY = 2 # 0: uncompressed, 1: compressed, 2: print both!

VERBOSE = False

x = ''
y = ''
line = ''

def hash160(hex_str):
    sha = hashlib.sha256()
    rip = hashlib.new('ripemd160')
    sha.update(hex_str)
    rip.update( sha.digest() )
    if (VERBOSE): print ( "key_hash = \t" + rip.hexdigest() )
    return rip.hexdigest()  # .hexdigest() is hex ASCII

# try to read parameters or stdin if they exist (in this order)
if (len(pubkey)==0):

    # read parameters from cmdline
    if ( len(sys.argv) == 2 ):
        x = sys.argv[1]
    elif ( len(sys.argv) == 3 ):
        x = sys.argv[1]
        y = sys.argv[2]
    else:
        # tries to read stdin
        try:
            for x in fileinput.input('-'):
                break
        except:
            pass

    # compose pubkey from data read
    line = x + y
    m = match(r'(?:0x)?(?:04)?([a-fA-F0-9]{1,64})L? *(?:0x)?([a-fA-F0-9]{1,64})L?$', line)
    if ( m is not None ):
        (x, y) = m.group(1, 2)
        pubkey = '04' + x + y
    else:
        if (VERBOSE): print("\n./bitcoin-address-from-public-key [04][128 hex]\n./bitcoin-address-from-public-key [04][x 64 hex] [y 64 hex]\n")
        exit(1)

if (VERBOSE): print ('pubkey = ' + pubkey)

compress_pubkey = COMPRESS_PUBKEY
if (COMPRESS_PUBKEY == 2):
    compress_pubkey = 1

while (compress_pubkey <= COMPRESS_PUBKEY):

    if (compress_pubkey==1):
        if (VERBOSE): print ("\nCompressed public key:")
        if (ord(bytearray.fromhex(pubkey[-2:])) % 2 == 0):
            pubkey_compressed = '02'
        else:
            pubkey_compressed = '03'
        pubkey_compressed += pubkey[2:66]
        hex_str = bytearray.fromhex(pubkey_compressed)
    else:
        if (VERBOSE): print ("\nUncompressed public key:")
        hex_str = bytearray.fromhex(pubkey)

    # Obtain key:

    key_hash = '00' + hash160(hex_str)

    # Obtain signature:

    sha = hashlib.sha256()
    sha.update( bytearray.fromhex(key_hash) )
    checksum = sha.digest()
    sha = hashlib.sha256()
    sha.update(checksum)
    checksum = sha.hexdigest()[0:8]

    if (VERBOSE): print ( "checksum = \t" + sha.hexdigest() )

    if (VERBOSE): print ( "key_hash + checksum = \t" + key_hash + ' ' + checksum )
    if (VERBOSE): 
        sys.stdout.write ( "bitcoin address = \t" )
    print ( (base58.b58encode( bytes(bytearray.fromhex(key_hash + checksum)) )).decode('utf-8') )

    compress_pubkey+=1