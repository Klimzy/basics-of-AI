import math
import seaborn as sns
import matplotlib.pylab as plt
import random
import numpy as np

x0 = 0
x1 = 35

N = 9                   # Размер хромосомы
Q = 20                  # Кол-во поколений
MAX_POPULATION = 50     # Размер популяции
Q_REPRODUCTION = 20     # Кол-во циклов скрещивания
Q_SELECTION = 20        # Кол-во циклов отбора
Q_MUTATION = 10         # Кол-во циклов мутации
samplingStep = math.fabs((x1 - x0) / 2 ** N)  # Шаг дискретизации



def fitness(x):
    return (0.8 * math.cos(3*x) + math.cos(x)) * (x-4)


def tournamentForMax(firstChromo, secondChromo):
    if fitness(firstChromo * samplingStep) > fitness(secondChromo * samplingStep):
        return firstChromo

    return secondChromo


def tournamentForMin(firstChromo, secondChromo):
    if fitness(firstChromo * samplingStep) < fitness(secondChromo * samplingStep):
        return firstChromo

    return secondChromo


def reproduction(firstParent, secondParent):

    locus = random.randint(0, N - 1)

    firstParent   = format(firstParent, '#011b').replace('0b', '').split(' ')
    secondParent  = format(secondParent, '#011b').replace('0b', '').split(' ')

    firstChild = firstParent[:locus] + secondParent[locus:]
    secondChild = secondParent[:locus] + firstParent[locus:]

    firstChild = ''.join(firstChild)
    secondChild = ''.join(secondChild)

    return int(firstChild, 2), int(secondChild, 2)


def mutation(chromo):
    chromo = list(format(chromo, '#011b').replace('0b', ''))
    locus = random.randint(0, N-1)

    for i in range(locus, N):
        if chromo[i] == '1':
            chromo[i] = '0'

        else:
            chromo[i] = '1'


    chromo = ''.join(chromo)

    return int(chromo, 2)


populationForMax = [random.randint(0, 2**N - 1) for _ in range(0, MAX_POPULATION)]
populationForMin = [random.randint(0, 2**N - 1) for _ in range(0, MAX_POPULATION)]

y_min_sample = []
y_max_sample = []


for _ in range(0, Q):

    # ОТБОР
    for _ in range(0, Q_SELECTION):
        randIndex1 = random.randint(0, MAX_POPULATION - 1)
        randIndex2 = random.randint(0, MAX_POPULATION - 1)

        populationForMax[randIndex1] = tournamentForMax(populationForMax[randIndex1], populationForMax[randIndex2])
        populationForMax[randIndex2] = tournamentForMax(populationForMax[randIndex1], populationForMax[randIndex2])

        populationForMin[randIndex1] = tournamentForMin(populationForMin[randIndex1], populationForMin[randIndex2])
        populationForMin[randIndex2] = tournamentForMin(populationForMin[randIndex1], populationForMin[randIndex2])

    # СКРЕЩИВАНИЕ

    for _ in range(0, Q_REPRODUCTION):
        parentFlag = [True for _ in range(0, MAX_POPULATION)]

        while True:
            firstParentIndex  = random.randint(0, MAX_POPULATION - 1)
            secondParentIndex = random.randint(0, MAX_POPULATION - 1)

            if parentFlag[firstParentIndex] == True and parentFlag[secondParentIndex] == True:
                break

        populationForMax[firstParentIndex], populationForMax[secondParentIndex] = \
            reproduction(populationForMax[firstParentIndex], populationForMax[secondParentIndex])

        populationForMin[firstParentIndex], populationForMin[secondParentIndex] = \
            reproduction(populationForMin[firstParentIndex], populationForMin[secondParentIndex])

        parentFlag[firstParentIndex], parentFlag[secondParentIndex] = False, False

    # МУТАЦИИ

    for _ in range(0, Q_MUTATION):
        mutationFlag = [True for _ in range(0, MAX_POPULATION)]

        while True:
            randIndex = random.randint(0, MAX_POPULATION - 1)
            if mutationFlag[randIndex] == True:
                break

        populationForMax[randIndex] = mutation(populationForMax[randIndex])
        populationForMin[randIndex] = mutation(populationForMin[randIndex])

        mutationFlag[randIndex] = False


    # Данные по каждому поколению для диаграммы рассеяния


    for i in range(1, MAX_POPULATION - 1):
        if fitness(populationForMax[i] * samplingStep) < fitness(populationForMax[i + 1] * samplingStep):
            y_max = fitness(populationForMax[i + 1] * samplingStep)

    y_max_sample.append(y_max)

    for i in range(1, MAX_POPULATION - 1):
        if fitness(populationForMin[i] * samplingStep) > fitness(populationForMin[i + 1] * samplingStep):
            y_min = fitness(populationForMin[i + 1] * samplingStep)

    y_min_sample.append(y_min)




# Поиск максимумов
for i in range(1, MAX_POPULATION - 1):
    if fitness(populationForMax[i] * samplingStep) < fitness(populationForMax[i+1] * samplingStep):
        y_max = fitness(populationForMax[i+1] * samplingStep)
        x_max = populationForMax[i+1] * samplingStep


# Поиск минимумов
for i in range(1, MAX_POPULATION - 1):
    if fitness(populationForMin[i] * samplingStep) > fitness(populationForMin[i+1] * samplingStep):
        y_min = fitness(populationForMin[i+1] * samplingStep)
        x_min = populationForMin[i+1] * samplingStep




# Построение графика функции
x = np.arange(0, 35, 0.1)
y = [fitness(x[i]) for i in range(0, len(x))]

sns.lineplot(x = x, y = y)
plt.plot(x_min, y_min, 'ro')
plt.plot(x_max, y_max, 'ro')
plt.show()


# Построение диаграммы рассеяния
x = np.arange(0, Q)
plt.scatter(x, y_min_sample)
plt.scatter(x, y_max_sample)
plt.show()







