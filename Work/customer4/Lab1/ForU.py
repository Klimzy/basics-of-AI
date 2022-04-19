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
    """Функция перевода числа в код Грея"""
    return '{:09b}'.format(graycode.tc_to_gray_code(organism))


def toTen(grayOrganism):
    """Функция перевода числа из кода Грея в 10 Систему считсления"""
    return graycode.gray_code_to_tc(int(grayOrganism, 2))


def toX(organism):
    """Функция перевода номера икса (который мы кодируем кодом грея) в значение икса"""
    return organism * (x2 - x1) / 2 ** N


def crateMask():
    """Функция создания маски для скрещивания"""
    mask = [random.randint(0, 1) for i in range(0, N)] # Создание массива масски из рандомных нулей и единиц, размером N
    return mask

def selection(firstOrganism, secondOrganism):
    """Функция турнирной селекции"""
    if fitness(toX(firstOrganism)) >= fitness(toX(secondOrganism)): # Если фитнес первого организма больше фитнеса второго, возвращаем первый организм
        return firstOrganism, firstOrganism
    else:
        return secondOrganism, secondOrganism # Иначе возвращаем второй организм


def crossing(firstOrganism, secondOrganism):
    """Функция для размножения"""
    mask = crateMask() # Создание маски

    firstOrganism = list(toGray(firstOrganism))  # представляем организм в код грея и в лист, чтобы можно было иттерировать
    secondOrganism = list(toGray(secondOrganism)) #

    child = [] # Массив для ребенка

    for i in range(0, N):
        if mask[i] == 1: # Если значение i-ого элемента в маске равно 1, берем бит из первого родителя, если значение маски 0, берем значение бита для ребенка из второго
            child.append(firstOrganism[i])
        else:
            child.append(secondOrganism[i])

    child = toTen(''.join(child)) # Преобразуем значение к десятичному виду

    return child, child


def mutation(organism):
    """Функция мутации организма"""
    organism = list(toGray(organism))
    bit = random.randint(0, N - 1)  # Выбор рандомного бита для инверсии

    if organism[bit] == '1':
        organism[bit] == '0'

    if organism[bit] == '0':
        organism[bit] == '1'

    organism = ''.join(organism)
    organism = toTen(organism)

    return organism


def fitness(x):
    """Функция фитнеса"""
    return math.cos(x)*(x-3)*(x-9)*(x-1.5)*(x-15)*(x-4)


# Начальное поколение
entity = [random.randint(0, 2 ** N - 1) for _ in range(0, MAX_ENT)]



for q in range(Q):

    k = 0

    while k < MAX_SL:
        m1 = random.randint(0, MAX_ENT - 1) # Создание рандомного индекса для первой особи
        m2 = random.randint(0, MAX_ENT - 1)

        if m1 == m2: # Если два одинаковых числа, начать заново
            continue


        entity[m1], entity[m2] = selection(entity[m1], entity[m2]) # Провести селекцию двух организмов и в популяции проигравшего заменить на победителя
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

        entity[m1], entity[m2] = crossing(entity[m1], entity[m2])  # Скрестить родителей и заменить их ребенком

        fl_parent[m1], fl_parent[m2] = False, False
        k += 1


    # Мутация
    fl_mutation = np.full(MAX_ENT, True) # Флаги для мутации. Чтобы организм мог промутировать только один раз
    k = 0
    while k < MAX_MUT:
        index = random.randint(0, MAX_ENT - 1) # Создание рандомного индекса для выбора особи из популяции
        if fl_mutation[index]: # Если организм еще не мутировал
            entity[index] = mutation(entity[index]) # Заменить исходный организм в популяции мутировавшим
            fl_mutation[index] = False # Сбросить флаг для мутации
            k += 1
        else:
            continue





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
plt.plot(x_point, y_point, 'ro') # Строим точку максимума
plt.show()


