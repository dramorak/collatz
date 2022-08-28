#python

def collatzStep(n):
    if n%2 == 1:
        return 3 * n + 1
    else:
        return n // 2

def collatzSequenceLength(n):
    result = 0
    last = 0
    while n != 1:
        result += 1
        last = n
        n = collatzStep(n)
    return result

print(collatzSequenceLength(10**(99)))

