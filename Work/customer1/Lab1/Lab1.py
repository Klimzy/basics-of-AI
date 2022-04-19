import graycode
import math
import random
import numpy as np
import matplotlib.pyplot as plt

Q = 50          # Кол-во поколений
MAX_ENT = 30    # размер популяции
MAX_CH = 10     # кол-во детей в одном цикле производства
N = 9           # длина хромосомы
KRITERI = 49    # значения критейрия остановки
x1 = 0
x2 = 35

def fitness(x):
    return (0.8 * math.cos(3 * x) + math.cos(x)) * (x - 4)


def dc_to_gray(number):
    return '{:09b}'.format(graycode.tc_to_gray_code(number))


def gray_to_tc(gray_number):
    return graycode.gray_code_to_tc(int(gray_number, 2))


def mutation(organism):
    l = random.randint(0, len(organism) - 1)
    organism = list(organism)

    for i in range(l, len(organism)):
        if organism[i] == '1':
            organism[i] = '0'
        else:
            organism[i] = '1'

    organism = ''.join(organism)

    return organism


def toX(organism):
    return organism * ((x2 - x1) / 2**N)


# Начальное поколение
entity = [dc_to_gray(random.randint(0, 2 ** N - 1)) for _ in range(MAX_ENT)]
y_maxes = []
x = []
for q in range(Q):

    # воспроиздовство

    fl_parent = np.full(MAX_ENT, True)

    k = 0

    while k < MAX_CH:
        m1 = random.randint(0, MAX_ENT - 1)
        m2 = random.randint(0, MAX_ENT - 1)

        if m1 == m2:
            continue
        if not (fl_parent[m1] & fl_parent[m2]):
            continue

        parent1 = list(entity[m1])
        parent2 = list(entity[m2])

        child1 = parent1[:]
        child2 = parent2[:]

        child1[3:6] = parent2[3:6]
        child2[3:6] = parent1[3:6]

        entity[m1], entity[m2] = ''.join(child1), ''.join(child2)

        fl_parent[m1] = False
        fl_parent[m2] = False

        k += 1

    # мутация
    randIndex = random.randint(0, MAX_ENT - 1)
    entity[randIndex] = mutation(entity[randIndex])

    # Поиск максимума в поколении
    fitnesses = [fitness(toX(gray_to_tc(entity[i]))) for i in range(0, MAX_ENT)]

    maxFit = fitnesses[0]
    x_point = toX(gray_to_tc(entity[0]))
    for i in range(1, MAX_ENT):
        if maxFit < fitnesses[i - 1]:
            maxFit = fitnesses[i]
            x_point = toX(gray_to_tc(entity[i]))

    y_maxes.append(maxFit)
    x.append(x_point)

    if (KRITERI - 0.2) <= y_maxes[q] <= (KRITERI + 0.2):
        break


# Построение графика
y_point = y_maxes[0]
x_point = x[0]

for i in range(1, len(y_maxes)):
    if y_point < y_maxes[i]:
        y_point = y_maxes[i]
        x_point = x[i]


x = [i / 10 for i in range(0, 350)]
y = [fitness(x[i]) for i in range(0, len(x))]


plt.plot(x, y)
plt.plot(x_point, y_point, 'ro')
plt.show()



