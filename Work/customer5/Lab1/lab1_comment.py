import graycode
import math
import random
import numpy as np
import matplotlib.pyplot as plt


Q = 80          # Кол-во поколений
MAX_ENT = 70    # размер популяции
MAX_CH = 30     # кол-во детей в одном цикле производства
N = 9           # длина хромосомы

x1 = 0  # начальная точка отрезка, на котором будем искать экстремум функции
x2 = 35 # конечная точка отрезка, на котором будем искать экстремум функции



def bin_to_gray(organism):
    """Функция перевода числа в код Грея"""
    return '{:09b}'.format(graycode.tc_to_gray_code(organism))


def to_ten(grayOrganism):
    """Функция перевода числа из кода Грея в 10 Систему считсления"""
    return graycode.gray_code_to_tc(int(grayOrganism, 2))


def toX(organism):
    """Функция перевода номера икса (который мы кодируем кодом грея) в значение икса"""
    return organism * (x2 - x1) / 2 ** N

def fitness(x):
    """Функция фитнеса"""
    return (math.sin(x-2)*math.cos(x+4)+ math.cos(3*x))*x**2


def wheel(population_for_wheel):
    """Функция селекции методом рулетки"""
    fitneses = [fitness(toX(population_for_wheel[i])) for i in range(0, len(population_for_wheel))] # считаем фитнесы для всей популяции, которую мы отобрали
    maxfit = sum(fitneses) # Считаем сумму фитнесов

    point = random.uniform(0, maxfit) # Задаем рандомное число в промежутке от нуля до суммы фитнесов


    range_sum = fitneses[0] # промежуточная сумма фитнесов инициализируется
    i = 0

    while point > range_sum: # пока поинт меньше range_sum
        i += 1 # прибавляем к i единицу
        range_sum += fitneses[i] # к range_sum прибавляем i-тый элемент из массива fitneses

    # возвращаем и-тый элемент из отобранной популяции, которую мы передавали в функцию
    # возвращается номер икса, выбранного рулеткой
    return population_for_wheel[i]


def screhivanie(parent1, parent2):
    parent1 = list(bin_to_gray(parent1))  # преобразуем организм в код грея и в лист, чтобы можно было иттерировать
    parent2 = list(bin_to_gray(parent2))

    child = [] # создаем массив для ребенка

    for i in range(0, N):
        chance = random.randint(0, 100) # задаем рандомное число от 0 до 100

        if chance >= 50: # если шанс больше 50, то берем i-тый бит от первого родителя
            child.append(parent1[i])
        else:
            child.append(parent2[i])  # если шанс меньше 50, то берем i-тый бит от второго родителя

    child = to_ten(''.join(child))  # Преобразуем значение ребенка к десятичному виду

    return child


def mutation(organism):
    """Функция мутации организма"""

    organism = list(bin_to_gray(organism)) # преобразуем организм в код грея и в лист, чтобы можно было иттерировать

    while True:
        rand_index_1 = random.randint(0, N - 1) # создаем рандомный индекс от 0 до N-1
        rand_index_2 = random.randint(0, N - 1)

        if rand_index_1 != rand_index_2: # если эти индексы не равны, то останавливаем генерацию радномных индексов
            break

    buff = organism[rand_index_1] # запоминаем первый бит, который хотим перезаписать в переменную буффер

    organism[rand_index_1] = organism[rand_index_2] # вместо бита с индексом rand_index_1 записываем бит под индексом rand_index_2
    organism[rand_index_2] = buff # вместо бита с индексом rand_index_2 записываем бит, который мы записали в буффер

    organism = to_ten(''.join(organism)) # Преобразуем значение организма к десятичному виду

    return organism


# Начальное поколение
entity = [random.randint(0, 2 ** N - 1) for _ in range(0, MAX_ENT)] # генерация начальной популяции
maxes_for_stop = [] # массив для вычисления изменения целевой функции на каждой итерации
stop_counter = 0    # счетчик для остановки алгоритма

for q in range(Q):

    # Селекция

    # создаем массив для рулетки. В эту популяцию будем записывать только те организмы,
    # фитнесы которых больше 0
    population_for_wheel = []

    for elem in entity:
        if fitness(toX(elem)) > 0: # если фитнес организма больше 0
            population_for_wheel.append(elem) # записываем его в популяцию для рулетки

    # запускаем рулетку 20 раз
    for i in range(0, 20):
        random_index = random.randint(0, MAX_ENT-1) # выбераем рандомный организм
        entity[random_index] = wheel(population_for_wheel) # перезаписываем его победителем в рулетке


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

        entity[m1] = screhivanie(entity[m1], entity[m2]) # Скрестить родителей и заменить их ребенком
        entity[m2] = screhivanie(entity[m1], entity[m2]) # Скрестить родителей и заменить их ребенком

        k += 1


    # Мутация
    k = 0


    # промутируем организмы 10 раз
    while k < 10:
        random_index = random.randint(0, MAX_ENT - 1) # создадим радномное число, чтобы выбрать рандомный организм для мутации
        entity[random_index] = mutation(entity[random_index]) # записываем на место рандомного организма этот же организм, только мутировавший
        k += 1


    # Критерий останова
    # считаем фитнесы для каждого организма, а затем добавляем максимум из этих фитнесов в массив для критерия останова
    # (его мы объявляли в начале программы)
    maxes_for_stop.append(max([fitness(toX(entity[i])) for i in range(0, MAX_ENT)]))

    if q >= 1:
        if maxes_for_stop[q] == maxes_for_stop[q - 1]: # если q элемент в массиве для критерия останова равен q - 1
            stop_counter += 1 # увеличиваем стопкаунтер на единницу
        else: # иначе зануляем его
            stop_counter = 0


    # если стопкаунтер больше или равен 5, то останавливаем работу программы
    if stop_counter >= 5:
        print(q)
        break







fitnesses = [fitness(toX(entity[i])) for i in range(0, MAX_ENT)] # Создать массив У из популяции. Каждый организм преобразуем сначала к значению Х а затем считаем фитнес

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
plt.plot(x_point, y_point, 'ro')  # Строим точку максимума
plt.show()