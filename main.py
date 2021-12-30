import numpy as np
import random as rd
import matplotlib.pyplot as plt
import itertools


def countlen(chromo, distance, city_num):
    """Загальна довжина шляху, яка відповідає хромосомі"""
    lenth = 0
    for iii in range(city_num - 1):
        lenth += distance[chromo[iii]][chromo[iii + 1]]
    lenth += distance[chromo[city_num - 1]][chromo[0]]
    return lenth


def crepopula(city_num, m):
    """Створення популяції"""
    popula = []  # Чисельність населення
    for ii in range(m):
        chromo = np.random.permutation(city_num).tolist()  # Хромосома
        popula.append(chromo)
    return popula


def countprobabily(popula, distance, city_num):
    """Розрахунок сукупної ймовірності кожної людини у популяції"""
    evall = []
    for chromo in popula:
        evl = max(30000 - countlen(chromo, distance, city_num), 0)  # Функція допасованості
        evall.append(evl)
    seval = sum(evall)
    probabil = evall / seval
    probabily = probabil.copy()
    for i in range(1, len(popula)):
        probabily[i] = probabily[i] + probabily[i - 1]
    return probabily


def lpd(popula, probabily, m):
    """Відбір потомства"""
    newpopula = []
    selechromo = 0
    for i in range(m):
        proba = rd.random()
        for ii in range(len(probabily)):
            if probabily[ii] >= proba:
                selechromo = popula[ii]
                break
        newpopula.append(selechromo)
    return newpopula


def crossover_nn(father1, father2, city_num, distance):
    """Евристичне схрещення"""
    father_1 = father1.copy()
    father_2 = father2.copy()
    city0 = rd.randint(0, city_num - 1)  # Випадкове місто як відправна точка
    son = [city0]
    while len(son) < len(father1):
        ord1 = father_1.index(city0)
        ord2 = father_2.index(city0)
        if ord1 == len(father_1) - 1:
            ord1 = -1
        if ord2 == len(father_1) - 1:
            ord2 = -1
        city1 = father_1[ord1 + 1]
        city2 = father_2[ord2 + 1]
        father_1.remove(city0)
        father_2.remove(city0)
        if distance[city0][city1] <= distance[city0][city2]:
            son.append(city1)
            city0 = city1
        else:
            son.append(city2)
            city0 = city2
    return son


def variat2(father, city_num, distance):
    """Евристична варіація"""
    or1 = rd.randint(0, city_num - 1)  # Вибір 5 випадкових положень
    or2 = rd.randint(0, city_num - 1)
    or3 = rd.randint(0, city_num - 1)
    or4 = rd.randint(0, city_num - 1)
    or5 = rd.randint(0, city_num - 1)
    not_same = list({or1, or2, or3, or4, or5})
    ords = list(itertools.permutations(not_same, len(not_same)))
    sons = []
    sonn = father.copy()
    for ord in ords:
        for ii in range(len(not_same)):
            sonn[not_same[ii]] = father[ord[ii]]
        sons.append(sonn)
    son_leng = []  # Відстань до всіх дітей
    for sonn in sons:
        leng = countlen(sonn, distance, city_num)
        son_leng.append(leng)
    n = son_leng.index(min(son_leng))   # Вибір мінімальної відстані
    return sons[n]


def main():
    """Координати міст"""
    cities = [[565, 575], [125, 185], [345, 750], [945, 685], [845, 955], [880, 260], [225, 230],
              [525, 980], [580, 1175], [650, 1130], [1205, 620], [1220, 580], [1065, 440], [1090, 870],
              [845, 680], [725, 370], [145, 665], [415, 635], [510, 875], [560, 365], [300, 465],
              [520, 585], [480, 415], [835, 1125], [975, 580], [915, 245], [225, 1075], [850, 400],
              [660, 180], [410, 250], [420, 555], [575, 665], [1150, 1160], [700, 480], [685, 595],
              [685, 810], [770, 610], [795, 645], [720, 635], [760, 650], [475, 960], [95, 260],
              [875, 920], [900, 500], [555, 815], [830, 485], [1170, 65], [830, 610], [605, 625],
              [595, 360], [1140, 725], [940, 245], [930, 800], [400, 970], [1000, 180], [650, 590]]
    ppl_num = 10  # Чисельність населення
    city_num = len(cities)  # Кількість міст (довжина хромосоми)
    generations = 500  # Кількість поколінь
    x_city = []
    y_city = []
    for city in cities:
        x_city.append(city[0])
        y_city.append(city[1])

    """Визначення матриці відстаней"""
    distance = np.zeros([city_num, city_num])
    for i in range(city_num):
        for j in range(city_num):
            distance[i][j] = pow((pow(cities[i][0]-cities[j][0], 2) + pow(cities[i][1]-cities[j][1], 2)), 0.5)

    """Створення популяції"""
    popula = crepopula(city_num, ppl_num)

    """Еволюція населення"""
    for n in range(generations):
        pc = 0.8  # Швидкість схрещення
        pv = 0.25  # Швидкість мутації
        son = []

        """Схрещення"""
        crossgroup = []
        for i in range(ppl_num):
            cpb = rd.random()
            if cpb < pc:  # Умова схрещення
                crossgroup.append(popula[i])
        if len(crossgroup) % 2 == 1:
            del crossgroup[-1]

        """Евристичне схрещення"""
        if crossgroup:
            for ii in range(0, len(crossgroup), 2):
                sonc = crossover_nn(crossgroup[ii], crossgroup[ii + 1], city_num, distance)
                son.append(sonc)

        """Мутації"""
        variatgroup = []
        for j in range(ppl_num):
            vpb = rd.random()
            if vpb < pv:  # Умова мутації
                variatgroup.append(popula[j])
        if variatgroup:
            for vag in variatgroup:
                sonv = variat2(vag, city_num, distance)  # Мутація
                son.append(sonv)

        """Сукупна ймовірність кожної хромосоми"""
        populapuls = popula + son
        probabily = countprobabily(populapuls, distance, city_num)

        """Створення нового покоління"""
        popula = lpd(populapuls, probabily, ppl_num)

    """Вибір кращої хромосоми"""
    opt_chr = popula[0]
    opt_len = countlen(opt_chr, distance, city_num)
    for chrm in popula:
        chrlen = countlen(chrm, distance, city_num)
        if chrlen < opt_len:
            opt_chr = chrm
            opt_len = chrlen
    print("Оптимальний шлях: " + str(opt_chr))
    print("Оптимальне значення: " + str(opt_len))

    """Малюємо шлях на карті"""
    plt.plot(x_city, y_city, marker='o', lw='0', color='r')
    plt.show()
    for cor in range(len(opt_chr) - 1):
        x = [cities[opt_chr[cor]][0], cities[opt_chr[cor + 1]][0]]
        y = [cities[opt_chr[cor]][1], cities[opt_chr[cor + 1]][1]]
        plt.plot(x, y, "b-")
    plt.plot(x_city, y_city, marker='o', lw='0', color='r')
    plt.show()


if __name__ == "__main__":
    main()
