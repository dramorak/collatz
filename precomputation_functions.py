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

if __name__ == "__main__":
    c = computeC(20)
    d = computeD(20)
    c3 = computeC3(c)
    l  = computeLengths(20)
    
    f = open("cache.txt", 'a')
    f.write("C:\n" + str(c) + "\n\n")
    f.write("D:\n" + str(d) + "\n\n")
    f.write("C3:\n" + str(c3) + "\n\n")
    f.write("L:\n" + str(l) + "\n\n")