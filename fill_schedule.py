# -*- coding: utf-8 -*-
__author__ = 'marcin'

"""
Do dodania i napisania
osobno liczba osób na dyżuże nocnym i dziennym  OK
przykładowo:
nocny 2 osoby                                   OK
dzienny 4 osoby                                 OK

przykładowa liczba osób do grafiku 15-16 osób

dodać get_working_daysmożliwość urlopu w grafiku:               OK
dopisać U bez możliwośći wstawienia tam dyżuru  OK

pod rząd tylko dwa dyżury:    OK
dozwolone NN, DD, DN          OK
niedozwolone ND,              OK

W tygodniu , (ostatnich 7 dniach) dozwolony tylko 4 dyżury

Łączna liczba dyżurów w miesiącu na osobę uzależniona od liczby dni pracujących w miesiącu- tabela od mamy
Czyli uzupełniamy dyżury aż do danej liczby nawet dla osób z urlopami !!!!!1
"""


import random
from models import Person, Schedule

# person_per_day = 4       # liczba osón na dyżurze dziennym
# person_per_night = 2     # liczba osón na dyżurze nocnym
# number_of_working_days = 21

def create_team_for_schedule_filing(schedule):
    """
    Tworzy instancje klas Person w celu uzupełniania grafiku
    """
    crew = schedule.crew
    schedules = schedule.schedule
    return [Person(name, person_schedule) for name, person_schedule in zip(crew, schedules)]


def input_work_to_person(one_schedule, day_number, work):
    """
    Metoda wprowadza zmiany w grafiku dla zadanego, grafiku, dnia i rodzaju dyżuru
    """
    if day_number == 0:
        output_schedule = "{}{}".format(work, one_schedule[1:])

    else:
        output_schedule = "{}{}{}".format(one_schedule[:day_number],
                                          work,
                                          one_schedule[day_number + 1:])

    return output_schedule


def get_number_of_free_worktype(day_number, people, work):
    number = 0
    for person in people:
        if person.schedule[day_number] == work:
            number += 1
    return number


def get_person_number_by_name(name, people):
    """
    Zwraca instancję Person z listy People wedłóg nadanego name.
    """
    for no, person in enumerate(people):
        if person.name == name:
            return no


def filtr_working_days_in_week(str):
    """
    Funkcja zwraca True jeśli liczba dni roboczych w str nie przekracza 4, inaczej False
    """
    number = 0
    for day in str:
        if day == u"D" or day == u"N":
            number += 1
    if number > 4:
        return False
    return True


def get_free_people(day_number, people, work, no_of_working_days):
    """
    Zwraca listę osób (w postaci atrybutów person.name), które moga przyjąć dyżur -
    Tutaj muszą być wszystkie filtry
    - I    osoba bez dyżuru              ok
    - II  dyżury pod rząd                ok
    - III liczba dyżurów w tygodniu
    - IV  liczba dyżurów w miesiącu
    """
    """
    Plan
    - I lista osób jakie mają wolny dzień
    - dodanie zmiennej schedule dla osoby i dodanie tego dyżuru NOCKA lub DNiówka, !!!!!! wymaga wprowadzenia nowego argumentu  N lub D
    - filtry  II, III, IV
    """
    # tworzenie tymczasowych insyancji Person - tylko w celu wypełniania grafiku
    people_for_one_day = [Person(person.name, person.schedule) for person in people]


    # filtrowanie osób, które mają wolny dzień
    people_free_day = [person for person in people_for_one_day if person.wheather_day_is_free(day_number)]

    # for person in people_free_day:
    #     print("people_free_day", person.name)

    # uzupełnienie grafiku o przykładowy dzień pracy - wedłóg day_number i work
    people_filled_example_work = []

    for person in people_free_day:
        person.schedule = input_work_to_person(person.schedule, day_number, work)
        people_filled_example_work.append(person)

    # for person in people_filled_example_work:
    #     print("people_filled_example_work", person.name, person.schedule)


    # filtrowanie osób z brakiem podwójnych dyżurów pod rząd   - brak "ND"
    people_filtr_1 = []
    for person in people_filled_example_work:
        if "ND" not in person.schedule:
            people_filtr_1.append(person)

    # for person in people_filtr_1:
    #     print("people_filtr_1", person.name, person.schedule)


    # filtrowanie po dozwolonej liczbie 4 dyżurów w tygodniu
    people_filtr_2 = []

    for person in people_filtr_1:
        schedule_parts = [person.schedule[numbers:numbers + 7] for numbers in range(len(person.schedule) - 7)]
        results = [filtr_working_days_in_week(parts) for parts in schedule_parts]
        if all(results):
            people_filtr_2.append(person)

    # for person in people_filtr_2:
    #     print("people_filtr_2", person.name, person.schedule)

    # filtrowanie po maksymalnej liczbie dni roboczych w miesiącu
    # 13 liczba dozwolonych dyżurów 12h w miesiącu !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    people_filtr_3 = [person for person in people_filtr_2 if person.get_working_days_number_person() <= no_of_working_days]

    return [person.name for person in people_filtr_3]





##############################################################################################

def fill_the_schedule(schedule, no_of_working_days, person_per_day, person_per_night):

    month_lenght = len(schedule.schedule[0])
    # print("month_lenght", month_lenght)

    people = create_team_for_schedule_filing(schedule)   # lista osób w postaci instancji Person
    # for person in people:
    #     print("person.name, person.schedule", person.name, person.schedule)

    for day_number in range(month_lenght):

        # NIGHTS

        # liczba osób potrzebnych
        number_of_need_night = person_per_night - get_number_of_free_worktype(day_number, people, "N")
        # print("number_of_need_night", number_of_need_night)

        # tworzenie listy ludzi którzy mogą przyjąć dyżur
        list_of_free_persons = get_free_people(day_number, people, "N", no_of_working_days)
        # print("free people", list_of_free_persons)

        for night in range(number_of_need_night):

            selected_person_name = random.choice(list_of_free_persons)    # losowanie osoby
            # print("selected_person_name", selected_person_name)

            # zdobycie numeru wylosowanej osoby w liście people !!!!!!!!!!
            selected_person_number = get_person_number_by_name(selected_person_name, people)
            # print("selected_person_number", selected_person_number)

            # pobranie grafiku
            one_schedule = people[selected_person_number].schedule
            # print(selected_person_name, selected_person_number, one_schedule)

            # wprowadzenie zmiany do grafiku
            new_schedule = input_work_to_person(one_schedule, day_number, "N")
            people[selected_person_number].schedule = new_schedule

            # usunięcie osoby z listy osób dostępnych
            list_of_free_persons.remove(selected_person_name)

        # DAYS
        # print("DAY")

        number_of_need_days = person_per_day - get_number_of_free_worktype(day_number, people, "D")
        # print("number_of_need_days", number_of_need_days)

        # tworzenie listy ludzi którzy mogą przyjąć dyżur
        list_of_free_persons = get_free_people(day_number, people, "D", no_of_working_days)
        # print("free people", list_of_free_persons)

        for day in range(number_of_need_days):
            selected_person_name = random.choice(list_of_free_persons)    # losowanie osoby
            # print("selected_person_name", selected_person_name)

            # zdobycie numeru wylosowanej osoby w liście people !!!!!!!!!!
            selected_person_number = get_person_number_by_name(selected_person_name, people)
            # print("selected_person_number", selected_person_number)

            # pobranie grafiku
            a_schedule = people[selected_person_number].schedule
            # print(selected_person_name,selected_person_number, a_schedule)

            # wprowadzenie zmiany do grafiku
            new_schedule = input_work_to_person(a_schedule, day_number, "D")
            people[selected_person_number].schedule = new_schedule

            # usunięcie osoby z listy osób dostępnych
            list_of_free_persons.remove(selected_person_name)

        # print("\n PART RESULTS \n")
        # print("  0123456789012345678901234567890")
        # for person in people:
        #     print( person.name, person.schedule)



    print ("\nFINAL SCHEDULE   %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% \n")
    for person in people:
        print( person.name, "  ", person.schedule, "   ", person.get_working_days_number_person)

    return [person.schedule for person in people]








if __name__ == '__main__':

    work = (u"D", u"N", u"U", u".")

    # person_per_day = 4       # liczba osón na dyżurze dziennym
    # person_per_night = 2     # liczba osón na dyżurze nocnym
    number_of_working_days = 21

    schedule_name = "FIRST"
    creation_date = "today"
    month = "january"
    year = 2016
    crew = [u'A', u'B', u'C', u'D', u'E',
            u'F', u'G', u'H', u'I', u'J',
            u'K', u'L', u'M', u'N', u'O']

    schedule = [u'D.........UUUUUU..............N',
                u'.D...........................N.',
                u'..D.........................N..',
                u'...D.................UUUUUUN...',
                u'....D.....................N....',
                u'.....D...................N.....',
                u'......D.................N......',
                u'.......D...............N.......',
                u'........D.............N........',
                u'UUU...UUUUUUU........N.........',
                u'..........D.........N..........',
                u'...........D..UUUUUUUU.........',
                u'............D.....N............',
                u'.............D...N.............',
                u'..............D.N..............']

    first_schedule = Schedule(schedule_name, creation_date, month, year, crew, schedule)

    fill_the_schedule(first_schedule)

