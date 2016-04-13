# -*- coding: utf-8 -*-
#!/usr/bin/python
__author__ = 'Marcin Pieczyński'

from flask import Flask, render_template, url_for, flash, redirect, request, g, session
import datetime
import calendar
import webbrowser
from models import Team, Schedule
from database import *


MONTHS = [u"styczeń", u"luty", u"marzec", u"kwiecień", u"maj", u"czerwiec", u"lipiec",
          u"sierpień", u"wrzesień", u"październik", u"listopad", u"grudzień"]

YEARS = range(2016, 2020)
WORK = (u"D", u"N", u'U', u".")
TYPE_OF_WORK = (u"D", u"N")

NIGHT = u"N"
DAY = u"D"
FREE = u"."

TODAY = datetime.date.today()
NOW = datetime.datetime.now()

CURRENT_MONTH = MONTHS[NOW.month-1]
CURRENT_YEAR = NOW.year

WORKING_DAYS = (u"pon", u"wt", u"śr", u"czw", u"pt")

WEEK_DAYS = {0: u"pon",
             1: u"wt",
             2: u"śr",
             3: u"czw",
             4: u"pt",
             5: u"sob",
             6: u"niedz"}

WORKING_DAYS_NUMBER_TEXT = {10: "6 x dyżur 12h + 3h 50'",
                            11: "6 x dyżur 12h + 11h 25'",
                            12: "7 x dyżur 12h + 7h 0'",
                            13: "8 x dyżur 12h + 2h 35'",
                            14: "8 x dyżur 12h + 10h 10'",
                            15: "9 x dyżur 12h + 5h 45'",
                            16: "10 x dyżur 12h + 1h 20'",
                            17: "10 x dyżur 12h + 8h 55'",
                            18: "11 x dyżur 12h + 4h 30'",
                            19: "12 x dyżur 12h + 0h 05'",
                            20: "12 x dyżur 12h + 7h 40'",
                            21: "13 x dyżur 12h + 3h 15'",
                            22: "13 x dyżur 12h + 10h 50'",
                            23: "14 x dyżur 12h + 6h 25'",
                            24: "15 x dyżur 12h + 2h 0'"}

WORKING_DAYS_NUMBERS = {10: 6,
                        11: 6,
                        12: 7,
                        13: 8,
                        14: 8,
                        15: 9,
                        16: 10,
                        17: 10,
                        18: 11,
                        19: 12,
                        20: 12,
                        21: 13,
                        22: 13,
                        23: 14,
                        24: 15}

DEBUG = True  # configuration
SECRET_KEY = 'l55Vsm2ZJ5q1U518PlxfM5IE2T42oULB'

app = Flask(__name__)
app.config.from_object(__name__)   # wprowadzanie konfiguracja aplikacji z obecnej lokalizacji

"""
przekazywanie między widikami obiektów w url, np przekazywanie id z bazy danych  !!!!!!!!!!!!!!!!!1
"""


def read_current_team():
    """
    Funkcja odczytuje dane wprowadzone na stronie dla team  i zwraca instancję Team
    """
    team_name = request.form['team_name']
    creation_date = TODAY
    crew = []
    no = 0
    while 1:
        try:
            person = request.form["person" + str(no)].strip()
            crew.append(person)
            no += 1
        except KeyError:
            break

    team = Team(team_name, creation_date, crew)
    return team


def read_current_schedule():
    """
    Funkcja odczytuje dane wprowadzone na stronie dla schedule i zwraca instancję Schedule
    """
    schedule = []
    month_calendar = session["month_calendar"]
    crew = session["team_crew"]
    selected_month = session["selected_month"]
    selected_year = session["selected_year"]

    schedule_name = request.form["schedule_name"]

    for person in crew:
        person_schedule = []
        for no, day in month_calendar:
            one_day = request.form[person + u'_day' + str(no)]
            person_schedule.append(one_day)
        schedule.append("".join(person_schedule))

    schedule = Schedule(schedule_name, TODAY, selected_month,
                        selected_year, crew, schedule)
    return schedule


def get_number_of_working_days_month(month_week_days):
    number = 0
    for no, day in month_week_days:
        if day in WORKING_DAYS:
            number += 1
    return number


def get_month_calendar(selected_year, selected_month):

    """
    Funkcja zwraca listę z planem miesiąca, zawierającą informację o liczbie dni
    oraz poszczególnych dniach tygodniach.
    """
    n = MONTHS.index(selected_month) + 1
    week_day, day_no = calendar.monthrange(selected_year, n)

    week_days = []
    for day in range(day_no):
        week_days.append(WEEK_DAYS[week_day])
        week_day += 1
        if week_day == 7:
            week_day = 0

    month_week_days = list(zip([elem + 1 for elem in range(day_no)], week_days))

    return month_week_days


def get_number_of_working_days(month_calendar):
    """
    Funkcja zwraca liczbą dnia pracujących w wybranym miesiącu.
    """
    number = 0
    for day_number, day in month_calendar:
        if day in WORKING_DAYS:
            number += 1
    return number


# inicjalizacja strony
@app.route('/')     # Pierwsza strona
def index():
    flash(u"Witam w aplikacji do układania grafików pracy.")
    return render_template('Grafik Iwonki.html',
                           months        = MONTHS,
                           years         = YEARS,
                           current_month = CURRENT_MONTH,
                           current_year  = CURRENT_YEAR,
                           team_names    = get_team_names_from_db(),
                           schedule_names= get_schedule_names_from_db())


# Obsługa klawiszy w panelu głównym, inicjalizacja i edycja grafiku oraz załóg
@app.route('/grafik_update', methods=['POST', 'GET'])
def grafik_update():

    if request.method == 'POST':

        if request.form["grafik_update"] == u"Utwórz nową załogę":     # Create new team

            flash(u"Otworzono okno służące do wprowadzenia nowej drużyny do rejestru aplikacji.")
            return render_template('Create_team.html',
                                   size       = 15,
                                   today      = TODAY,
                                   team_names = get_team_names_from_db(),
                                   schedule_names= get_schedule_names_from_db(),
                                   current_month = CURRENT_MONTH,
                                   current_year  = CURRENT_YEAR,
                                   months     = MONTHS,
                                   years      = YEARS)

        elif request.form["grafik_update"] == u"Edytuj załogę":          # Edit existed team

            team_to_be_edit = request.form["edit_team"]
            team = get_team_from_db(team_to_be_edit)

            flash(u"Otworzono okno służące do edycji załogi '{}'.".format(team.team_name))
            return render_template('Existing_team.html',
                                   team_names    = get_team_names_from_db(),
                                   schedule_names= get_schedule_names_from_db(),
                                   months        = MONTHS,
                                   years         = YEARS,
                                   today         = TODAY,
                                   current_month = CURRENT_MONTH,
                                   current_year  = CURRENT_YEAR,
                                   team          = team,
                                   size          = len(team.crew))

        elif request.form["grafik_update"] == u"Usuń załogę":             # Delete /existed team
            # pytanie z oknem czy na pewno JS

            team_to_delate = request.form["edit_team"]
            delete_team_in_db(team_to_delate)

            flash(u"Uwaga! Załoga '{}' została usunięta z rejestru aplikacji.".format(team_to_delate))
            return render_template('Grafik Iwonki.html',
                                   months        = MONTHS,
                                   years         = YEARS,
                                   current_month = CURRENT_MONTH,
                                   current_year  = CURRENT_YEAR,
                                   team_names    = get_team_names_from_db(),
                                   schedule_names= get_schedule_names_from_db())


        elif request.form["grafik_update"] == u"Stwórz nowy grafik":     # Create new schedule

            selected_month = request.form['month']
            selected_year = int(request.form['year'])

            team_name_for_new_schedule = request.form["team_for_new_schedule"]
            team = get_team_from_db(team_name_for_new_schedule)

            month_calendar = get_month_calendar(selected_year, selected_month)

            session["selected_month"] = selected_month
            session["selected_year"] = selected_year
            session["team_crew"] = team.crew
            session["month_calendar"] = month_calendar

            return render_template('Create_schedule.html',
                                   months         = MONTHS,
                                   years          = YEARS,
                                   current_month  = CURRENT_MONTH,
                                   current_year   = CURRENT_YEAR,
                                   selected_month = selected_month,
                                   selected_year  = selected_year,
                                   month_calendar = month_calendar, # plan miesiąca
                                   work           = WORK,
                                   today          = TODAY,
                                   team_names     = get_team_names_from_db(),
                                   schedule_names= get_schedule_names_from_db(),
                                   team           = team,
                                   workin_days    = WORKING_DAYS_NUMBER_TEXT[get_number_of_working_days(month_calendar)])

        elif request.form["grafik_update"] == u"Edycja grafiku":     # Edit existed schedule

            schedule_to_edit = request.form["schedule_to_edit"]
            schedule = get_schedule_from_db(schedule_to_edit)

            month_calendar = get_month_calendar(schedule.year, schedule.month)

            session["selected_month"] = schedule.month
            session["selected_year"] = schedule.year
            session["team_crew"] = schedule.crew
            session["month_calendar"] = month_calendar

            flash(u"Edycja grafiku pracy {}.".format(schedule.schedule_name))

            return render_template('Existing_schedule.html',
                                   months         = MONTHS,
                                   years          = YEARS,
                                   current_month  = CURRENT_MONTH,
                                   current_year   = CURRENT_YEAR,
                                   month_calendar = month_calendar, # plan miesiąca
                                   work           = WORK,
                                   team_names     = get_team_names_from_db(),
                                   schedule_names= get_schedule_names_from_db(),
                                   schedule       = schedule,
                                   person_schedules = list(zip(schedule.crew, schedule.schedule)),
                                   workin_days    = WORKING_DAYS_NUMBER_TEXT[get_number_of_working_days(month_calendar)])

        elif request.form["grafik_update"] == u"Usunięcie grafiku":  # Delete existed schedule
            # pytanie z oknem czy na pewno JS
            schedule_to_delate = request.form["schedule_to_edit"]
            delete_schedule_in_db(schedule_to_delate)

            flash(u"Uwaga! Grafik '{}' został usunięty z rejestru aplikacji.".format(schedule_to_delate))
            return render_template('Grafik Iwonki.html',
                                   months        = MONTHS,
                                   years         = YEARS,
                                   current_month = CURRENT_MONTH,
                                   current_year  = CURRENT_YEAR,
                                   team_names    = get_team_names_from_db(),
                                   schedule_names= get_schedule_names_from_db())


# obsługa klawiszy w oknie z załogą, zapisywanie i edycja
@app.route('/update_team', methods=['POST', 'GET'])
def team_update():

    team_size = 15

    if request.method == 'POST':

        # if request.form["create_team"] == u"dodaj osobę":
        #     team_size += 1
        #     flash(u"Do załogi '{}' dodano nową osobę.".format(team.team_name))
        #
        # elif request.form["create_team"] == u"odejmij osobę":
        #     team_size -= 1
        #     flash(u"Załogę '{}' zmniejszono o jedną osobę.".format(team.team_name))

        if request.form["create_team"] == u"Zapisz załogę":
            team = read_current_team()
            save_team_to_db(team)

            return render_template('Existing_team.html',
                                   team_names = get_team_names_from_db(),
                                   months     = MONTHS,
                                   years      = YEARS,
                                   current_month = CURRENT_MONTH,
                                   current_year  = CURRENT_YEAR,
                                   today      = TODAY,
                                   team       = team,
                                   size       = len(team.crew))


# obsługa klawiszy w oknie z grafikiem, zapisywanie i edycja
@app.route('/schedule_update', methods=['POST', 'GET'])
def schedule_update():
    if request.method == 'POST':

        # odczytanie wprowadzonych danych dla schedule i zrobienie z tego instancji
        schedule = read_current_schedule()

        month_calendar = get_month_calendar(schedule.year, schedule.month)

        if request.form["save_schedule"] == u"Zapisz Grafik":     # Create new schedule

            save_schedule_to_db(schedule)

            flash(u"Dokonano zapisu grafiku pracy {} w bazie danyc.".format(schedule.schedule_name))

            return render_template('Existing_schedule.html',
                                   months         = MONTHS,
                                   years          = YEARS,
                                   current_month  = CURRENT_MONTH,
                                   current_year   = CURRENT_YEAR,
                                   month_calendar = month_calendar, # plan miesiąca
                                   work           = WORK,
                                   team_names     = get_team_names_from_db(),
                                   schedule_names= get_schedule_names_from_db(),
                                   schedule       = schedule,
                                   person_schedules = list(zip(schedule.crew, schedule.schedule)))


        if request.form["save_schedule"] == u"Uzupełnij Grafik Automatycznie !":     # Create new schedule

            print("START")
            person_per_day = int(request.form["no_of_person_day"])      # liczba osón na dyżurze dziennym
            person_per_night = int(request.form["no_of_person_night"])  # liczba osón na dyżurze nocnym

            no_of_working_days = get_number_of_working_days_month(month_calendar)



            print("przed IMPORTEM")
            from fill_schedule import fill_the_schedule
            print("PO IMPORTEM")

            number_of_tries = 10
            while number_of_tries:
                try:
                    schedule.schedule = fill_the_schedule(schedule,
                                                          no_of_working_days,
                                                          person_per_day,
                                                          person_per_night)

                    flash(u"Dokonano automatycznego uzupełnienia grafiku {}.".format(schedule.schedule_name))

                    return render_template('Existing_schedule.html',
                                           months         = MONTHS,
                                           years          = YEARS,
                                           current_month  = CURRENT_MONTH,
                                           current_year   = CURRENT_YEAR,
                                           month_calendar = month_calendar, # plan miesiąca
                                           work           = WORK,
                                           team_names     = get_team_names_from_db(),
                                           schedule_names= get_schedule_names_from_db(),
                                           schedule       = schedule,
                                           person_schedules = list(zip(schedule.crew, schedule.schedule)))

                except IndexError:
                    flash(u"Atomatyczne uzupełnienie grafiku {} nie powiodło się.".format(schedule.schedule_name))
                number_of_tries -= 1












if __name__ == '__main__':
    # webbrowser.open("http://127.0.0.1:5000")
    app.run()