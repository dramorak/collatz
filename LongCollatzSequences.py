import heapq
import random
from cmath import inf;
def beamSearch():
    #uses beam search algorithm to find numbers with long collatz sequences.

    WIDTH = 1000            #beam width
    MAX   = 10 ** 100   
    LIMIT   = 1000 * MAX    #consideration limit

    level = [-8]     #bfs level set (negative so I can use it as a max-heap with heapq)

    record, delay = 8, 3    #record best-found
    depth = 3       

    #want to keep going while level contains potential elements
    while level:
        #find the next level of the tree
        t = []
        minL=inf
        for i in range(len(level)):
            n = -level.pop()
            minL = min(minL, n)

            #if n goes above LIMIT, it probably isn't coming back down.
            if (n < LIMIT):
                heapq.heappush(t, -n * 2)
                if n % 6  == 4:
                    heapq.heappush(t, -((n - 1) // 3))
                
                #remove the largest elements
                while len(t) > WIDTH:
                    heapq.heappop(t)

        #store the best answer found so far, if it's valid.
        if (minL < MAX):
            delay = depth
            record = minL

        #t now contains the next level of the tree.
        depth += 1
        level = t

    return (record, delay)

#Guesses numbers randomly to find long collatz sequences.
def montecarlo(c, d, c3, l, start = 9 * 10 ** 99, end = 10 ** 100, number = 10 ** 10, file="record.txt"):
    f = open(file, 'a')
    f.write("\n\n")
    i = 1
    m = 0
    length = 0
    while i < number:
        #find random number
        b = random.randint(start, end)
        #calculate collatz on that number
        length = collatzSequenceLength_shortened(b, 15, c, c3, d, l)

        #if it's larger, save and
        #  print it to file.z
        if length > m:
            m = length
            #print to a file.
            f.write(str(m) + " " + str(b) + "\n")
        i += 1
    f.close()

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
    
def runMonteCarlo():
    cur_rate = 35000
    hours = 8
    total_time = hours * 60 * 60
    calculations = int(cur_rate * total_time)
    start = 9 * 10 ** 99
    end = 10 ** 100
    c = computeC(15)
    d = computeD(15)
    c3 = computeC3(c)
    l  = computeLengths(15)

    montecarlo(c,d,c3,l,start,end,100000, "record2.txt")

if __name__ == "__main__":
    print(beamSearch())

    print(runMonteCarlo())