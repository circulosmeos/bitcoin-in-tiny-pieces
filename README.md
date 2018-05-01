# bitcoin in tiny pieces

These are Python scripts made from scracth (only *bitcoin* dependency is *base58*) to play with Bitcoin addresses: public, private, WIF...

The scripts are compatible with Python 2 and Python 3.

## examples of use

	$ ./bitcoin-public-from-private.py 0x01
		79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798 483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8

	$ ./bitcoin-public-from-private.py 0x01 | ./bitcoin-address-from-public-key.py
		pubkey = 0479be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8

		Compressed public key:
		key_hash =      751e76e8199196d454941c45d1b3a323f1433bd6
		checksum =      510d1634d943109b69da527ef5948106f22b655fb5193b4e9ef7e4dcd342d245
		key_hash + checksum =   00751e76e8199196d454941c45d1b3a323f1433bd6 510d1634
		bitcoin address =       1BgGZ9tcN4rm9KBzDn7KprQz87SZ26SAMH

		Uncompressed public key:
		key_hash =      91b24bf9f5288532960ac687abb035127b1d28a5
		checksum =      0074ffe0526d823be09b39865422a1d6135afc85afb0a6863c58e9fe89989170
		key_hash + checksum =   0091b24bf9f5288532960ac687abb035127b1d28a5 0074ffe0
		bitcoin address =       1EHNa6Q4Jz2uvNExL497mE43ikXhwF6kZm

	$ echo 0x01 | ./bitcoin-wif-private-key.py
		privkey = 8001

		For compressed public key:
		checksum =      553bc06a6f4e0f4d575a9b43e2eb82546131dccec1c3a99151ee08cb5972c8a9
		key + checksum =        800101 553bc06a
		bitcoin address =       5rM1SJieKB

		For uncompressed public key:
		checksum =      e27a1d3a74fa86f9a913e996663ea76fc2333c3b77ae33ff18349a549fd36721
		key + checksum =        8001 e27a1d3a
		bitcoin address =       26k9aD1PF

	$ ./bitcoin-public-from-private.py 0x01 | ./bitcoin-address-from-public-key.py | grep address | awk -F'= ' '{print $2;}' | xargs -I {} ./bitcoin-get-address-balance.py {}

	address         = 1BgGZ9tcN4rm9KBzDn7KprQz87SZ26SAMH
	total_received  = 0.14609494 Bitcoin
	final_balance   = 0 Bitcoin

	address         = 1EHNa6Q4Jz2uvNExL497mE43ikXhwF6kZm
	total_received  = 4.87126141 Bitcoin
	final_balance   = 0 Bitcoin

	# changing *VERBOSE* to *False* on *bitcoin-address-from-public-key.py* the previous command is shorter:
	# ./bitcoin-public-from-private.py 0x01 | ./bitcoin-address-from-public-key.py | xargs -I{} ./bitcoin-get-address-balance.py {}

	# Use a SHA256 hashed string as private key, and check if it has been used:
	$ ./bitcoin-test-address-balance.sh satoshi
	satoshi
	address         = 1ADJqstUMBB5zFquWg19UqZ7Zc6ePCpzLE
	total_received  = 0.00375370 Bitcoin
	final_balance   = 0 Bitcoin

	address         = 1xm4vFerV3pSgvBFkyzLgT1Ew3HQYrS1V
	total_received  = 0.00111100 Bitcoin
	final_balance   = 0 Bitcoin

## License

Release under [GPL 3](https://www.gnu.org/licenses/gpl-3.0.en.html).