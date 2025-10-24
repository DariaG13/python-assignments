# Importy #
import numpy as np
import math
import matplotlib.pyplot as plt
from time import perf_counter
from itertools import repeat
import gc

# Funkcja zmierz_raz z wykłądu #
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

# Zad 1 #
### xgcd - funkcja z wykładu ###
def xgcd(a, b):
    if b==0:
        return (a, 1, 0)
    else:
        (gcd, x_prim, y_prim) = xgcd(b, a%b)
        return (gcd, y_prim, x_prim-a//b*y_prim)

# Diofantyczne ma rozwiązanie
def diofantyczne_ma_rozwiązanie(a, b, c):
    trojka=xgcd(a,b)
    if c%trojka[0]==0:
        return True
    else:
        return False

# print(diofantyczne_ma_rozwiązanie(18, 16, 500) is True)

# Przykładowe rozwiązanie diofantyczne
def diofantyczne_rozwiązanie(a, b, c):
    trojka=xgcd(a,b)
    if c%trojka[0]==0:
        czynnik=c//trojka[0]
        return (trojka[1]*czynnik, trojka[2]*czynnik)
    else:
        return None

# (x, y) = diofantyczne_rozwiązanie(18, 16, 500)
# print(18*x + 16*y == 500)

# Nieujemne rozwiązania diofantyczne
def diofantyczne_nieujemne(a, b, c):
    rozwiązania=set()
    if diofantyczne_ma_rozwiązanie(a,b,c):
        para=diofantyczne_rozwiązanie(a, b, c)
        dzielnik=xgcd(a,b)[0]

        if ((-1)*para[0]*dzielnik)/b<=(para[1]*dzielnik)/a:
            k1=((-1)*para[0]*dzielnik)/b
            k2=(para[1]*dzielnik)/a
        else:
            k1=(para[1]*dzielnik)/a
            k2=((-1)*para[0]*dzielnik)/b

        if not k1//1==k1:
            k1=int((k1//1)+1)

        k2=int((k2//1)+1)

        for k in range(k1,k2):
            xk=int(para[0]+(b/dzielnik)*k)
            yk=int(para[1]-(a/dzielnik)*k)
            rozwiązania.add((xk,yk))

    return rozwiązania

# print(diofantyczne_nieujemne(18, 16, 500) == {(26, 2), (18, 11), (10, 20), (2, 29)})

# Zadanie ze skoczkiem
### Zmienne
krótki_skok=84
długi_skok=228
dom=430
kolega=432

### Funkcja na minimum
# Wiem, że ta funkcja nie obsługuje sensownie rozwiązań nieujemnych, jednak nie implementowałam tego, bo tu takowych nie ma

def minimalna_suma(a,b,c):
    (x,y)=diofantyczne_rozwiązanie(a,b,c)
    d=xgcd(a,b)[0]
    szacowane_k=(-1*x*d)/b

    k_przedział=(szacowane_k//1, (szacowane_k//1)+1)

    (x1,y1)=(int(x+(b//d)*k_przedział[0]),int(y-(a//d)*k_przedział[0]))
    (x2,y2)=(int(x+(b//d)*k_przedział[1]),int(y-(a//d)*k_przedział[1]))

    return min(abs(x1)+abs(y1),abs(x2)+abs(y2))

if diofantyczne_ma_rozwiązanie(krótki_skok, długi_skok,dom):
    print('Alfred będzie nocować w domu. Wykona minimalnie '+str(minimalna_suma(krótki_skok, długi_skok,dom))+' skoków.')
elif diofantyczne_ma_rozwiązanie(krótki_skok, długi_skok,kolega):
    print('Alfred będzie nocować u Horacego. Wykona minimalnie '+str(minimalna_suma(krótki_skok, długi_skok,kolega))+' skoków.')
else:
    print('Alfred nie będzie nocować pod dachem.')

# Zad 2 #
# Wersja rekurencyjna funkcji
    
def Newton_rekurencja(n, k):
    if k==0 or k==n:
        return 1
    else:
        return Newton_rekurencja(n-1, k-1)+Newton_rekurencja(n-1, k)
    
# print(Newton_rekurencja(21,14))

def Newton_iteracja(n=1,k=1):
    trójkąt=np.zeros((n+1,n+1))
    trójkąt[0][0]=1
    for i in range (1,n+1):
        for j in range(i+1):
            if j==0:
                trójkąt[i][j]=1
            else:
                trójkąt[i][j]=trójkąt[i-1][j-1]+trójkąt[i-1][j]
    return int(trójkąt[n][k])

# print(Newton_iteracja(21,14))

def Newton_silnia(n,k):
    return (math.factorial(n))//(math.factorial(k)*math.factorial(n-k))

# print(Newton_silnia(21,14))

### Kod na wykres w komentarzu ze względu na czas ładowania - wykres w załączniku #

#liczby=[(n,k) for n in range (10,20,2) for k in range (1,11,2)]
#liczby_strings=[str(i) for i in liczby]

#czasy1=[zmierz_raz(lambda: Newton_rekurencja(n[0],n[1])) for n in liczby]
#czasy2=[zmierz_raz(lambda: Newton_iteracja(n[0],n[1])) for n in liczby]
#czasy3=[zmierz_raz(lambda: Newton_silnia(n[0],n[1])) for n in liczby]

#plt.scatter(liczby_strings, czasy1, color='r')
#plt.scatter(liczby_strings, czasy2, color='m')
#plt.scatter(liczby_strings, czasy3, color='b')
#plt.show()
# Zad 3 #
### Wzór na implementację ciągu znalazłam w sieci, jednak, niestety, nie znam jego wytłumaczenia
def liczba_działek(k):
    zbiór=[(x,y) for x in range (1,k+1) for y in range (x, k+1) if xgcd(x,y)[0]==1]
    return len(zbiór)