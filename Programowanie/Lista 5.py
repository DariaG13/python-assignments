# Importy #
from random import choice
from itertools import combinations

# Zad 1 #
### Podpunkt 1 ###
def koduj(napis, klucz=1):
    zakodowany=''
    indeksA=ord('A')
    indeksZ=ord('Z')
    for c in napis:
        indeks=ord(c)
        nowyindeks=indeks+klucz
        if nowyindeks>indeksZ:
            nowyindeks=nowyindeks-indeksZ+indeksA-1
        elif nowyindeks<indeksA:
            nowyindeks=nowyindeks+indeksZ-indeksA+1
        zakodowany+=chr(nowyindeks)
    return zakodowany

print(koduj('ALAMAKOTAZZZ', 5))

### Podpunkt 2 ###
def dekoduj(napis, klucz=1):
    return(koduj(napis, -1*klucz))

print(dekoduj('FQFRFPTYFEEE', 5))

### Podpunkt 3 ###
# Słownik przechowujący częstotliwości dla języka polskiego
freq = {
  'A': 0.099,  'B': 0.0147, 'C': 0.0436, 'D': 0.0325, 'E': 0.0877, 'F': 0.003,  'G': 0.0142,
  'H': 0.0108, 'I': 0.0821, 'J': 0.0228, 'K': 0.0351, 'L': 0.0392, 'M': 0.028,  'N': 0.0572,
  'O': 0.086,  'P': 0.0313, 'Q': 0.0014, 'R': 0.0469, 'S': 0.0498, 'T': 0.0398, 'U': 0.025,
  'V': 0.004,  'W': 0.0465, 'X': 0.0002, 'Y': 0.0376, 'Z': 0.0653
}

# Funkcja z listy na porównywanie podobieństwa
def porównaj(freq1, freq2):
    delta = 0
    for litera, częstość in freq1.items():
        if litera not in freq2:
            delta += częstość
        else:
            delta += abs(częstość - freq2[litera])
    for litera, częstość in freq2.items():
        if litera not in freq1:
            delta += częstość
    return delta

# Zakodowana wiadomość z listy
wiadomość1 = """CNJRYVTNJRYJWRQALZFGNYVQBZHCNJRYANTBEMRNTNJRYANQBYRCNJRYFCBXBWALAVRJNQMVYAVXBZHTNJRYANWQMVXFMRJLZLFYNYFJNJBYRPVNTYRCBYBJNYCBFJBVZCBXBWHGBCVRFGBMNWNPZVRQMLFGBYLFGBYXVTBAVYHPVRXNYJLJENPNYXBMVBYXVFGEMRYNYVGENOVYVXEMLPMNYQBMABWH"""

# Funkcja na wyznaczenie częstotliwości występowania liter – żeby było czytelniej
def częstotliwość(napis):
    długość=len(napis)
    występowanie={}
    częstotliwość={}
    for n in napis:
        if n in występowanie:
            występowanie[n]+=1
        else:
            występowanie[n]=1

    for litera, wystąpienia in występowanie.items():
        częstotliwość[litera]=(((wystąpienia/długość)*10000)//1)/10000
    return częstotliwość

wiadomości={}

for k in range(26):
    wiadomości[k]=dekoduj(wiadomość1, k)

delty=[]

for k, w in wiadomości.items():
    delty.append((porównaj(freq, częstotliwość(w)), k, w))

delty.sort()

print('Odkodowaną wiadomością jest: "' + delty[0][2] +'", dla klucza ' + str(delty[0][1]))

# Zad 2 #
### popdunkt A ###
def levenshtein(napis1, napis2):
    długość1=len(napis1)
    długość2=len(napis2)
    wymiary1=długość2+2 # ilość wierszy
    wymiary2=długość1+2 # ilość kolumn
    tablica=[[0]*wymiary2 for n in range(wymiary1)]
    # Pierwszy indeks to indeks wiersza, drugi kolumny (czyli napierw od góry do dołu, a potem od lewej do prawej)

    for i in range(2, wymiary2):
        tablica[0][i]=napis1[:(i-1)]
        tablica[1][i]=i-1
    for j in range(2, wymiary1):
        tablica[j][0]=napis2[:(j-1)]
        tablica[j][1]=j-1

    for k in range(2,wymiary1):
        for l in range(2,wymiary2):
            if tablica[0][l][-1] == tablica[k][0][-1]:
                tablica[k][l]=tablica[k-1][l-1]
            else:
                wartości=[0,0,0]
                wartości[0]=tablica[k][l-1]+1
                wartości[1]=tablica[k-1][l]+1
                wartości[2]=tablica[k-1][l-1]+2
                tablica[k][l]=min(wartości)
    return tablica[wymiary1-1][wymiary2-1]

print(levenshtein('Ala','Olek'))

### podpunkt 2 ###
#### Funkcje pomocnicze ####
# funkcja generująca losowy napis
def losowynapis(długość):
    napis=''
    zakres=list(range(ord('A'), ord('Z')+1))
    for _ in range(długość):
        napis+=chr(choice(zakres))
    return napis

'''napisala='ALAMAKOTA'
listanapisów=[losowynapis(9) for n in range(100)]

print(listanapisów)'''

def guess(napis, lista):
    odległości=[(levenshtein(napis, n), n) for n in lista]
    odległości.sort()
    najmniejszaodległość=odległości[0][0]
    napisy=[n[1] for n in odległości if n[0]==najmniejszaodległość]
    return napisy

#print(guess(napisala, listanapisów))

# Zad 3 #
### Zmienne zadane ###
słownik = {'kalafior', 'rower', 'krowa', 'pieczarka', 'prezydent', 'usa', 'pi', 'sigma', 'python', 'naleśniki'}
wiadomość = "uslppiapniepyrtswczehazdoyrkcnadvientjqlkjeogijpzxczx"

def dekodowanie_słów(słownik, wiadomość):
    kopia_słownika=słownik.copy()
    kopia_wiadomości=''

### Optymalizacja wiadomości i słownika

    for s in słownik:
        for x in s:
            if x not in wiadomość:
                kopia_słownika.remove(s)

    litery_w_słowniku=[]

    for s in kopia_słownika:
        for x in s:
            litery_w_słowniku.append(x)

    litery_w_słowniku=set(litery_w_słowniku)

    for w in wiadomość:
        if w in litery_w_słowniku:
            kopia_wiadomości+=w

### Zapisanie szczegółowe wszystkich możliwych przypadków dla każdego słowa
    długość_wiadomości=len(kopia_wiadomości)
    możliwe_indeksy={}

    for s in kopia_słownika:
        indeksy_właściwe=[]
        indeksy_ostateczne=[]
        wiadomość_do_operowania=''
        indeksy_0_1=''
        for w in kopia_wiadomości:
            if w in s:
                wiadomość_do_operowania+=w
                indeksy_0_1+='1'
            else:
                indeksy_0_1+='0'
        kombinacje_indeksów=list(combinations(list(range(len(wiadomość_do_operowania))), len(s)))
        #print(s + '; ' + wiadomość_do_operowania + '; ' + indeksy_0_1) # do usunięcia po ostatecznym końcu testowania

        for k in kombinacje_indeksów:
            słowo_lista=[wiadomość_do_operowania[n] for n in k]

            słowo=''.join(słowo_lista)
            if słowo==s:
                indeksy_właściwe.append(k)
        #print(indeksy_właściwe) # do usunięcia po ostatecznym końcu testowania

        if len(indeksy_właściwe)>0:
            for i in indeksy_właściwe:
                numer=0
                indeks_ostateczny=[]
                for j in range(len(indeksy_0_1)):
                    if indeksy_0_1[j]=='1':
                        if numer in i:
                            indeks_ostateczny.append(j)
                        numer+=1
                indeksy_ostateczne.append(tuple(indeks_ostateczny))
            #print(indeksy_ostateczne) # do usunięcia po ostatecznym końcu testowania
            możliwe_indeksy[s]=indeksy_ostateczne
        else:
            możliwe_indeksy[s]=None

    for x in możliwe_indeksy.items():
        if x[1] is not None:
            print(x[0]+ ': ' + str(x[1]) + ';') # do usunięcia po ostatecznym końcu testowania
    return 'siema' # zmiana returna na coś sensownego

### Test funkcji dla marchewki i autobusu XD
słownik2={'marchewka','autobus'}
wiadomość2='amaurtcheobwuksa'

#print(dekodowanie_słów(słownik2, wiadomość2))

słownik3 = {'abba', 'huba', 'halo'}
wiadomość3 = "hubabbhaloaa"

#print(dekodowanie_słów(słownik3, wiadomość3))

print(dekodowanie_słów(słownik, wiadomość))