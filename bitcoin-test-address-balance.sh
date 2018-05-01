#!/bin/bash
STRING=$1
echo -n "$STRING"
echo -n "$STRING" | openssl dgst -sha256 | awk -F'= ' '{print $2}' | ./bitcoin-public-from-private.py | ./bitcoin-address-from-public-key.py | grep address | awk -F'= ' '{print $2;}' | xargs -I {} ./bitcoin-get-address-balance.py {}