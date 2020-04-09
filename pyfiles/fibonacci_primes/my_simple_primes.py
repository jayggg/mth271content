def prime_numbers(N):
    primes = []
    q = 1
    for n in range(q+1, N):
        if all(n % p > 0 for p in primes):
            primes.append(n)
            q = n
            yield n
