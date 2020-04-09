from fibonacci import fibonacci, fibonacci_primes


def test_fibonacci_prime():
    N = 10000
    F = list(fibonacci(N))
    nFP = [3, 4, 5, 7, 11, 13, 17, 23, 29, 43]
    
    our_list = fibonacci_primes(N)
    known_list = set([F[n] for n in nFP if n < len(F)])
    
    assert len(known_list.difference(our_list))==0, 'We have a bug!'
    print('Passed test!')
