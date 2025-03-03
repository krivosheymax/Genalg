'''
Генетический алгоритм

__________________________________________________________________________

Дана некоторая функция f(x1, x2, x3, x4, x5).
Программа находит такие целые положительные значения переменных x1, x2, x3, x4, x5, при которых значение f(x1, x2, x3, x4, x5) равняется или близко к 50.
'''
from random import randint, seed
from copy import deepcopy as dcp, copy as cp
def o_vel(l): #Расчёт показателя отклонения от 50 для каждого набора переменных
    q = 0
    t = []
    for i in l:
        o = abs(f(*i)-50)
        q +=(1 / o) if o!=0 else 0
    for i in l:
        o = abs(f(*i)-50)
        t.append([o, ((1 / o) if o!=0 else 0)/q])
    return t
def otkl_50(l): #Расчёт среднего отклонения от 50 имеющихся наборов
    n = 0
    s = 0
    for i in l:
        n+=1
        s+=abs(f(*i)-50)
    return s/n
def f(a,b,c,d,e,w):
    return 2*a+5*b+2*c+3*d-4*e-6*w+2*a*b-3*c*d+e*d-w*e+a*w*c-e*c*d+e**2*a*b-c**2*d*w+w**2*c**2 #По легенде, программа не знает, какая формула скрыта под функцией. Данная формула взята для примера, на её место может быть поставлена любая другая. Главное, чтобы решение уравнеиеи имело, хотя бы приближённое :)
def mut(): # Реализация мутации - случайного изменения некоторых переменных в наборе
    global l
    n = len(l)
    q = [[] for i in range(n)]
    for i in range(n):
        for j in range(6):
            y = randint(1, 10)
            if y==5:
                q[i].append(randint(1, 50))
            else:
                q[i].append(cp(l[i][j]))
    l = dcp(q)
def top5(l): #Индексы пяти лучших наборов
    ou = []
    for i in range(5):
        m = float('-inf')
        for j in l:
            m = max(m, j[1])
        k = 0
        for j in l:
            if j[1]==m:
                ou.append(k)
                l[k][1]=float('-inf')
                break
            k+=1
    return ou
def comb(): #Реализация скрещивания. Механизм отбора 5 лучших из образовавшихся в результате скрещивания 10 наборов переменных позволяет в процессе эволюции накапливать положительные и отсеивать отрицательные мутуции
    global l, t
    u = dcp(l)
    ll = []
    qw = []
    w = []
    e = top5(dcp(t))
    for i in e:
        w.append(cp(u[i]))
    for i in range(5):
        for j in range(i+1, 5):
            x, y = cp(w[i]), cp(w[j])
            for h in range(6):
                q = randint(0,1)
                if q:
                    x[j], y[h] = y[h], x[h]
            q = randint(0, 1)
            if q:
                qw.append(x)
            else:
                qw.append(y)
    q = 0
    tt = []
    for i in qw:
        o = abs(f(*i) - 50)
        q += (1 / o) if o!=0 else 0
    for i in qw:
        o = abs(f(*i) - 50)
        tt.append([o, ((1 / o) if o!=0 else 0) / q])
    e = top5(dcp(tt))
    for i in e:
        ll.append(cp(qw[i]))
    return ll
l = [[randint(1, 50) for i in range(6)] for j in range(5)] #Стартовый набор
t = []
so = otkl_50(l)
t = dcp(o_vel(l))
for i in range(5000): #5000 ступеней эволюции
    ee = so
    aa = comb()
    ew = otkl_50(aa)
    if ee-ew<0: #Если данный вариант скрещивания не даёт положительного эффекта, не принимаем его, как новую модель
        continue
    l = dcp(aa)
    so = ew
    t = dcp(o_vel(dcp(l)))
    if so>4 and (ee-so)/ee<0.21: #В случае, если модель "забуксовала", и скрещивания не приводят к её улучшению, запускаем мутации.
        mut()
        seed(randint(0, 3000))
        so = otkl_50(l)
l = set([tuple(i) for i in l])
n, o = 0, 0
for i in l:
    n+=1
    qw = abs(f(*i)-50)
    o+=qw
    print('''Набор переменных: {}; Результат: {};
Отклонение:{}'''.format(', '.join(map(str, i)), f(*i), qw))
print("Среднее отклонение:", o/n, "Процент отклонения от идеального результата:",o/n*2)