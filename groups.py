from math import gcd, factorial
from sympy import isprime
import time

"""
    TODO
    Metacylic groups
    schnorr groups                          ✓
    order permutations better               ✓
    get generators of group
    compute automorphism                    ✓
    Aut(G)
    outer automorphisms (Aut(G)/Inn(G))
    stabilizer/ group orbits?
    compute order in O(n) instead of O(n*logn)
    is abelian in O(n)
    semidirect product
"""

"""
    Z/nZ
"""
def cyclic(n):
    return [[(i+j)%n for i in range(n)] for j in range(n)]

"""
    group of symettries of a n-gon
"""
def dihedral(n):
    return [[(k+g)%n + k//n*n if g < n else ((g+(n-1)*k)%n + (k//n+1)*n)%(2*n) for k in range(2*n)] for g in range(2*n)]

"""
    symmetric group of permutations of n letters
"""
def symmetric(n):
    if n == 1:
        return [[0]]

    H = symmetric(n-1)
    G = [[H[i%len(H)][j] + i//len(H)*len(H) for j in range(len(H))] for i in range(len(H)*n)]
       
    blockwidth = len(H)
    for col in range(1,n):
        rowwidth = blockwidth//(n-col)
        for block in range(len(G)//blockwidth):
            blockdest = block//(n-col+1)*(n-col+1)
            for row in range(blockwidth//rowwidth):
                if blockdest == block:
                    blockdest += 1
                rowindex = (block if block < blockdest else block-1)%(n-col+1)
                for i in range(rowwidth):
                    G[blockdest*blockwidth+rowindex*rowwidth+i].extend(G[block*blockwidth+row*rowwidth+i][(col-1)*len(H):col*len(H)])
                blockdest+=1
        blockwidth = rowwidth
    return G

"""
    multiplicative group modulo n
"""
def mult(n):
    H = [k for k in range(1,n) if gcd(k,n)==1]
    return __multGroup(H,n)

"""
    
"""
def __multGroup(H_, n):
    H = {H_[i]:i for i in range(len(H_))}
    return [[H[(H_[i]*H_[j])%n] for i in range(len(H_))] for j in range(len(H_))]

"""
    https://math.dartmouth.edu/~carlp/PDF/paper55.pdf
"""
def falseWitness(n):
    H = [k for k in range(1,n) if modpow(k,n-1,n) == 1]
    return __multGroup(H,n)

def schnorr(p,q):
    assert(isprime(p))
    assert(isprime(q))
    r = (p-1)//q
    assert(p-1==q*r)
    h = 0
    for i in range(2,p):
        if i**r%p!=1:
           h = i
           break

    assert(h!=0)
    
    g = h**r%p

    H = [g**i%p for i in range(q)]
    
    return __multGroup(H,p)

"""
    direct product of A and B
"""
def direct(A, B):
    return [[(A[b%len(A)][a%len(A)]+B[b//len(A)][a//len(A)]*len(A))%(len(A)*len(B)) for a in range(len(A)*len(B))] for b in range(len(A)*len(B))]

"""
    returns the orders of all elements of G
"""
def orders(G, returndict:bool = False):
    o = {0:1}

    elements = set(G[0][1:])
##    divisors = [k for k in range(1,len(G)) if len(G)%k == 0]      divset = {divisors[i]:i for i in range(len(divisors))}          gcds = [[gcd(divisors[i],divisors[j]) for j in range(len(divisors))] for i in range(len(divisors))]
    
    while len(elements) > 0:
        g = elements.pop()
        product = g
        powers = []
        while product != 0:
            powers.append(product)
            product = G[g][product]
        orderg = len(powers)+1
        o[g] = orderg
        for i in range(1,len(powers)):
            if powers[i] in o:
                continue
##            if i+1 in divset:         order = orderg//gcds[divset[i+1]][divset[orderg]]           print(divisors[divset[i+1]],divisors[divset[orderg]],gcds[divset[i+1]][divset[orderg]])         else:         order = orderg
            o[powers[i]] = orderg//gcd(i+1,orderg)
            elements.remove(powers[i])

    if returndict:
        return o

    return [o[i] for i in range(len(G))]

"""
    return orders of all elements of the subset H of G
"""
def ordersSub(G, H):
    o = list()
    for g in range(len(H)):
        order = 1
        product = H[g]
        while product != 0:
            product = G[H[g]][product]
            order += 1
        o.append(order)
    return o    

"""
    returns a set of generators of G
"""
def generators(G):
    o = orders(G)
    e = G[0][:]
    gens = list()
    order = 1
    while order < len(G):
        maxorder = max(o)
        order*=maxorder
        gen = e[o.index(maxorder)]
        product = 0
        print(o)
        print(e)
        for i in range(maxorder):
            try:
                del o[e.index(product)]
                e.remove(product)
            except ValueError:
                pass
            product = G[gen][product]
        gens.append(gen)
    return gens

def isAbelian(G):
    for i in range(1,len(G)):
        for j in range(i+1,len(G)):
            if G[i][j] != G[j][i]:
                return False
    return True

def isCyclic(G):
    if len(G) <= 3:
        return True
    for g in range(1,len(G)):
        order = 1
        product = g
        while product != 0:
            product = G[g][product]
            order += 1
        if order == len(G):
            return True
    return False

def isNormal(G,N):
    return "A programar listillo"

"""
    returns the center of G
    Z(G) = {g∈G | ∀k ∈ G  k*g = g*k}
"""
def center(G):
    Z = list()
    for i in range(len(G)):
        c = True
        for j in range(len(G)):
            if G[i][j] != G[j][i]:
                c = False
                break
        if c:
            Z.append(i)
    return Z

def centralizer(G, S):
    C = list()

    for g in range(len(G)):
        c = True
        for s in range(len(S)):
            if G[g][S[s]] != G[S[s]][g]:
                c = False
                break
        if c:
            C.append(g)

    return C
    
def normalizer(G, S):
    N = list()

    for g in range(len(G)):
        if leftcoset(G, S, g) == rightcoset(G, S, g):
            N.append(g)
    return N

"""
    gH = {gh : h∈H}
"""
def leftcoset(G, H, g):
    coset = set()

    for h in range(len(H)):
        coset.add(G[g][H[h]])

    return coset

"""
    Hg = {hg : h∈H}
"""
def rightcoset(G, H, g):
    coset = set()

    for h in range(len(H)):
        coset.add(G[H[h]][g])

    return coset

"""
    If H is a normal subgroup of G, then gH = Hg ∀g ∈ G
    and we can define the quotient group G/H = {gH : g∈G}
"""
def quotient(G, H):
    Q = list()
    m = set()
    elements = set()
    cosets = list()

    for g in range(len(G)):
        for h in range(len(H)):
            gh = G[g][H[h]]
            if gh not in m:
                m.add(gh)
                elements.add(g)
            else:
                break
    cosets = [leftcoset(G, H, e) for e in elements]
    elements = list(elements)
    
    Q = [[cosets.index(leftcoset(G,H,G[g1][g2])) for g2 in elements] for g1 in elements]

    return Q

"""
    semidirect product of G and H
"""
def semidirect(G,H,automorphism):
    return "Illo programame"

"""
    returns an automorphism given the images of the generators
"""
def automorphism(G, genimg: dict):
    bijection = [0 for i in range(len(G))]

    elements = set(G[0])
    
    s = [[0]]

    for g in genimg.keys():
        subgroup = [0]
        product = g
        bijection[g] = genimg[g]
        while product != 0 and product in elements:
            subgroup.append(product)
            elements.remove(product)
            product = G[g][product]
        s.append(subgroup)

    for H in s:
        for i in range(1,len(H)):
            bijection[H[i]] = G[bijection[H[1]]][bijection[H[i-1]]]

    k = 0
    while k < len(s)-1:
        sn = list()
        for i in range(0,len(s[k])):
            for j in range(0,len(s[k+1])):
                g = G[s[k][i]][s[k+1][j]]
                bijection[g] = G[bijection[s[k][i]]][bijection[s[k+1][j]]]
                sn.append(g)
        del(s[k+1])
        s[k] = sn
        
    return bijection
        
        
"""
    group of automorphisms of G
"""
def Aut(G, gens: set):
    o = ordersDict(G)
    
    return G

"""
    group of inner automorphisms of G
    Inn(G) = G/Z(G)
"""
def Inn(G):
    return quotient(G, center(G))

"""
    outter automorphisms of G
    Out(G) = Aut(G)/Inn(G)
"""
def Out(G):
    return quotient(Aut(G),Inn(G))

def toString(G):
    print(str(G).replace("], ", "]\n").replace("[[","[").replace("]]","]"))

"""
Utils
"""

"""
    returns (a^b)%n
"""
def modpow(a, b, n):
    r = 1
    while b > 0:
        if b & 1 == 1:
            r = r*a%n
        b //= 2
        a = a*a%n
    return r


"""
DEPRECATED METHODS
"""


#Returns orders of elements of G
def ordersDepr(G):
    o = list()
    for g in range(len(G)):
        order = 1
        product = g
        while product != 0:
            product = G[g][product]
            order += 1
        o.append(order)
    return o



def directDepr(A, B):
    G = [[0 for b in range(len(B)*len(A))] for a in range(len(A)*len(B))]
    for y in range(len(B)):
        for x in range(len(B)):
            for g in range(len(A)):
                for k in range(len(A)):
                    G[g+y*len(A)][k+x*len(A)] = (A[g][k]+B[y][x]*len(A))%len(G)
    return G


def symmetricDepr(n):
    perms = permutations([k for k in range(0,n)])
    return [[perms.index(permcomp(perms[g],perms[h])) for h in range(len(perms))] for g in range(len(perms))]

def permcomp(p1, p2):
    return [p2[p1[i]] for i in range(len(p1))]

def permutations(l):
    perms = []
    if len(l)==1:
        return [l]
    for i in range(len(l)):
        trasposition = l[:]
        trasposition[i] = trasposition[0]
        iperms = permutations(trasposition[1:])
        for p in iperms:
            perm  = [l[i]]
            perm.extend(p)
            perms.append(perm)
    
    return perms
