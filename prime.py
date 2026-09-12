primes = []

def is_prime(num):
    if num < 2: #checks if a number is prime
        return False

    for i in range(2, num):
        if num % i == 0:
            return False

    return True

for num in range (2, 10000): #range of prime numbers
    if is_prime(num):
        primes.append(num)

#print(primes) #the list of primes

