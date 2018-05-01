#!/usr/bin/env python
# (Python 2 & python 3 compatible)
# Get final balance of a bitcoin address from blockchain.info json
# by circulosmeos https://github.com/circulosmeos/bitcoin-in-tiny-pieces

import sys
import fileinput
import re
from time import sleep

try:    # python3
    from urllib.request import urlopen
except: # python2
    from urllib2 import urlopen

BELL = True
WARNING_WAITING_TIME = 0

blockchain_tags = [ 
    'total_received',
    'final_balance',
    ]

SATOSHIS_PER_BITCOIN = 1e+8

#
# try to read parameters or stdin if they exist (in this order)
#
address = ''
# read parameter from cmdline
if ( len(sys.argv) >= 2 ):
    address = sys.argv[1]
else:
    # tries to read stdin
    try:
        for address in fileinput.input('-'):
            break
    except:
        pass

# check address (loose) correcteness
m = re.match(r' *([a-zA-Z1-9]{1,34})$', address)
if ( m is not None ):
    address = m.group(1)
else:
    print( "\nBitcoin address invalid\n\n./bitcoin-get-address-balance [bitcoin address]\n" )
    exit(1)

#
# get address info from blockchain.info
#

reading=1
while (reading):
    try:
        htmlfile = urlopen("https://blockchain.info/address/%s?format=json" % address)
        reading  = 0
    except:
        reading=1
        print( "..." )
        sleep(60)

htmltext = htmlfile.read().decode('utf-8')

blockchain_info = []
tag = ''
try:
    for tag in blockchain_tags:
        blockchain_info.append (
            float( re.search( r'%s":(\d+),' % tag, htmltext ).group(1) ) )
except:
    print( "Error processing tag '%s'." % tag );
    exit(1)

print( "\naddress \t= " + address )

for i, coins in enumerate(blockchain_info):

    sys.stdout.write ("%s \t= " % blockchain_tags[i])
    if coins > 0.0:
        print( "%.8f Bitcoin" % (coins/SATOSHIS_PER_BITCOIN) );
    else:
        print( "0 Bitcoin" );

    if (BELL and blockchain_tags[i] == 'final_balance' and coins > 0.0): 
        # funny bell when something is found
        sys.stdout.write ('\a\a\a\a\a\a')
        sys.stdout.flush()
        if (WARNING_WAITING_TIME>0):
            sleep(WARNING_WAITING_TIME)
        else:
            exit (2)

print('')
