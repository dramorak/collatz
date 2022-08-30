#python
import random
import mutility 

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

def montecarlo(start = 9 * 10 ** 100, end = 10 ** 101, number = 10 ** 10):
    f = open("record.txt", 'a')
    f.write("\n\n")
    i = 1
    m, n = 0,0
    while i < number:
        #find random number
        b = random.randint(start, end)

        #calculate collatz on that number
        l = collatzSequenceLength(b)

        #if it's larger, save and print it to file.z
        if l > m:
            m = l
            n = b
            #print to a file.
            f.write(str(l) + " " + str(n) + "\n")
        i += 1
    f.close()
    return (m, n)

if __name__ == "__main__":
    hours = 0.25
    time = hours * 60
    calculations = time * 100000
    start = 92782646348448348659949789458135845994515771618866311583339871771203327449182878552245381896867646813 - 10 ** 101 // 20
    end = 92782646348448348659949789458135845994515771618866311583339871771203327449182878552245381896867646813 + 10 ** 101 // 20
    number = 10 ** 10
    montecarlo(start, end, calculations)


"""
print("1:" + str(maxLength(1, 1)))
print("[2, 100]:" + str(maxLength(2, 100)))
print("[101, 1000]:", str(maxLength(101, 1000)))
print("[1001, 10000]:", str(maxLength(1001, 10000)))
print("[10001, 100000]:", str(maxLength(10001, 100000)))
print("[100001, 1000000]:", str(maxLength(100001, 1000000)))
"""

"""
Best found:
    monte carlo takes ~ 60 sec / 100000 guesses
    99999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999951424, 3355
    99999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999996006400, 3355
    95602131789319107091296635542174063925062101257853221583875519477916047156680830624785640341219268155, 3466
    99603972912947426165315603910845648565199480617374152896261243933028599712387704422426555441643561334, 3673
    92628389784614627027667072426533948577495426102244525637475797869379059593931277412021315936016493806, 3952 
    92782646348448348659949789458135845994515771618866311583339871771203327449182878552245381896867646813, 4438
"""
