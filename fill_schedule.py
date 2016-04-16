# -*- coding: utf-8 -*-
__author__ = 'marcin'


import random
from models import Person, Schedule


def create_team_for_schedule_filing(schedule):
    """
    Tworzy instancje klas Person w celu uzupełniania grafiku
    """
    crew = schedule.crew
    schedules = schedule.schedule
    return [Person(name, person_schedule) for name, person_schedule in zip(crew, schedules)]


def get_number_of_free_worktype(day_number, people, work):
    """
    Zwraca liczbę osób z obsadzonymi dyżurami dla danego dnia i rodzaju dyżuru
    """
    number = 0
    for person in people:
        if person.schedule[day_number] == work:
            number += 1
    return number


def get_person_number_by_name(name, people):
    """
    Zwraca instancję Person z listy People wedłóg nadanego atrybutu name.
    """
    for no, person in enumerate(people):
        if person.name == name:
            return no


def get_free_people(day_number, people, work, no_of_working_days):
    """
    Zwraca listę osób (w postaci atrybutów person.name), które moga przyjąć dyżur -
    Tutaj muszą być wszystkie filtry
    - osoba bez dyżuru
    - 2 dyżury pod rząd, 24h
    - liczba dyżurów w tygodniu
    - liczba dyżurów w miesiącu
    """

    # tworzenie tymczasowych insyancji Person - tylko w celu wypełniania grafiku
    people_for_one_day = [Person(person.name, person.schedule) for person in people]

    # filtrowanie osób, które mają wolny dzień
    people_free_day = [person for person in people_for_one_day if person.wheather_day_is_free(day_number)]

    # uzupełnienie grafiku o przykładowy dzień pracy - wedłóg day_number i work
    people_filled_example_work = []
    for person in people_free_day:
        person.take_work(day_number, work)       #  wprowadzanie zmian w grafiku
        people_filled_example_work.append(person)

    return [person.name for person in people_filled_example_work if
            person.filtre_double_work() and
            person.filtre_work_days_in_week(4) and
            person.filtre_work_days_in_month(no_of_working_days)]


def fill_the_schedule(schedule, no_of_working_days, person_per_day, person_per_night):

    month_lenght = len(schedule.schedule[0])
    people = create_team_for_schedule_filing(schedule)   # lista osób w postaci instancji Person

    for day_number in range(month_lenght):

        # NIGHTS

        # liczba osób potrzebnych
        number_of_need_night = person_per_night - get_number_of_free_worktype(day_number, people, "N")

        # tworzenie listy ludzi którzy mogą przyjąć dyżur    Wszystkie FILTRY !!!!!!!
        list_of_free_persons = get_free_people(day_number, people, "N", no_of_working_days)

        for night in range(number_of_need_night):

            # losowanie osoby
            selected_person_name = random.choice(list_of_free_persons)

            # zdobycie numeru wylosowanej osoby w liście people
            selected_person_number = get_person_number_by_name(selected_person_name, people)
            # print("selected_person_number", selected_person_number)

            # wprowadzenie zmiany do grafiku
            people[selected_person_number].take_work(day_number, "N")

            # usunięcie osoby z listy osób dostępnych
            list_of_free_persons.remove(selected_person_name)

        # DAYS

        # liczba osób potrzebnych
        number_of_need_days = person_per_day - get_number_of_free_worktype(day_number, people, "D")

        # tworzenie listy ludzi którzy mogą przyjąć dyżur
        list_of_free_persons = get_free_people(day_number, people, "D", no_of_working_days)

        for day in range(number_of_need_days):
            selected_person_name = random.choice(list_of_free_persons)    # losowanie osoby

            # zdobycie numeru wylosowanej osoby w liście people
            selected_person_number = get_person_number_by_name(selected_person_name, people)

            # wprowadzenie zmiany do grafiku
            people[selected_person_number].take_work(day_number, "D")

            # usunięcie osoby z listy osób dostępnych
            list_of_free_persons.remove(selected_person_name)

    return [person.schedule for person in people]


if __name__ == '__main__':

    work = (u"D", u"N", u"U", u".")

    person_per_day = 4       # liczba osón na dyżurze dziennym
    person_per_night = 2     # liczba osón na dyżurze nocnym
    number_of_working_days = 14

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

    filled_schedule = fill_the_schedule(first_schedule, number_of_working_days, person_per_day, person_per_night)

    for elem in filled_schedule:
        print(elem)