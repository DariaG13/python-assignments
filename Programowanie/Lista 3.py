#### Importy ####
import math
import matplotlib.pyplot as plt
import numpy as np
from time import perf_counter
from itertools import repeat
import gc
from random import seed, randrange, setstate, getstate

#--- Zad 1 ---#
### Funkcje z wykładu prowadzące do sprawdzenia, czy liczba jest doskonała ###
def pierwsze_sito(N):
    if N < 2:
        return []
    kandydaci = list(range(N))
    kandydaci[0] = None
    kandydaci[1] = None
    for x in kandydaci:
        if x is None:
            continue
        if x*x >= N:
            break
        for y in range(x*x, N, x):
            kandydaci[y] = None
    return [x for x in kandydaci if x is not None]

def czynniki_pierwsze(n):
    wyniki = {}
    for p in pierwsze_sito(n+1):
        ile_razy = 0
        while n%p == 0:
            ile_razy += 1
            n //= p
        if ile_razy:
            wyniki[p] = ile_razy
    return wyniki

def wymnażaj(pary):
    if not pary:
        return [1]
    (n, k) = pary[0]
    bez_pierwszego = wymnażaj(pary[1:])
    wynik = []
    mnoznik = n
    for _ in range(k):
        wynik += [x*mnoznik for x in bez_pierwszego]
        mnoznik *= n
    return bez_pierwszego + wynik

def lista_dzielników(N, właściwe = True):
    czynniki = list(czynniki_pierwsze(N).items())
    dzielniki = sorted(wymnażaj(czynniki))
    if właściwe:
        return dzielniki[:-1]
    else:
        return dzielniki

def czy_doskonała(N):
    return N == sum(lista_dzielników(N))

### Funkcja na wypisanie liczb doskonałych mniejszych od N ###
def lista_doskonałych(N):
    doskonałe=[]
    for i in range(1,N):
        if czy_doskonała(i):
            doskonałe.append(i)
    return doskonałe

### Sprawdzenie funkcji dla N = 100 ###
#print(lista_doskonałych(100))

# Zad 2 #
### Funkcja sprawdzająca, czy liczba N i suma jej dzielników właściwych są liczbami zaprzyjaźnionymi ###
def czy_zaprzyjaźnione(N):
    if czy_doskonała(N):
        return None
    druga_liczba=sum(lista_dzielników(N))
    if N==sum(lista_dzielników(druga_liczba)):
        if N<=druga_liczba:
            return (N, druga_liczba)
        else:
            return (druga_liczba, N)
    else:
        return None
    
### Funkcja zwracająca liczbę par liczb zaprzyjaźnionych mniejszych od N ###
def ile_zaprzyjaźnionych(N):
    pary=set()
    for i in range(1,N):
        x=czy_zaprzyjaźnione(i)
        if x is not None and x[0]<N and x[1]<N:
            pary.add(x)
    return len(pary)

#print(ile_zaprzyjaźnionych(10000))
# Zad 3 #
### podpunkt 1, podstawowe sito
def sito_Sundarama(N):
    k=(N-2)//2
    kandydaci=list(range(1,k+1))
    liczby=[]
    if 2<N:
        liczby.append(2)
    for i in range(1, k+1):
        for j in range(1,k+1):
            suma=i+j+2*i*j
            if suma <=k:
                kandydaci[suma-1]=None
    for k in kandydaci:
        if k is not None:
            liczby.append(2*k+1)
    return liczby

### podpunkt 2, optymalizacja sita
#### Dodaję optymalizację 2, j<=(k-i)//(1+2*i) (z wyliczeń)

def sito_Sundarama2(N):
    k=(N-2)//2
    kandydaci=list(range(1,k+1))
    liczby=[]
    if 2<N:
        liczby.append(2)
    for i in range(1, k+1):
        for j in range(1,((k-i)//(1+2*i))+1):
            suma=i+j+2*i*j
            if suma <=k:
                kandydaci[suma-1]=None
    for k in kandydaci:
        if k is not None:
            liczby.append(2*k+1)
    return liczby

#print('Sito Eratostenesa: ' + str(pierwsze_sito(100)))
#print('Sito Sundarama: ' + str(sito_Sundarama(100)))
#print('Sito Sundarama (druga wersja): ' + str(sito_Sundarama2(100)))

### podpunkt 3, mierzenie czasu wykonania funkcji
#### Funkcje do mierzenia czasu – z wykładu ####

def zmierz_raz(f, min_time=0.2):
    czas = 0
    ile_razy = 0
    ile_teraz = 1
    stan_gc = gc.isenabled()
    gc.disable()
    while czas < min_time:
        if ile_teraz == 1:
            start = perf_counter()
            f()
            stop = perf_counter()
        else:
            iterator = repeat(None, ile_teraz)
            start = perf_counter()
            for _ in iterator:
                f()
            stop = perf_counter()
        czas = stop-start
        ile_teraz *= 2
    if stan_gc:
        gc.enable()
    return czas/ile_teraz

def zmierz_min(f, serie_min=5, min_time=0.2):
    pomiary = []
    generator = getstate()
    seed()
    my_seed = randrange(1000)
    for _ in repeat(None, serie_min):
        seed(my_seed)
        pomiary.append(zmierz_raz(f, min_time=min_time))
    setstate(generator)
    return min(pomiary)

def zmierz(f, serie_median=10, serie_min=5, min_time=0.2):
    pomiary = []
    for _ in repeat(None, serie_median):
        pomiary.append(zmierz_min(f, serie_min=serie_min, min_time=min_time))
    pomiary.sort()
    if serie_median%2==0:
        return (pomiary[serie_median//2-1]+pomiary[serie_median//2])/2
    else:
        return pomiary[serie_median//2]
    
liczby=[2**n for n in range(4,14)]
czasy1=[zmierz(lambda: pierwsze_sito(n)) for n in liczby]
czasy2=[zmierz(lambda: sito_Sundarama(n)) for n in liczby]
czasy3=[zmierz(lambda: sito_Sundarama2(n)) for n in liczby]

plt.xscale('log')
plt.scatter(liczby, czasy1, color='r')
plt.scatter(liczby, czasy2, color='g')
plt.scatter(liczby, czasy3, color='b')
plt.show()