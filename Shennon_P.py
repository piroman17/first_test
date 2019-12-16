# -*- coding: utf-8 -*-
"""
Реализация кода Шеннона

(набор символов с вероятностями появления в генерируемом тексте)
"""

from math import  fabs, isfinite, modf, log2
import numpy as np
from matplotlib import pyplot  as plt

#функция перевода дробной части в 2
def float_to_bin_fixed(f):
    if not isfinite(f): #проверка на бесконечьность или NaN
        return repr(f)  # inf nan
    
    frac, fint = modf(fabs(f))  # деление на дробную и целую части
    n, d = frac.as_integer_ratio()  # возвращает числа, дающие эту дробь при делении
    assert d & (d - 1) == 0  # power of two
    return f'{n:0{d.bit_length()-1}b}'

#Генерация строки из заданных символов с вероятностями
def text_gen(N, sym, P):
    ascii_sym = [ord(i) for i in sym] #номер символа в ascii
    out_str = ''    
    for i in range(N):        
        out_str += chr(np.random.choice(ascii_sym, p=P))        
    return(out_str)
    
#генерация вероятностей
def rand_p(N):
    a = np.random.random(N)
    a /= a.sum()

    return (list(a))

#генерация вероятностей, где один из символов имеет вероятность 0.5
def rand_p2(N):
    a = np.random.random(N-1)
    a = np.append(a, a.sum())
    a /= a.sum()

    return (list(a))


def shennon(sym, p, data):
    d = {sym[i]:p[i]  for i in range(len(sym))}

    #сортировка по невозрастанию
    P = sorted(d.items(), key=lambda x: x[1],  reverse=True)


    print('\nСимволы и их вероятности, отсортированные по убыванию вероятности:')
    for symbol, key in P:
        print(symbol, key, sep=': ')
    
    entr =0 
    for i in range(len(P)):
        entr += P[i][1]*log2(1/P[i][1])

    #print('\nЭнтропия ансамбля:', entr)

    b = [0]
    c = [0]
    for i in range(0,len(P)-1):
    
        #список, содержащий комулятивные суммы вероятностей
        b.append(float(P[i][1]+ b[i]))
    #print(b)

    #дробные части вероятностей переведенные в двоичную систему
    c = [float_to_bin_fixed(b[i]) for i in range(len(P))]
    #print(c)


    X, codes=[], []

    for i in range(len(P)):
        x = 0
        while P[i][1] <= 2**-x:
            x += 1
        #длины слов
        X.append(x)
    
        while len(c[i]) < x:
            c[i] += '0'    
        #коды    
        codes.append(c[i][:x])
    

    #print('Длины кодовых слов: ')
    #print(X)

    codes_dict = {P[i][0]:codes[i]  for i in range(0, len(P), 1)}
    print('\nСимволы и соответствущие им коды: ')
    for symbol, key in sorted(codes_dict.items(), key=lambda item: len(item[1])):
        print(symbol, key, sep=': ')
    #коды, соответствующие символам сообщения
    encoded = [codes_dict[letter] for letter in data]
    
    #строка кодов
    encoded_bits = ''.join(encoded)
    #преобразование кодовых слов в строку
    encoded_str = [chr(int(encoded_bits[i:i + 8], 2)) for i in range(0, len(encoded_bits), 8)]


    print('\nИсходный текст ({} bits): '.format(len(data) * 8), data)
    #print('\nСжатый текст ({} bits): \n'.format(len(encoded_str) * 8), ''.join(encoded_str))
    print('Данные ({} bits): {}'.format(len(encoded_str) * 8, encoded_bits))
    
    print('\nКоэффициент сжатия данных:', len(data)/len(encoded_str))
    
    return [len(data) * 8,len(encoded_str) * 8,len(data)/len(encoded_str)]


    

#symbols = ['A','B','C','D','E','F','G','H','I',' ']
symbols = [chr(i) for i in range(65,91,1)]
symbols.append(' ')
#P1 = [0.3, 0.05, 0.05, 0.15, 0.05, 0.03, 0.07,0.08, 0.02, 0.2]
P2 = [1/len(symbols) for i in range(len(symbols))]
P1 = rand_p(len(symbols))
P3 = rand_p2(len(symbols))
#Количество символов в генерируемой строке
N = int(input('Введите количество символов в строке: '))


print('\n1) Вероятности появления символов не равны')
data = text_gen(N,symbols, P1)  #генерация строки
print('\nСгенерированная строка:')
print(data)
rez1 = shennon(symbols,P1,data)

print('\n2) Вероятность появления одного из символов равна 0.5')
data = text_gen(N,symbols, P3)  #генерация строки
print('\nСгенерированная строка:')
print(data)
rez3 = shennon(symbols,P3,data)

print('\n\n3) Вероятности появления символов равны')

data = text_gen(N,symbols, P2)  #генерация строки
print('\nСгенерированная строка:')
print(data)
rez2 = shennon(symbols,P2,data)








