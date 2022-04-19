import graycode
import math
import random
import numpy as np
import matplotlib.pyplot as plt


Q = 60          # Кол-во поколений
MAX_ENT = 70    # размер популяции
MAX_CH = 30     # кол-во детей в одном цикле производства
N = 9           # длина хромосомы

x1 = 0
x2 = 35

def bin_to_gray(organism):
    return '{:09b}'.format(graycode.tc_to_gray_code(organism))


def to_ten(grayOrganism):
    return graycode.gray_code_to_tc(int(grayOrganism, 2))


def toX(organism):
    return organism * (x2 - x1) / 2 ** N

def fitness(x):
    return (math.sin(x-2)*math.cos(x+4)+ math.cos(3*x))*x**2


def wheel(population_for_wheel):

    fitneses = [fitness(toX(population_for_wheel[i])) for i in range(0, len(population_for_wheel))]
    maxfit = sum(fitneses)

    point = random.uniform(0, maxfit)


    range_sum = fitneses[0]
    i = 0

    while (point > range_sum):
        i += 1
        range_sum += fitneses[i]



    return population_for_wheel[i]


def screhivanie(parent1, parent2):
    parent1 = list(bin_to_gray(parent1))
    parent2 = list(bin_to_gray(parent2))

    child = []

    for i in range(0, N):
        chance = random.randint(0, 100)

        if chance >= 50:
            child.append(parent1[i])
        else:
            child.append(parent2[i])

    child = to_ten(''.join(child))

    return child


def mutation(organism):
    organism = list(bin_to_gray(organism))

    while True:
        rand_index_1 = random.randint(0, N - 1)
        rand_index_2 = random.randint(0, N - 1)

        if rand_index_1 != rand_index_2:
            break

    buff = organism[rand_index_1]

    organism[rand_index_1] = organism[rand_index_2]
    organism[rand_index_2] = buff

    organism = to_ten(''.join(organism))

    return organism


# Начальное поколение
entity = [random.randint(0, 2 ** N - 1) for _ in range(0, MAX_ENT)]
maxes_for_stop = []
stop_counter = 0

for q in range(Q):

    # Селекция
    population_for_wheel = []
    for elem in entity:
        if fitness(toX(elem)) > 0:
            population_for_wheel.append(elem)

    for i in range(0, 20):
        random_index = random.randint(0, MAX_ENT-1)
        entity[random_index] = wheel(population_for_wheel)


    # Cкрещивание
    fl_parent = np.full(MAX_ENT, True)
    k = 0

    while k < MAX_CH:
        m1 = random.randint(0, MAX_ENT - 1)
        m2 = random.randint(0, MAX_ENT - 1)

        if m1 == m2:
            continue
        if not (fl_parent[m1] & fl_parent[m2]):
            continue

        entity[m1] = screhivanie(entity[m1], entity[m2])
        entity[m2] = screhivanie(entity[m1], entity[m2])

        k += 1


    # Мутация
    k = 0
    while k < 15:
        random_index = random.randint(0, MAX_ENT - 1)
        entity[random_index] = mutation(entity[random_index])
        k += 1


    # Критерий останова
    maxes_for_stop.append(max([fitness(toX(entity[i])) for i in range(0, MAX_ENT)]))

    if q >= 1:
        if maxes_for_stop[q] == maxes_for_stop[q - 1]:
            stop_counter += 1


    if stop_counter >= 4:
        print(q)
        break







fitnesses = [fitness(toX(entity[i])) for i in range(0, MAX_ENT)]

y_point = fitnesses[0]
x_point = toX(entity[0])

for i in range(1, MAX_ENT):
    if y_point < fitnesses[i]:
        y_point = fitnesses[i]
        x_point = toX(entity[i])



x = [i / 10 for i in range(0, 350)]
y = [fitness(x[i]) for i in range(0, len(x))]


plt.plot(x, y)
plt.plot(x_point, y_point, 'ro')
plt.show()