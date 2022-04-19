import random
import math

MAX_ENT = 10

N = 9


def toX(organism):
    return organism * (35) / 2 ** N


def fitness(x):
    return (math.sin(x-2)*math.cos(x+4)+ math.cos(3*x))*x**2


def wheel(population_for_wheel):

    fitneses = [fitness(toX(population_for_wheel[i])) for i in range(0, len(population_for_wheel))]
    maxfit = sum(fitneses)

    point = random.uniform(0, maxfit)

    print('\n', 'point = ', point, '\n')

    range_sum = fitneses[0]
    i = 0

    while (point > range_sum):
        i += 1
        range_sum += fitneses[i]



    return population_for_wheel[i]



entity = [random.randint(0, 2 ** N - 1) for _ in range(0, MAX_ENT)]

population_for_wheel = []
for elem in entity:
    if fitness(toX(elem)) > 0:
        population_for_wheel.append(elem)





fit = [fitness(toX(population_for_wheel[i])) for i in range(0, len(population_for_wheel))]

for i in range(0, len(population_for_wheel)):
    print(population_for_wheel[i], '\t\t\t', fit[i])




print(wheel(population_for_wheel))


