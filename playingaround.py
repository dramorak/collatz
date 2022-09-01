#python
import random
import mutility 
from multiprocessing import Process

def collatzStep(n):
    if n % 2 == 0:
        return n // 2
    else:
        return 3 * n + 1

def inverseCollatzStep(n):
    if n % 6 == 4:
        return (n - 1) // 3
    else:
        return n * 2

def collatzSequenceLength(n):
    result = 0
    while n != 1:
        result += 1
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
    return result

def maxLength(start, end):
    #finds the number i of max sequence length between [start, end]
    idx = 0
    m = 0
    for i in range(start, end):
        l = collatzSequenceLength(i)
        if l > m:
            idx = i
            m = l
    return (idx, m)

def constructLongSequence(n, end = 10 ** 101):
    length = 0
    while n < end and length < 1000:
        length += 1
        n = inverseCollatzStep(n)
    return length

def isPrime(n):
    for i in range(2, int(n ** (1/2)) + 1):
        if n % i == 0:
            return i
    return -1

def kSteps(c3, d, k, n):
    #skips the computation forward k steps.
    #c3 and d are special dictionaries that contain some precomputed values.
    a = n >> k
    b = n % (2 ** k)

    return c3[b] * a + d[b]

def collatzSequenceLength_shortened(n, k, c, c3, d, l):
    #finds the collatz sequence length of a number n
    result = 0
    mod = 2 ** k - 1
    while n > mod:
        #jump k steps
        a = n >> k
        b = n & mod

        n = c3[b]*a + d[b]
        result += k + c[b]
    return result + l[n]

def computeC(k):
    #returns the C mapping for numbers in [1, 2 ** k]
    #the c mapping is the number of increasing sub-steps in the (shortened) collatz sequence.
    c = []
    for i in range(0, 2 ** k):
        n = i
        r = 0
        for j in range(k):
            if n%2 == 0:
                n = n // 2
            else:
                n = (3*n + 1) / 2
                r += 1
        c.append(r)
    return c

def computeD(k):
    #returns the d mapping on integers [0, 2 ** k - 1].
    #The D mapping is the result of applying the collatz step k times.
    d = []
    for i in range(2 ** k):
        n = i
        for j in range(k):
            if n % 2 == 0:
                n = n//2
            else:
                n = (3*n + 1) // 2
        d.append(n)
    return d

def computeC3(c):
    #precomputes powers of 3 for elements in c
    r = []
    for k in c:
        r.append(3 ** k)
    return r

def computeLengths(k):
    #computes all collatz sequence lengths from 0 to 2 ** k - 1
    l = [0]
    for i in range(1, 2 ** k):
        n = i
        r = 0
        while n != 1:
            if n%2 == 0:
                n = n // 2
                r += 1
            else:
                n = (3*n + 1)//2
                r += 2
        l.append(r)
    return l

def tests():
    #test shortened_collatz
    c = computeC(15)
    d = computeD(15)
    c3 = computeC3(c)
    l = computeLengths(15)
    print("Testing...")
    #manual
    inputs = [27,29,30,31,32,33, 2**2, 2**3, 2**4, 2**5, 2**6, 2**7, 2**8, 2**9, 2**10, 2**11, 2**12, 2**13, 2**14]
    for bigNum in inputs:
        colLength = collatzSequenceLength_shortened(bigNum, 20, c, c3, d, l)
        realColLength = collatzSequenceLength(bigNum)
    
    #bash
    for i in range(1, 10000):
        colLength = collatzSequenceLength_shortened(bigNum, 20, c, c3, d, l)
        realColLength = collatzSequenceLength(bigNum)
        assert colLength == realColLength

    #BIGBASH
    for i in range(10**99, 10**99 + 100):
        colLength = collatzSequenceLength_shortened(bigNum, 20, c, c3, d, l)
        realColLength = collatzSequenceLength(bigNum)
        assert colLength == realColLength
        
    print("Tests complete.")

def montecarlo(c, d, c3, l, start = 9 * 10 ** 99, end = 10 ** 100, number = 10 ** 10, file="record.txt"):
    f = open(file, 'a')
    f.write("\n\n")
    f.close()
    i = 1
    m, n = 0,0
    while i < number:
        #find random number
        b = random.randint(start, end)
        n = b
        #calculate collatz on that number
        length = collatzSequenceLength_shortened(n, 15, c, c3, d, l)

        #if it's larger, save and print it to file.z
        if length > m:
            m = length
            #print to a file.
            f = open(file, 'a')
            f.write(str(m) + " " + str(n) + "\n")
            f.close()
        i += 1

if __name__ == "__main__":
    cur_rate = 35000
    hours = 8
    time = hours * 60 * 60
    calculations = int(cur_rate * time)
    start = 9 * 10 ** 99
    end = 10 ** 100
    c = computeC(15)
    d = computeD(15)
    c3 = computeC3(c)
    l  = computeLengths(15)

    timedMonte = mutility.timeit(montecarlo)
    montecarlo(c, d, c3, l, start, end, calculations, "record.txt")

"""
Analysis:
   -@1@Initial
        ~1700 Large numbers / second
   -@2@removed function calls and implemented stuff inline.
        ~2631 Large numbers  / second
   -@3@Used some precomputed values to speed up collatz-length finding.
        ~15733 Large numbers / second
   -@4@Tweaked the number of precomputed values
        ~41407 Large numbers / second
    
Best Found:
    3853 9102319857259649962757829050604833689755764717261988082729087533238506652322401427394805774990600281
    3866 9277187926146854356453241592811309876752177728061970146319682799554121435098641596731860836738208074
    4171 9288771528353840854831983696275716493602004410732116499791458824135688644765364444141662371216825657
    4432 9312832634319510961624138895706272543015704696480077444378817181261679777116932197071977862740736731
"""