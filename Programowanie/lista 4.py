# Importy #
from random import seed, randrange, setstate, getstate, shuffle, choice
from time import perf_counter
from itertools import repeat
import gc
import matplotlib.pyplot as plt

# Funkcje z wykładu #
### Pomiar czasu ###
def zmierz_raz_sortowanie(algorytm, lista, min_time=0.2):
    czas = 0
    ile_teraz = 1
    stan_gc = gc.isenabled()
    gc.disable()
    while czas < min_time:
        kopie_list = [lista.copy() for _ in repeat(None, ile_teraz)]
        if ile_teraz == 1:
            start = perf_counter()
            algorytm(kopie_list.pop())
            stop = perf_counter()
        else:
            iterator = repeat(None, ile_teraz)
            start = perf_counter()
            for _ in iterator:
                algorytm(kopie_list.pop())
            stop = perf_counter()
        czas = stop-start
        ile_teraz *= 2
    if stan_gc:
        gc.enable()
    return czas/ile_teraz
 
def zmierz_min_sortowanie(algorytm, lista, serie_min=5, min_time=0.2):
    pomiary = []
    generator = getstate()
    seed()
    my_seed = randrange(1000)
    for _ in repeat(None, serie_min):
        seed(my_seed)
        pomiary.append(zmierz_raz_sortowanie(algorytm, lista, min_time=min_time))
    setstate(generator)
    return min(pomiary)
 
def zmierz_sortowanie(algorytm, lista, serie_median=10, serie_min=5, min_time=0.2):
    pomiary = []
    lista = lista.copy()
    for _ in repeat(None, serie_median):
        shuffle(lista)
        pomiary.append(zmierz_min_sortowanie(algorytm, lista, serie_min=serie_min, min_time=min_time))
    pomiary.sort()
    if serie_median%2==0:
        return (pomiary[serie_median//2-1]+pomiary[serie_median//2])/2
    else:
        return pomiary[serie_median//2]


### Funkcje na sortowanie – do wykorzystania w podpunkcie 2 listy 1 oraz w pomiarach z zadania 2 ###
def sortowanie_bąbelkowe(lista, relacja=lambda x, y: x <= y):
    n = len(lista)
    dalej = True
    i = 0
    while dalej:
        dalej = False
        for j in range(n-1-i):
            if not relacja(lista[j],lista[j+1]):
                lista[j], lista[j+1] = lista[j+1], lista[j]
                dalej = True
        i += 1
 
def sortowanie_wstawianie(lista, relacja=lambda x, y: x <= y):
    for i in range(1, len(lista)):
        li = lista[i]
        j = i
        while j>0 and not relacja(lista[j-1], li):
            lista[j] = lista[j-1]
            j -= 1
        lista[j] = li
 
def sortowanie_wybieranie(lista, relacja=lambda x, y: x <= y):
    n = len(lista)
    for i in range(n-1):
        j = i
        for k in range(i+1, n):
            if not relacja(lista[j], lista[k]):
                j = k
        if j != i:
            lista[i], lista[j] = lista[j], lista[i]
 
def sortowanie_scalanie(lista, relacja=lambda x, y: x <= y):
    def scal(lista1, lista2):
        wynik = []
        n1 = len(lista1)
        n2 = len(lista2)
        i1 = 0
        i2 = 0
        while i1 < n1 and i2 < n2:
            if relacja(lista1[i1], lista2[i2]):
                wynik.append(lista1[i1])
                i1 += 1
            else:
                wynik.append(lista2[i2])
                i2 += 1
        return wynik + lista1[i1:] + lista2[i2:]
    n = len(lista)
    if n <= 1:
        return lista.copy()
    k = n//2
    l1, l2 = lista[:k], lista[k:]
    l1 = sortowanie_scalanie(l1)
    l2 = sortowanie_scalanie(l2)
    return scal(l1, l2)

# Zad 1 #
### Podpunkt 1 ###
L = [1,5,2,-1]

def inwersje(lista, relacja=lambda x, y: x <= y):
    lista_inwersji=[]
    długość=len(lista)
    for i in range(długość):
        for j in range(i+1,długość):
            if relacja(lista[j],lista[i]):
                lista_inwersji.append((lista[i],lista[j]))
    return lista_inwersji

#print(inwersje(L))

### Podpunkt 2 ###
#### Traktuję elementy jako różne, bez klas równoważności, wykorzystuję sortowanie przez scalanie, ponieważ zwraca kopię listy i nie modyfikuje listy pierwotnej ####
def rangi(lista, relacja=lambda x, y: x <= y):
    długość=len(lista)
    posortowana_lista=sortowanie_scalanie(lista)
    indeksy=[0]*długość
    for i in range(długość):
        indeksy[i]=posortowana_lista.index(lista[i])
    return indeksy

#print(rangi(L))

# Zad 2 #
### Podpunkt 1  nie wiem, może potem ogarnę XD ###
### Podpunkt 2 ###
lista_zliczanie=[9,7,7,1,1,7,8]
klucze_zliczanie=range(1,10)

def sortowanie_zliczanie(lista, klucze):
    ### Zmienne pomocnicze
    długość=len(lista) # Długość listy, żeby nie musieć jej potem ściągać
    ### Słowniki i właściwa lista
    wystąpienia={}
    pozycje={}
    posortowana=[0]*długość

    ### Zliczenie wystąpień
    for klucz in klucze:
        wystąpienia[klucz]=0 # Inicjalizacja słownika i wypełnienie go zerami, by oszczędzić czasu na sprawdzanie potem, czy dany klucz istnieje
    for l in lista:
        wystąpienia[l]+=1 # Zliczanie wystąpień właściwe

    # Wyczyszczenie wystąpień z zer, dla przejrzystości
    wystąpienia={klucz:wartość for klucz, wartość in wystąpienia.items() if wartość!=0}

    ### Zapisanie odpowiednich pozycji
    suma_wystąpień=0

    for w in wystąpienia.items():
        pozycje[w[0]]=suma_wystąpień
        suma_wystąpień+=w[1]

    ### Iteracja przez elementy listy

    for l in lista:
        posortowana[pozycje[l]]=l
        pozycje[l]+=1
        
    return posortowana

#print(sortowanie_zliczanie(lista_zliczanie,klucze_zliczanie))

### Podpunkt 3 ###
# Generacja losowej listy liczb z zakresu od 0 do 9
zakres=list(range(10))
lista_tysiąca=[choice(zakres) for n in range(1000)]

# Żeby dobrze wyglądało, to zrobię to w formie wykresu, a poszczególne funkcje odpowiednio ponumeruję
#numery=list(range(1,7))
#wyniki=[0]*6

#numery2=list(range(1,4))
#wyniki2=[0]*3

# 1: Sortowanie przez zliczanie
#wyniki2[0]=zmierz_sortowanie(lambda lista: sortowanie_zliczanie(lista, range(10)), lista_tysiąca)
# 2: Sortowanie metodą sort()
#wyniki2[1]=zmierz_sortowanie(lambda lista: lista.sort(), lista_tysiąca)
# 3: Sortowanie bąbelkowe
#wyniki[2]=zmierz_sortowanie(lambda lista: sortowanie_bąbelkowe(lista), lista_tysiąca)
# 4: Sortowanie przez wstawianie
#wyniki[3]=zmierz_sortowanie(lambda lista: sortowanie_wstawianie(lista), lista_tysiąca)
# 5: Sortowanie przez wybieranie
#wyniki[4]=zmierz_sortowanie(lambda lista: sortowanie_wybieranie(lista), lista_tysiąca)
# 6: Sortowanie przez scalanie
#wyniki2[2]=zmierz_sortowanie(lambda lista: sortowanie_scalanie(lista), lista_tysiąca)

#wyniki 2 to: wyniki[0], wyniki[1] i wyniki[5]

#plt.scatter(numery2, wyniki2)
#plt.show()

#print(lista_tysiąca)
#print(zmierz_sortowanie(lambda lista: lista.sort(), lista_tysiąca))

# Zad 3 #
def cyfra_znacząca(liczba, numer_cyfry):
    return (liczba//(10**(numer_cyfry-1)))%10

testowa_lista=[526,4,2456,13,736,168]

# nie wiem, co z tego będzie, ale trudno
def sortowanie_zliczanie_zmodyfikowane(lista, c, klucze=range(10)):
    ### Zmienne pomocnicze
    długość=len(lista) # Długość listy, żeby nie musieć jej potem ściągać
    czy_same_zera=True

    ### Słowniki i właściwa lista
    wystąpienia={}
    pozycje={}
    posortowana=[0]*długość

    ### Zliczenie wystąpień
    for klucz in klucze:
        wystąpienia[klucz]=0 # Inicjalizacja słownika i wypełnienie go zerami, by oszczędzić czasu na sprawdzanie potem, czy dany klucz istnieje
    for l in lista:
        cyfra=cyfra_znacząca(l,c)
        wystąpienia[cyfra]+=1 # Zliczanie wystąpień właściwe
        if cyfra != 0:
            czy_same_zera=False
    
    if czy_same_zera:
        return None

    # Wyczyszczenie wystąpień z zer, dla przejrzystości
    wystąpienia={klucz:wartość for klucz, wartość in wystąpienia.items() if wartość!=0}

    ### Zapisanie odpowiednich pozycji
    suma_wystąpień=0

    for w in wystąpienia.items():
        pozycje[w[0]]=suma_wystąpień
        suma_wystąpień+=w[1]

    ### Iteracja przez elementy listy

    for l in lista:
        cyfra=cyfra_znacząca(l,c)
        posortowana[pozycje[cyfra]]=l
        pozycje[cyfra]+=1
        
    return posortowana

def sortowanie_pozycyjne(lista):
    pozycyjnie_posortowana=lista

    czy_ma_się_sortować=True
    i_do_sortu=1
    while czy_ma_się_sortować:
        nowa_lista=sortowanie_zliczanie_zmodyfikowane(pozycyjnie_posortowana,i_do_sortu)
        if nowa_lista is not None:
            pozycyjnie_posortowana=nowa_lista
            i_do_sortu=i_do_sortu+1
        else:
            czy_ma_się_sortować=False
    return pozycyjnie_posortowana

print(sortowanie_pozycyjne(testowa_lista))

'''zakres2=list(range(10000))
lista_tysiąca2=[choice(zakres2) for n in range(1000)]
print(lista_tysiąca2)
print(sortowanie_pozycyjne(lista_tysiąca2))'''