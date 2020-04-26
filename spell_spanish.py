"""Spelling Corrector in Python 3; see http://norvig.com/spell-correct.html

Copyright (c) 2007-2016 Peter Norvig
MIT license: www.opensource.org/licenses/mit-license.php
"""

################ Spelling Corrector 

import re #se importa el modulo de expresiones regulares para separar las palabras usadas para el entrenamiento
from collections import Counter #se importa el contador para hacer un vector con las frecuenciass de cada palabra

def words(text): return re.findall(r'\w+', text.lower())

# se leen los datos que se utilisan para el entrenamiento
#   ***tomados de***
# http://www.gutenberg.org/cache/epub/15532/pg15532.txt
# https://www.gutenberg.org/files/61594/61594-0.txt
# http://www.gutenberg.org/cache/epub/47287/pg47287.txt
# http://www.gutenberg.org/cache/epub/47631/pg47631.txt
# https://www.gutenberg.org/ebooks/48903
# http://www.gutenberg.org/cache/epub/2000/pg2000.txt
# https://en.wiktionary.org/wiki/Wiktionary:Frequency_lists
WORDS = Counter(words(open('E:/UNIVERSIDAD/UCEVA/2020-1/inteligencia/segundo_corte/25_abril/spell_train.txt').read()))

def P(word, N=sum(WORDS.values())): 
    "Probability of `word`."
    return WORDS[word] / N

def correction(word): 
    "Most probable spelling correction for word."
    return max(candidates(word), key=P)

def candidates(word): 
    "Generate possible spelling corrections for word."
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def known(words): 
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnñopqrstuvwxyzáéíóú' #pendiente el manejo de tildes
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word): 
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))

################ Test Code 
# Se hacen pruebas para verificar el correcto funcionamiento del algoritmo
def unit_tests():
    assert correction('coazon') == 'corazon'                    # insert
    assert correction('bliecos') == 'blancos'                   # replace 2
    assert correction('toce') == 'toca'                         # replace
    assert correction('dulnea') == 'dulcinea'                   # insert 2
    assert correction('universidadd') == 'universidad'          # delete
    assert correction('lirbo') =='libro'                        # transpose
    assert correction('escriiibere') =='escribiere'             # transpose + delete
    assert correction('plata') == 'plata'                       # known
    assert correction('quintessential') == 'quintessential'     # unknown
    assert words('Esto es una PRUEBA.') == ['esto', 'es', 'una', 'prueba']
    assert Counter(words('Esto es una prueba. 123; UNA PRUEBA esto es.')) == (
           Counter({'123': 1, 'una': 2, 'es': 2, 'prueba': 2, 'esto': 2}))
    assert len(WORDS) == 120294 #Se sabe que existen 120294 palabras diferentes
    assert sum(WORDS.values()) == 822387 #Se sabe que en total hay 822387 palabras
    assert WORDS.most_common(10) == [ #Se muestran las 10 palabras mas repetidas
    ('y', 30583), 
    ('de', 29236), 
    ('que', 27656), 
    ('la', 17643), 
    ('el', 14508), 
    ('en', 13072), 
    ('a', 11355), 
    ('no', 8722), 
    ('los', 7660), 
    ('se', 7535)]
    assert WORDS['y'] == 30583
    assert P('quintessential') == 0
    assert 0.03 < P('y') < 0.04
    return 'unit_tests pass'

def spelltest(tests, verbose=False):
    "Run correction(wrong) on all (right, wrong) pairs; report results."
    import time
    start = time.perf_counter()
    good, unknown = 0, 0
    n = len(tests)
    for right, wrong in tests:
        w = correction(wrong)
        good += (w == right)
        if w != right:
            unknown += (right not in WORDS)
            if verbose:
                print('correction({}) => {} ({}); expected {} ({})'
                      .format(wrong, w, WORDS[w], right, WORDS[right]))
    dt = time.perf_counter() - start
    print('{:.0%} of {} correct ({:.0%} unknown) at {:.0f} words per second '
          .format(good / n, n, unknown / n, n / dt))
    
def Testset(lines):
    "Parse 'right: wrong1 wrong2' lines into [('right', 'wrong1'), ('right', 'wrong2')] pairs."
    return [(right, wrong)
            for (right, wrongs) in (line.split(':') for line in lines)
            for wrong in wrongs.split()]

if __name__ == '__main__':
# Se realiza una prueba final para demostrar la efectividad del algoritmo, en este caso dada la pequeña cantidad de palabras tenemos una 
# Efectividad relativamente baja del 33%
    print(unit_tests())
    spelltest(Testset(open('E:/UNIVERSIDAD/UCEVA/2020-1/inteligencia/segundo_corte/25_abril/diccionario.txt')))
