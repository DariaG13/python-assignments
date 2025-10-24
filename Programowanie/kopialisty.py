#### Importy ####
import math
import matplotlib.pyplot as plt
import numpy as np
from time import perf_counter
from itertools import repeat
import gc
from random import seed, randrange, setstate, getstate

#### Funkcje do mierzenia czasu – używane w całej liście, z wykładu ####

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

#### Zadanie 1 ####
# Zdefiniowanie funkcji minimum na bazie funkcji maksimum z wykładu
def minimum(lista):
    if lista:
        lista = iter(lista)
        kandydat = next(lista)
        for element in lista:
            if element < kandydat:
                kandydat = element
        return kandydat
    
# Pomiar dla losowej listy liczb #

# Zdefiniowanie funkcji generującej losową listę liczb
def losowa_lista_liczb(rozmiar=10):
    return list(np.random.randint(low = 0,high=2**10,size=rozmiar))

# Kod w komentarzu, ponieważ ładuje się zbyt długo #
#liczby1=[10**n for n in range(0,11)]
#czasy1=[zmierz(lambda: minimum(losowa_lista_liczb(n))) for n in liczby]

#plt.xscale('log')
#plt.scatter(liczby1, czasy1)
#plt.show()

# Zdefiniowanie funkcji generującej losową listę wyrazów #

def lista_losowych_słów(rozmiar=10, len=10):
    słowa=[]
    for x in range(rozmiar):
        znaki=list(np.random.randint(low = 33,high=128,size=len))
        słowo=""
        for y in znaki:
            słowo+=chr(y)
        słowa.append(słowo)
    return słowa

# 1-znakowe słowa #
#liczby2=[2**n for n in range(0,11)]
#czasy2=[zmierz(lambda: minimum(lista_losowych_słów(n, 1))) for n in liczby2]

#plt.xscale('log')
#plt.scatter(liczby2, czasy2)
#plt.show()

# 32-znakowe słowa #
#liczby3=[2**n for n in range(0,11)]
#czasy3=[zmierz(lambda: minimum(lista_losowych_słów(n, 32))) for n in liczby3]

#plt.xscale('log')
#plt.scatter(liczby3, czasy3)
#plt.show()

# 1024-znakowe słowa #
#liczby4=[2**n for n in range(0,11)]
#czasy4=[zmierz(lambda: minimum(lista_losowych_słów(n, 1024))) for n in liczby4]

#plt.xscale('log')
#plt.scatter(liczby4, czasy4)
#plt.show()

# Listy długości 1000 #
#liczby5=[2**n for n in range(0,11)]
#czasy5=[zmierz(lambda: minimum(lista_losowych_słów(1000, n))) for n in liczby5]

#plt.xscale('log')
#plt.scatter(liczby5, czasy5)
#plt.show()

#### Zadanie 2 ####

# Bisekcja – implementacja z wykładu #
def bisekcja(f, a, b, tolerancja=1e-6):
    c = (a+b)/2
    pół_długości = (b-a)/2
    if pół_długości <= tolerancja:
        return c
    f_a = f(a)
    while pół_długości > tolerancja:
        f_c = f(c)
        if f_a*f_c < 0:
            b = c
        elif f_a*f_c > 0:
            a = c
            f_a = f_c
        else:
            return c
        pół_długości /= 2
        c = (a+b)/2
    return c

def arctanminus1(x):
    return math.atan(x)-1

ns=list(range(1,101))
a=[0 for n in ns]
b=[10*n for n in ns]

#czasyb=[zmierz(lambda: bisekcja(arctanminus1, 0, n)) for n in ns]

#plt.plot(ns, czasyb)
#plt.show()

#### Zadanie 3 ####
przykladowatablica=np.array([[1,2,3,4,5,6,7,8],[9,10,11,12,13,14,15,16],[17,18,19,20,21,22,23,24]])

#listalist=[[1,2,3],[4,5,6],[7,8,9]]
#tablica2=np.array(listalist)
#print(tablica2)

def sąsiedztwo(A, r, i, j):
    wymiar=A.shape
    if not (0<=i<wymiar[0] and 0<=j<wymiar[1] and r>=0):
        return False
    i0=0
    i1=wymiar[0]
    j0=0
    j1=wymiar[1]

    if i-r>0:
        i0=i-r
    if j-r>0:
        j0=j-r
    if i+r<i1:
        i1=i+r+1
    if j+r<j1:
        j1=j+r+1

    wycinek=[]
    for x in range(i0,i1):
        lista=[]
        for y in range(j0,j1):
            lista.append(A[x,y])
        wycinek.append(lista)
    
    wycinekarray=np.array(wycinek)
    return wycinekarray

#print(przykladowatablica)
#print(sąsiedztwo(przykladowatablica,2,1,0))

tablica2=np.array([[1,2,3,4],[5,6,5,6],[2,2,3,4]])

def maksima_lokalne(A):
    maksima=[]
    for k in range(0,A.shape[0]):
        for l in range(0, A.shape[1]):
            obecnyelement=A[k][l]
            czymaksimum=True
            sąsiedztwoelementu=sąsiedztwo(A,1,k,l)
            for a in range(0,sąsiedztwoelementu.shape[0]):
                for b in range(0,sąsiedztwoelementu.shape[1]):
                    if sąsiedztwoelementu[a][b]>obecnyelement:
                        czymaksimum=False
                        break
            if czymaksimum:
                maksima.append((k,l))
    return maksima

def czy_jednomodalna(A):
    lista_maksimów=maksima_lokalne(A)
    if len(lista_maksimów)==1:
        return True
    else:
        return False
            
print(czy_jednomodalna(tablica2))
print(czy_jednomodalna(przykladowatablica))