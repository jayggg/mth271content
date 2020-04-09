from my_simple_primes import prime_numbers

def fibonacci(max):
    f, fnext = 0, 1
    while f < max: 
        yield f
        f, fnext = fnext, f + fnext


def fibonacci_primes(N):
    F = set(fibonacci(N))
    P = set(prime_numbers(N))
    print('Intersecting', len(P), 'primes with', len(F), 'fibonaccis.')
    return P.intersection(F)
