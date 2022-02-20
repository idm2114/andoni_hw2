### Written by Ian Macleod (idm2114) and Imanol Uribe (iu2155) 
### for COMS 4342 HW2 Q2B

import random
import copy 
import math
import collections


# scale factor by which we increase size of arrays for sketches
# each of the log_n sketches has size O(k) = 100k
C = 100

def universal_hash(n, k, numHashFunctions):
    # smallest prime > 1000000 = 10000019
    p = 10000019
    H = []
    for i in range(numHashFunctions):
        a = random.randint(0,p-1)
        if a % 2 == 0:
            a += 1
        b = random.randint(0,p-1)
        H.append([a,b,p])
    return H

def eval_h(itm, hash_function, k):
    a = hash_function[0]
    b = hash_function[1]
    p = hash_function[2]
    return int(int((a * itm + b) % p) % (C*k))

## creating sets with symmetric difference of size k and size n + k/2
def generate_sets(n,common,k):
    Alice = set() 

    target_different = set()

    # init two sets with common elements
    while(len(Alice) < common):
        tmp = random.randint(1,n)
        Alice.add(tmp)

    Bob = copy.copy(Alice)

    for j in range(k):
        if j % 2 == 0 and j > 1:
            tmp = random.randint(1,n)
            while tmp in Bob or tmp in Alice:
                tmp = random.randint(1,n)
            Alice.add(tmp)
            target_different.add(tmp)
        else:
            tmp = random.randint(1,n)
            while tmp in Bob or tmp in Alice:
                tmp = random.randint(1,n)
            Bob.add(tmp)
            target_different.add(tmp)

    return list(Alice), list(Bob), list(target_different)

def generate_sketches(Alice, Bob, H, k):
    '''
    input: Alice's set, 
           Bob's set,  
           hash function family H, 
           symmetric difference cardinality |A \Delta B| = k
    '''
    a_sketch = []
    b_sketch = []
    # for each of the hash functions
    for i in range(len(H)):
        current_hash = H[i]
        a_curr = [ 0 for x in range(C * k) ]
        b_curr = [ 0 for x in range(C * k) ]
        for itm in Alice:
            a_curr[eval_h(itm, current_hash, k)] += itm
        for itm in Bob:
            b_curr[eval_h(itm, current_hash, k)] += itm
        a_sketch.append(a_curr)
        b_sketch.append(b_curr)
    return a_sketch, b_sketch

def recovery(a_sketch, b_sketch, k):
    stream = []
    for i in range(len(a_sketch)):
        diff = [ a_sketch[i][j] - b_sketch[i][j] for j in range(len(a_sketch[i])) ] 
        for itm in diff:
            if itm != 0:
                stream.append(abs(itm))
    
    ## getting top k elements in stream
    c = collections.Counter(stream)
    return [ x[0] for x in c.most_common(k) ]

if __name__=='__main__':
    success_count = 0
    num_trials = 100
    for i in range(num_trials):
        n = 100000000
        common = 10000
        k = 500
        alice, bob, target_different = generate_sets(n,common,k)
        H = universal_hash(n, k, math.floor(math.log2(n)))
        a_sketch, b_sketch = generate_sketches(alice, bob, H, k)
        estimated_different = recovery(a_sketch, b_sketch, k)
        if set(estimated_different) == set(target_different):
            success_count+=1
    print("Summary statistics:")
    print(f"num trials = {num_trials}\nAlice and Bob set size = {common+int(k/2)}\n|symmetric difference| = {k}\nUniverse=(1,...,{n})")
    print(f"Success rate is {100 * success_count / num_trials}%")

