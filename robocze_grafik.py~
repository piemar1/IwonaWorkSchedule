# -*- coding: utf-8 -*-
__author__ = 'marcin'

import random
hours_pex_month = 180
no_of_daywork = 2

example = [[u'A', u'D..D......UUUUUU...............'],
           [u'B', u'.......N...............N.......'],
           [u'C', u'...............................'],
           [u'D', u'...........D.........UUUUUUU...'],
           [u'E', u'...............................'],
           [u'F', u'......N..........D....N........'],
           [u'G', u'...............................'],
           [u'H', u'.........N..........D..........'],
           [u'I', u'...............................'],
           [u'J', u'UUU...UUUUUUU..................'],
           [u'K', u'...............................'],
           [u'L', u'DD......D.....UUUUUUUU.........'],
           [u'M', u'..........................DD...'],
           [u'N', u'.N......D..N................N.N'],
           [u'O', u'..N.......D..N........N.....N..']]
            # osoba, rodzaj dużuru w kolejnych dniach, liczba dużurów w miesiącu

"""
Do dodania i napisania
osobno liczba osób na dyżuże nocnym i dziennym  OK
przykładowo:
nocny 2 osoby                                   OK
dzienny 4 osoby                                 OK

przykładowa liczba osób do grafiku 15-16 osób

dodać możliwość urlopu w grafiku:               OK
dopisać U bez możliwośći wstawienia tam dyżuru  OK


pod rząd tylko dwa dyżury:    OK
dozwolone NN, DD, DN          OK
niedozwolone ND,              OK

W tygodniu , (ostatnich 7 dniach) dozwolony tylko 4 dyżury

Łączna liczba dyżurów w miesiącu na osobę uzależniona od liczby dni pracujących w miesiącu- tabela od mamy
Czyli uzupełniamy dyżury aż do danej liczby nawet dla osób z urlopami !!!!!1

"""

example1 = example
work = (u"D", u"N", u"U", u".")

person_per_day = 4       # liczba osón na dyżurze dziennym
person_per_night = 2     # liczba osón na dyżurze nocnym

team_size = len(example)              # liczba osób na załodze
days_in_month = len(example[0][1])    # liczba dnia w miesiącu
print days_in_month

def day_filtr(elem, days_no):
    # filtruje czy osobie można przypisać grafik
    # tutaj musza być zawarte wszystkie filtry !!!!!!!

    #[1] oznacza grafik w postaci stninga, [days_no] - numer dnia w miesiącu
    person = elem[1]

    if days_no == 0:
        if person[days_no] == '.' and person[days_no + 2] in '.':
            return True

    elif person[days_no] == '.':
        if days_no == 1:
            # jeżeli poprzedni dyżur nie był nocką --> True  and następny jest wolny
            if person[days_no - 1] in u'.DU' and person[days_no + 2] in '.':      # '.NU' for night
                return True
        elif days_no == days_in_month:
            if person[days_no - 1] in u'.DU':      # '.NU' for night
                return True


        elif 1 < days_no < days_in_month:
                  # jeżeli poprzedni dyżur nie był nocką --> True
            if person[days_no - 1] in u'.DU' and person[days_no - 2] in u'.U' and person[days_no + 1] in u'.U':
                return True
    return False



def night_filtr(elem, days_no):
    # filtruje czy osobie można przypisać grafik
    # tutaj musza być zawarte wszystkie filtry !!!!!!!

    #[1] oznacza grafik w postaci stninga, [days_no] - numer dnia w miesiącu
    # if days_no == 0:
        return True if elem[1][days_no] == '.' else False
    #
    # elif elem[1][days_no] == '.':
    #     if days_no > 1:
    #         # jeżeli 2 poprzednie dni dyżur --> False
    #         if elem[1][days_no - 1] in u'DN' and elem[1][days_no - 2] in u'DN':
    #             return False
    #     if days_no > 0:
    #         if elem[1][days_no - 1] == u'.':  # jeżeli poprzedniego dnia wolne --> True
    #             return True
    #         elif elem[1][days_no - 1] in u'D': # jeżeli poprzedniego dnia Dniówka --> False
    #             return False
    # return False



def index(name):
    # odnajduje osobę w grafiku po zastosowaniu random
    for elem in example:
        if name in elem:
            return example.index(elem)


def random_grafik2(example, person_per_day, person_per_night):
    # przypisuje losowo grafik na cały miesiąc

    for days_no in xrange(days_in_month):

        days, nights = person_per_day, person_per_night

        print 50 * '%'
        print "DAY NUMBER {}".format(days_no + 1)
        print 50 * '%'

        print "days", days, "nights", nights, "--> stan poczatkowy"    # tyle dyzurow w jednym dniu jest do obstawienia


        # przefiltrowanie, szukanie osob,
        # ktore nie maja wyznacznych dyzurow w danycm dniu
        for elem in example:
            if elem[1][days_no] == "D":               # [1] osoba [days_no] day number
                days -= 1
            if elem[1][days_no] == "N":
                nights -= 1

        # filtrowanie osób którym można dać dyżur, filtr liczby dyżurów i inne
        free_people = [elem[0] for elem in [item for item in example if day_filtr(item, days_no)]]
        # filter(function, iterable) is equivalent to [item for item in iterable if function(item)]

        # tyle brakuje wyznaczonych dyzurow N i D
        print "days", days, "nights", nights, "--> po uwzgledneniu pierwszych wpisow \n"
        print "len(free_people)", len(free_people), free_people    # drukowanie przefiltrowanie osob

        # wypełnianie grafiku dla dyżurów dziennych
        while days > 0:
            person = random.choice(free_people)
            free_people.remove(person)

            print "person", person
            print "len(free_people)", len(free_people)    # drukowanie przefiltrowanie osob

            person_index = index(person)
            example[person_index][1] = example[person_index][1][:days_no] + u"D" + example[person_index][1][days_no + 1:]
                                                             #  day number                           # [1:] day number
            days -= 1

        # filtrowanie osób którym można dać dyżur, filtr liczby dyżurów i inne
        free_people = [elem[0] for elem in [item for item in example if night_filtr(item, days_no)]]    # Dodanie argumentu dnia

        print "Po rozdaniu DNIOWEK --> \n len(free_people)", len(free_people), free_people    # drukowanie przefiltrowanie osob
        print "days", days, "nights", nights, "\n"    # tyle brakuje wyznaczonych dyzurow N i D

        # wypełnianie grafiku dla dyżurów nocnych
        while nights > 0:
            person = random.choice(free_people)
            free_people.remove(person)

            print "person", person
            print "len(free_people)", len(free_people)    # drukowanie przefiltrowanie osob

            person_index = index(person)
            example[person_index][1] = example[person_index][1][:days_no] + u"N" + example[person_index][1][days_no + 1:]
                                                                # [:0] day number                   # [1:] day number
            nights -= 1


        # # free_people = [elem[0] for elem in filter(filtr, example)]     # Dodanie argumentu dnia
        # free_people = [elem[0] for elem in [item for item in example if filtr(item, days_no)]]    # Dodanie argumentu dnia

        print "Po rozdaniu NOCEK --> \n len(free_people)", len(free_people), free_people    # drukowanie przefiltrowanie osob
        print "days", days, "nights", nights, "\n"    # tyle brakuje wyznaczonych dyzurow N i D


    # PRINTY
    for elem in example:
        print elem[0], elem[1]

    print 'GRAFIK UŁOŻONY !!!!'





def random_grafik1(example, person_per_day):
    """
    Randomowo ustala wolne dyzury ale tylko w pierwszym dniu miesiaca !!!
    """

    days, nights = person_per_day, person_per_day
    # przeszukuje pierwszy dzien na zadeklarowane dyzury

    print "days", days, "nights", nights, "--> stan poczatkowy"    # tyle dyzurow w jednym dniu jest do obstawienia

    for elem in example:
        if elem[1][0] == "D":
            days -= 1
        if elem[1][0] == "N":
            nights -= 1
    # przefiltrowanie, szukanie osob,
    # ktore nie maja wyznacznych dyzurow w danycm dniu
    free_people = [elem[0] for elem in filter(filtr, example)]

    print "days", days, "nights", nights, "--> po uwzgledneniu pierwszych wpisow \n"    # tyle brakuje wyznaczonych dyzurow N i D
    print "len(free_people)", len(free_people), free_people    # drukowanie przefiltrowanie osob
    # for elem in free_people:
    #     print elem


    while days > 0:
        person = random.choice(free_people)
        free_people.remove(person)

        print "person", person
        print "len(free_people)", len(free_people)    # drukowanie przefiltrowanie osob

        person_index = index(person)
        example[person_index][1] = example[person_index][1][:0] + u"D" + example[person_index][1][1:]
        days -= 1
    free_people = [elem[0] for elem in filter(filtr, example)]

    print "Po rozdaniu DNIOWEK --> \n len(free_people)", len(free_people), free_people    # drukowanie przefiltrowanie osob
    print "days", days, "nights", nights, "\n"    # tyle brakuje wyznaczonych dyzurow N i D


    while nights > 0:
        person = random.choice(free_people)
        free_people.remove(person)

        print "person", person
        print "len(free_people)", len(free_people)    # drukowanie przefiltrowanie osob

        person_index = index(person)
        example[person_index][1] = example[person_index][1][:0] + u"N" + example[person_index][1][1:]
        nights -= 1

    free_people = [elem[0] for elem in filter(filtr, example)]

    print "Po rozdaniu NOCEK --> \n len(free_people)", len(free_people), free_people    # drukowanie przefiltrowanie osob
    print "days", days, "nights", nights, "\n"    # tyle brakuje wyznaczonych dyzurow N i D


    # PRINTY
    for elem in example:
        print elem[0], elem[1]

    print "days", days, "nights", nights, "\n"    # tyle brakuje wyznaczonych dyzurow N i D
    free_people = [elem[0] for elem in filter(filtr, example)]
    print "len(free_people)", len(free_people)    # drukowanie przefiltrowanie osob


def random_grafik(example, person_per_day):
    days, nights = person_per_day, person_per_day
    for elem in example:
        if elem[1][0] == "D":
            days -= 1
        if elem[1][0] == "N":
            nights -= 1
    print days, nights

    while days > 0:
        no = random.randint(0, team_size-1)
        if example[no][1][0] not in u"ND":
            example[no][1] = u"D" + example[no][1]
            days -= 1

    while nights > 0:
        no = random.randint(0, team_size-1)
        if example[no][1][0] not in u"ND":
            example[no][1] = u"N" + example[no][1]
            nights -= 1

    print days, nights
    for elem in example:
        print elem[1]




# print '################################ - random_grafik'
# random_grafik(example, person_per_day)
# print '################################ \n - random_grafik1'
# random_grafik1(example, person_per_day)
print '################################ \n - random_grafik2'
random_grafik2(example, person_per_day, person_per_night)


# try:
#     random_grafik2(example, person_per_day, person_per_night)
# except:
#     print "GRAFIKU nie dało się ułożyć"
#
#     for elem in example:
#         print elem[0], elem[1]

