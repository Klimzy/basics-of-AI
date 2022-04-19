import graycode
import math
import random
import numpy as np
import matplotlib.pyplot as plt

Q = 60          # Кол-во поколений
MAX_ENT = 70    # размер популяции
MAX_CH = 30     # кол-во детей в одном цикле производства
MAX_SL = 40     # кол-во циклов отбора
MAX_MUT = 25    # кол-во циклов мутации
N = 9           # длина хромосомы

def toGray(organism):
    return '{:09b}'.format(graycode.tc_to_gray_code(organism))


def toTC(grayOrganism):
    return graycode.gray_code_to_tc(int(grayOrganism, 2))


def toX(organism):
    return organism * 35 / 2 ** N


def fitness(x):
    return x ** 2 * (math.sin(x - 2.75) * math.cos(x + 5) + math.sin(3 * x))


def selection(firstOrganism, secondOrganism):
    if fitness(toX(firstOrganism)) >= fitness(toX(secondOrganism)):
        return firstOrganism, firstOrganism
    else:
        return secondOrganism, secondOrganism


def crateMask():
    mask = [random.randint(0, 1) for i in range(0, N)]
    return mask


def crossing(firstOrganism, secondOrganism):
    mask = crateMask()

    firstOrganism = list(toGray(firstOrganism))
    secondOrganism = list(toGray(secondOrganism))

    child = []

    for i in range(0, N):
        if mask[i] == 1:
            child.append(firstOrganism[i])
        else:
            child.append(secondOrganism[i])

    child = toTC(''.join(child))

    return child, child


def mutation(organism):
    organism = list(toGray(organism))
    bit = random.randint(0, N - 1)

    if organism[bit] == '1':
        organism[bit] = '0'
    else:
        organism[bit] = '1'

    organism = toTC(''.join(organism))

    return organism


# Начальное поколение
entity = [random.randint(0, 2 ** N - 1) for _ in range(0, MAX_ENT)]

for q in range(Q):
    # Селекция

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

    fl_mutation = np.full(MAX_ENT, True)
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

for i in range(1, MAX_ENT):
    if y_point < fitnesses[i]:
        y_point = fitnesses[i]
        x_point = toX(entity[i])








# построение графика
x = [i / 10 for i in range(0, 350)]
y = [fitness(x[i]) for i in range(0, len(x))]


plt.plot(x, y)
plt.plot(x_point, y_point, 'ro')
plt.show()


