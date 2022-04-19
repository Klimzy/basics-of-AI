import graycode
import math
import random
import numpy as np
import matplotlib.pyplot as plt

Q = 50  # Кол-во поколений
MAX_ENT = 30  # размер популяции
MAX_CH = 10  # кол-во детей в одном цикле производства
N = 9  # длина хромосомы
KRITERI = 49  # значения критейрия остановки
x1 = 0        # начальная точка промежутка
x2 = 35       # конечная точка промежутка

def fitness(x): # функция фитнеса, считающая значения функции по варианту
    return (0.8 * math.cos(3 * x) + math.cos(x)) * (x - 4)


def dc_to_gray(number): # функция перевода числа из 10 системы счисления в код Грея
    return '{:09b}'.format(graycode.tc_to_gray_code(number))


def gray_to_tc(gray_number): # функция перевода кода Грея в число 10 системы счисления
    return graycode.gray_code_to_tc(int(gray_number, 2))


def mutation(organism): # Функция мутации по варианту
    l = random.randint(0, len(organism) - 1) # выбираем рандомное положение в хромосоме
    organism = list(organism) # преобразуем организм в лист, чтобы можно было заменять числа

    for i in range(l, len(organism)): # цикл инверсии битов
        if organism[i] == '1':
            organism[i] = '0'
        else:
            organism[i] = '1'

    organism = ''.join(organism) # после проделанных операций превращаем организм обратно в строку

    return organism


def toX(organism): # функция, необходимая для расчета значения х по его номеру
    return organism * ((x2 - x1) / 2**N)


# Начальная популяция
entity = [dc_to_gray(random.randint(0, 2 ** N - 1)) for _ in range(MAX_ENT)] # Создание начальной популяции
y_maxes = [] # Массив для записи каждого максимума в каждом поколении
x = [] # Массив для записи каждого икса, соответствующего максимуму в каждом поколеннии
for q in range(Q):

    # воспроиздовство

    fl_parent = np.full(MAX_ENT, True) # Создание массива флагов (как в лекции)

    k = 0

    while k < MAX_CH:
        m1 = random.randint(0, MAX_ENT - 1)
        m2 = random.randint(0, MAX_ENT - 1)

        if m1 == m2:
            continue
        if not (fl_parent[m1] & fl_parent[m2]):
            continue

        parent1 = list(entity[m1]) # преобразуем строку в лист, чтобы можно было взять "середину" для размножению
        parent2 = list(entity[m2])

        child1 = parent1[:] # Копируем строку первого родителя в ребенка
        child2 = parent2[:]

        child1[3:6] = parent2[3:6] # Вставляем в первого ребенка (с 3 по 6 элемент) биты второго родителя
        child2[3:6] = parent1[3:6]

        entity[m1], entity[m2] = ''.join(child1), ''.join(child2) # вместо родителей в поколение подставляем детей

        fl_parent[m1] = False
        fl_parent[m2] = False

        k += 1

    # мутация
    randIndex = random.randint(0, MAX_ENT - 1)   # выбираем случайный индекс организма для мутации
    entity[randIndex] = mutation(entity[randIndex]) # подвергаем организм мутации и перезаписываем его в поколении

    # Поиск максимума в поколении

    # Создаем массив фитнесов сначала переведя особь из грейкода в десятичную систему счисления, а затем преобразуем
    # ее в значение Х

    fitnesses = [fitness(toX(gray_to_tc(entity[i]))) for i in range(0, MAX_ENT)]

    # Ищем максимальное значение У в текущем поколении и соответсвующее ему значение Х
    maxFit = fitnesses[0]
    x_point = toX(gray_to_tc(entity[0]))
    for i in range(1, MAX_ENT):
        if maxFit < fitnesses[i - 1]:
            maxFit = fitnesses[i]
            x_point = toX(gray_to_tc(entity[i]))

    y_maxes.append(maxFit) # Добавляем значение максимального У в массив
    x.append(x_point)      # Добавляем значение Х, соответсвующего максимальному значению У в массив

    # Критейий останова
    # Если значение У близко к критерию останова, то останавливаем поиск
    if (KRITERI - 0.2) <= y_maxes[q] <= (KRITERI + 0.2):
        break


# Построение графика


# Поиск значений Х У для отображения точки максимума
y_point = y_maxes[0]
x_point = x[0]

for i in range(1, len(y_maxes)):
    if y_point < y_maxes[i]:
        y_point = y_maxes[i]
        x_point = x[i]


# Создание значений х и у для построения графика
x = [i / 10 for i in range(0, 350)]
y = [fitness(x[i]) for i in range(0, len(x))]


plt.plot(x, y) # рисуем график по созданным значениям
plt.plot(x_point, y_point, 'ro') # рисуем точку максимума
plt.show() # отображаем график



