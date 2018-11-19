#!/usr/bin/env python
# (Python 2 & python 3 compatible)
# Get final balance of a bitcoin address from blockchain.info json
# by circulosmeos //github.com/circulosmeos/bitcoin-in-tiny-pieces
#
# This brainwallet version hacked up by jamesyoungdigital
# //github.com/jamesyoungdigital/bitcoin-in-tiny-pieces
#
# Borrowed some code from pybitcointools in my repo, where I added a
# bci_unspent2 function. Requires pybitcointools from my repo
#

# For Python 2
from __future__ import division
from bitcoin import *

# Just in case you want to hack on this script, see:
# https://github.com/StealingBitcoinWithMath/StealingBitcoinWithMath
# From Ryan Castellucci, Defcon 23/2015 (check out this one first), check
# YouTube for his talk.
# Another very interesting talk co-hosted with Ryan:
# https://speakerdeck.com/filosottile/stealing-bitcoin-with-math-hope-xi


VERBOSE = False        # if True, all json is printed.
BELL = True            # False if you don't want the funny bell noise :)
SATOSHIS_PER_BITCOIN = 1e+8
SATOSHIS_IN_BITCOINS = 10000000000

#
# try to read brainwallet password/passphrase from command line, else
# try to read the password/passphrase from stdin
#

address = ''

# read parameter from cmdline
if ( len(sys.argv) == 2 ):
    address = sys.argv[1]
else:
    # tries to read stdin
    try:
        for address in fileinput.input('-'):
            break
    except:
        pass

#
# get address info from blockchain.info
#

priv = sha256(address)  # Actually, password/passphrase not address
pub = privtopub(priv)   # Get pub addr from priv key
addr = pubtoaddr(pub)   # Get the 1Btc... address


print( "\nbrainwallet address '{}'\n\taddress {}\n".format(address, addr) )


h = history(addr)       # Does this brainwallet have any history?

#
#   You can do if len(h) == 0 or if len(h) >= 0
#   then go onto unspent.  You might get an address with no spends
#   but a balance if len(h) == 0
#
#   Lots of output for very popular addresses, brainwallets like
#   'battery horse correct staple', avoid these ones
#
#

if len(h) >= 0:

    # This could dump crap on rate-limiting, or throw an exception
    u = unspent(addr)

    # Change to different key if using something other than bci_unspent2
    if u[0]['balance'] > 0:

        spendable = u[0]['balance']
        spendable_btc = u[0]['balance'] / SATOSHIS_IN_BITCOINS

        # funny bell when something is found
        if BELL == True:
            sys.stdout.write ('\a\a\a\a\a\a')

        print("Brainwallet address: '{}'\nPrivKey: {}\nPubKey: {}\nAddress: {}".format(address, priv, pub, addr))
	print("Balance: {} Satoshis\nBalance: {:f} BTC\n".format(spendable, spendable_btc))

    else:

	print("No balance for brainwallet address '{}'".format(address))
