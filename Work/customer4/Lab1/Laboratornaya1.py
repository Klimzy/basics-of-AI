import math
import random
import graycode
import matplotlib.pyplot as plt
import numpy as np


Q = 30          # Кол-во поколений
MAX_ENT = 100    # размер популяции
MAX_CH = 30     # кол-во детей в одном цикле производства
MAX_SL = 20     # кол-во циклов отбора
MAX_MUT = 20    # кол-во циклов мутации
N = 9          # длина хромосомы

x1 = 0
x2 = 35


def toGray(organism):
    return '{:09b}'.format(graycode.tc_to_gray_code(organism))


def toTen(grayOrganism):
    return graycode.gray_code_to_tc(int(grayOrganism, 2))


def toX(organism):
    return organism * (x2 - x1) / 2 ** N


def crateMask():
    mask = [random.randint(0, 1) for i in range(0, N)] # Маска
    return mask

def selection(firstOrganism, secondOrganism):
    if fitness(toX(firstOrganism)) >= fitness(toX(secondOrganism)):
        return firstOrganism, firstOrganism
    else:
        return secondOrganism, secondOrganism


def crossing(firstOrganism, secondOrganism):

    mask = crateMask() # Создание маски

    firstOrganism = list(toGray(firstOrganism))
    secondOrganism = list(toGray(secondOrganism))

    child = []

    for i in range(0, N):
        if mask[i] == 1:
            child.append(firstOrganism[i])
        else:
            child.append(secondOrganism[i])

    child = toTen(''.join(child))

    return child, child


def mutation(organism):

    organism = list(toGray(organism))
    bit = random.randint(0, N - 1)

    if organism[bit] == '1':
        organism[bit] == '0'

    if organism[bit] == '0':
        organism[bit] == '1'

    organism = ''.join(organism)
    organism = toTen(organism)

    return organism


def fitness(x):
    return math.cos(x)*(x-3)*(x-9)*(x-1.5)*(x-15)*(x-4)


# Начальное поколение
entity = [random.randint(0, 2 ** N - 1) for _ in range(0, MAX_ENT)]



for q in range(Q):

    k = 0

    while k < MAX_SL:
        m1 = random.randint(0, MAX_ENT - 1)
        m2 = random.randint(0, MAX_ENT - 1)

        if m1 == m2:
            continue

        entity[m1], entity[m2] = selection(entity[m1], entity[m2])
        k += 1


    # Скрещивание

    fl_parent = np.full(MAX_ENT, True)
    k = 0

    while k < MAX_CH:
        m1 = random.randint(0, MAX_ENT - 1)
        m2 = random.randint(0, MAX_ENT - 1)

        if m1 == m2:
            continue
        if not (fl_parent[m1] & fl_parent[m2]):
            continue

        entity[m1], entity[m2] = crossing(entity[m1], entity[m2])

        fl_parent[m1], fl_parent[m2] = False, False
        k += 1


    # Мутация
    fl_mutation = np.full(MAX_ENT, True) # Флаги для мутации. Чтобы организм мог промутировать только один раз
    k = 0
    while k < MAX_MUT:
        index = random.randint(0, MAX_ENT - 1)
        if fl_mutation[index]:
            entity[index] = mutation(entity[index])
            fl_mutation[index] = False
            k += 1
        else:
            continue

fitnesses = [fitness(toX(entity[i])) for i in range(0, MAX_ENT)]

y_point = fitnesses[0]
x_point = toX(entity[0])

# Поиск значений Х и У для максимума
for i in range(1, MAX_ENT):
    if y_point < fitnesses[i]:
        y_point = fitnesses[i]
        x_point = toX(entity[i])


# построение графика
x = [i / 10 for i in range(0, 350)]
y = [fitness(x[i]) for i in range(0, len(x))]


plt.plot(x, y) # Строим график
plt.plot(x_point, y_point, 'ro') # Строим точку максимума
plt.show()


