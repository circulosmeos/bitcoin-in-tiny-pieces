#!/usr/bin/env python
# (Python 2 & python 3 compatible)
# Calculate public (x, y) bitcoin key from private bitcoin key (secret)
# by circulosmeos //github.com/circulosmeos/bitcoin-in-tiny-pieces
#
# modified from:
# //bitcoin.stackexchange.com/questions/25024/how-do-you-get-a-bitcoin-public-key-from-a-private-key/29880#25039
#
import sys
import fileinput
from re import match

VERBOSE = 0 # 0 (None), 1, 2

class CurveFp( object ):
    def __init__( self, p, a, b ):
        self.__p = p
        self.__a = a
        self.__b = b

    def p( self ):
        return self.__p

    def a( self ):
        return self.__a

    def b( self ):
        return self.__b

    def contains_point( self, x, y ):
        return ( y * y - ( x * x * x + self.__a * x + self.__b ) ) % self.__p == 0

class Point( object ):
    def __init__( self, curve, x, y, order = None ):
        self.__curve = curve
        self.__x = x
        self.__y = y
        self.__order = order
        if self.__curve: assert self.__curve.contains_point( x, y )
        if order: assert self * order == INFINITY

    def __add__( self, other ):
        if other == INFINITY: return self
        if self == INFINITY: return other
        assert self.__curve == other.__curve
        if self.__x == other.__x:
            if ( self.__y + other.__y ) % self.__curve.p() == 0:
                return INFINITY
            else:
                return self.double()

        p = self.__curve.p()
        l = ( ( other.__y - self.__y ) * \
                    inverse_mod( other.__x - self.__x, p ) ) % p
        x3 = ( l * l - self.__x - other.__x ) % p
        y3 = ( l * ( self.__x - x3 ) - self.__y ) % p
        return Point( self.__curve, x3, y3 )

    def __mul__( self, other ):
        def leftmost_bit( x ):
            assert x > 0
            result = 1
            while result <= x: result = 2 * result
            return result / 2

        e = other
        if self.__order: e = e % self.__order
        if e == 0: return INFINITY
        if self == INFINITY: return INFINITY
        assert e > 0
        e3 = 3 * e
        negative_self = Point( self.__curve, self.__x, -self.__y, self.__order )
        i = int(leftmost_bit( e3 ) / 2)
        result = self
        while i > 1:
            result = result.double()
            if ( e3 & i ) != 0 and ( e & i ) == 0: result = result + self
            if ( e3 & i ) == 0 and ( e & i ) != 0: result = result + negative_self
            i = int(i / 2)
        return result

    def __rmul__( self, other ):
        return self * other

    def __str__( self ):
        if self == INFINITY: return "infinity"
        return "(%d,%d)" % ( self.__x, self.__y )

    def double( self ):
        if self == INFINITY:
            return INFINITY

        p = self.__curve.p()
        a = self.__curve.a()
        l = ( ( 3 * self.__x * self.__x + a ) * \
                    inverse_mod( 2 * self.__y, p ) ) % p
        x3 = ( l * l - 2 * self.__x ) % p
        y3 = ( l * ( self.__x - x3 ) - self.__y ) % p
        return Point( self.__curve, x3, y3 )

    def x( self ):
        return self.__x

    def y( self ):
        return self.__y

    def curve( self ):
        return self.__curve

    def order( self ):
        return self.__order

INFINITY = Point( None, None, None )

def inverse_mod( a, m ):
    if a < 0 or m <= a: a = a % m
    c, d = a, m
    uc, vc, ud, vd = 1, 0, 0, 1
    while c != 0:
        q, c, d = divmod( d, c ) + ( c, )
        uc, vc, ud, vd = ud - q*uc, vd - q*vc, uc, vc
    assert d == 1
    if ud > 0: return ud
    else: return ud + m

# secp256k1
_p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
_r = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
_b = 0x0000000000000000000000000000000000000000000000000000000000000007
_a = 0x0000000000000000000000000000000000000000000000000000000000000000
_Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
_Gy = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8

class Public_key( object ):
    def __init__( self, generator, point ):
        self.curve = generator.curve()
        self.generator = generator
        self.point = point
        n = generator.order()
        if not n:
            raise RuntimeError( "Generator point must have order." )
        if not n * point == INFINITY:
            raise RuntimeError( "Generator point order is bad." )
        if ( (point.x() is None or point.y() is None) or 
                point.x() < 0 or n <= point.x() or point.y() < 0 or n <= point.y() ):
            raise RuntimeError( "Generator point has x or y out of range." )

curve_256 = CurveFp( _p, _a, _b )
generator_256 = Point( curve_256, _Gx, _Gy, _r )
g = generator_256

if __name__ == "__main__":

    if (VERBOSE == 2): print ('='*73)
    
    ### set privkey
    secret = 0x0
    
    # try to read parameters or stdin if they exist (in this order)
    # read parameter from cmdline
    if ( len(sys.argv) >= 2 ):
        secret = sys.argv[1]
    else:
        # tries to read stdin
        try:
            for secret in fileinput.input('-'):
                break
        except:
            pass

    # check for secret correcteness
    m = match(r' *(?:0x)?([a-fA-F0-9]{1,64})L?', secret)
    if ( m is not None ):
        secret = int( m.group(1), 16)
    else:
        print("\n./bitcoin-public-from-private [hex private key]\n")
        exit(1)

    # print (privkey)
    if (VERBOSE >= 1): print ('secret = ' + "{0:0{1}x}".format( secret,64 ))

    # generate pubkey
    pubkey = Public_key( g, g * secret )
    
    # print (pubkey)
    BREAK_LINE = ''
    if (VERBOSE >= 1): 
        sys.stdout.write('pubkey = ')
        if (VERBOSE == 2): BREAK_LINE = "\n\t"
    print ("{0:0{1}x}".format( pubkey.point.x(),64 ) + BREAK_LINE + " {0:0{1}x}".format( pubkey.point.y(),64 ))
    
    if (VERBOSE == 2): print ('='*73)
