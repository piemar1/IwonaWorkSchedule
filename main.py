# -*- coding: utf-8 -*-
#!/usr/bin/python
__author__ = 'Marcin Pieczyński'

from flask import Flask, render_template, flash, redirect, request, session, Response, url_for
from sqlalchemy_db import *
from models import Team, Schedule

import io
import datetime
import calendar
import webbrowser
import threading

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

WORKING_DAYS = (u"pn", u"wt", u"śr", u"cz", u"pt")

WEEK_DAYS = {0: u"pn",
             1: u"wt",
             2: u"śr",
             3: u"cz",
             4: u"pt",
             5: u"so",
             6: u"n"}

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

WORKING_DAYS_NUMBERS = {10: 7,
                        11: 7,
                        12: 8,
                        13: 9,
                        14: 9,
                        15: 10,
                        16: 11,
                        17: 11,
                        18: 12,
                        19: 13,
                        20: 13,
                        21: 14,
                        22: 14,
                        23: 15,
                        24: 16}
TEAM_SIZE = 15

SECRET_KEY = 'l55Vsm2ZJ5q1U518PlxfM5IE2T42oULB'
UPLOAD_FOLDER = '/uploads/'
ALLOWED_EXTENSIONS = set("pdf")

app = Flask(__name__)
app.config.from_object(__name__)   # wprowadzanie konfiguracja aplikacji z obecnej lokalizacji


def read_current_team(remove_empty=False):
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
            if remove_empty and not person:
                pass
            else:
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
    """
    Funckcja zwraca liczbę dni roboczych w danym miesiącu
    """
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
    flash(u"Witam w aplikacji GafikIwonki do układania grafików pracy.")
    return redirect(url_for('main_page'))


@app.route('/GrafikIwonki', methods=['GET', 'POST'])     # Pierwsza strona
def main_page():
    return render_template('Grafik Iwonki.html',
                           months        = MONTHS,
                           years         = YEARS,
                           current_month = CURRENT_MONTH,
                           current_year  = CURRENT_YEAR,
                           team_names    = get_team_names_from_db(),
                           schedule_names= get_schedule_names_from_db())


@app.route('/Team/<team_name>', methods=['GET', 'POST'])     # Strona z zapisanymi drużynami
def existing_team(team_name=None):

    team_name = session["team_name"]
    crew = session["team_crew"]

    return render_template('Existing_team.html',
                           team_names    = get_team_names_from_db(),
                           schedule_names= get_schedule_names_from_db(),
                           months        = MONTHS,
                           years         = YEARS,
                           today         = TODAY,
                           current_month = CURRENT_MONTH,
                           current_year  = CURRENT_YEAR,
                           team_name     = team_name,
                           crew          = crew,
                           size          = len(crew))

@app.route('/Schedule/<schedule_name>', methods=['GET', 'POST'])     # Strona z zapisanymi grafikami
def existing_schedule(schedule_name=None):

    schedule_crew = session["team_crew"]
    month_calendar = session["month_calendar"]
    schedule_schedule = session["schedule_schedule"]
    schedule_name = session["schedule_name"]

    return render_template('Existing_schedule.html',
                           months         = MONTHS,
                           years          = YEARS,
                           current_month  = CURRENT_MONTH,
                           current_year   = CURRENT_YEAR,
                           month_calendar = month_calendar, # plan miesiąca
                           work           = WORK,
                           team_names     = get_team_names_from_db(),
                           schedule_names = get_schedule_names_from_db(),
                           schedule_name = schedule_name,
                           working_days   = WORKING_DAYS_NUMBER_TEXT[get_number_of_working_days(month_calendar)],
                           no_of_daywork  = WORKING_DAYS_NUMBERS[get_number_of_working_days_month(month_calendar)],
                           WORKING_DAYS_NUMBER_TEXT = WORKING_DAYS_NUMBER_TEXT.values(),
                           WORKING_DAYS_NUMBERS     = WORKING_DAYS_NUMBERS.values(),
                           person_schedules         = list(zip(schedule_crew, schedule_schedule)))


# Obsługa klawiszy w panelu głównym, inicjalizacja i edycja grafiku oraz załóg
@app.route('/grafik_update', methods=['POST', 'GET'])
def grafik_update():

    if request.method == 'POST':

        if request.form["grafik_update"] == u"Utwórz nową załogę":     # Create new team

            flash(u"Otworzono okno służące do utworzenia nowego zespołu.")
            return render_template('Create_team.html',
                                   size       = TEAM_SIZE,
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

            session["team_name"] = team.team_name
            session["team_crew"] = team.crew

            flash(u"Otworzono okno służące do edycji załogi '{}'.".format(team.team_name))
            return redirect(url_for('existing_team', team_name=team.team_name))

        elif request.form["grafik_update"] == u"Usuń załogę":             # Delete /existed team

            team_to_delate = request.form["edit_team"]
            delete_team_in_db(team_to_delate)

            flash(u"Uwaga! Załoga '{}' została usunięta z rejestru aplikacji.".format(team_to_delate))
            return redirect(url_for('main_page'))

        elif request.form["grafik_update"] == u"Stwórz nowy grafik":     # Create new schedule

            selected_month = request.form['month']
            selected_year = int(request.form['year'])

            team_name_for_new_schedule = request.form["team_for_new_schedule"]
            team = get_team_from_db(team_name_for_new_schedule)

            month_calendar = get_month_calendar(selected_year, selected_month)
            no_of_daywork = WORKING_DAYS_NUMBERS[get_number_of_working_days_month(month_calendar)]

            session["team_crew"] = team.crew
            session["month_calendar"] = month_calendar
            session["selected_month"] = selected_month
            session["selected_year"] = selected_year

            flash(u"Czas przystąpić do układania grafiku dla załogi '{}' dla miesiąca {} {}.".format(team.team_name,
                                                                                                  selected_month,
                                                                                                  selected_year))

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
                                   schedule_names = get_schedule_names_from_db(),
                                   team           = team,
                                   working_days   = WORKING_DAYS_NUMBER_TEXT[get_number_of_working_days(month_calendar)],
                                   WORKING_DAYS_NUMBER_TEXT = WORKING_DAYS_NUMBER_TEXT.values(),
                                   no_of_daywork = no_of_daywork,
                                   WORKING_DAYS_NUMBERS = WORKING_DAYS_NUMBERS.values())

        elif request.form["grafik_update"] == u"Edycja grafiku":     # Edit existed schedule

            schedule_to_edit = request.form["schedule_to_edit"]
            schedule = get_schedule_from_db(schedule_to_edit)

            if not schedule:
                flash(u"Brak możliwości wyświetlenia grafiku o nazwie '{}'. "
                      u"Przyczyną jest brak żądanej drużyny w bazie danych.".format(schedule_to_edit))
                return redirect(url_for('main_page'))

            month_calendar = get_month_calendar(schedule.year, schedule.month)
            no_of_daywork = WORKING_DAYS_NUMBERS[get_number_of_working_days_month(month_calendar)]

            session["selected_month"] = schedule.month
            session["selected_year"] = schedule.year
            session["team_crew"] = schedule.crew
            session["month_calendar"] = month_calendar
            session["schedule_schedule"] = schedule.schedule
            session["schedule_name"] = schedule.schedule_name

            flash(u"Edycja grafiku pracy '{}' stworzonego dla miesiąca {} {}.".format(schedule.schedule_name,
                                                                                      schedule.month,
                                                                                      schedule.year))

            return redirect(url_for('existing_schedule', schedule_name=schedule.schedule_name))

        elif request.form["grafik_update"] == u"Usunięcie grafiku":  # Delete existed schedule
            schedule_to_delate = request.form["schedule_to_edit"]

            delete_schedule_in_db(schedule_to_delate)

            flash(u"Uwaga! Grafik '{}' został usunięty z rejestru aplikacji.".format(schedule_to_delate))
            return redirect(url_for('main_page'))


# obsługa klawiszy w oknie z załogą, zapisywanie i edycja
@app.route('/team_update', methods=['POST', 'GET'])
def team_update():

    team = read_current_team()

    if request.method == 'POST':

        if request.form["create_team"] == u"dodaj osobę":
            team.crew.append("")
            flash(u"Do załogi '{}' dodano nową osobę.".format(team.team_name))

        elif request.form["create_team"] == u"odejmij osobę":
            team.crew.pop()
            flash(u"Załogę '{}' zmniejszono o jedną osobę.".format(team.team_name))

        elif request.form["create_team"] == u"Zapisz załogę":
            team = read_current_team(remove_empty=True)
            save_team_to_db(team)
            flash(u"Załoga '{}' została zapisana do bazy danych.".format(team.team_name))

        session["team_name"] = team.team_name
        session["team_crew"] = team.crew
        return redirect(url_for('existing_team', team_name=team.team_name))


# obsługa klawiszy w oknie z grafikiem, zapisywanie i edycja
@app.route('/schedule_update', methods=['POST', 'GET'])
def schedule_update():

    if request.method == 'POST':

        # odczytanie wprowadzonych danych dla schedule i zrobienie z tego instancji
        schedule = read_current_schedule()
        month_calendar = get_month_calendar(schedule.year, schedule.month)

        # month_working_days, no_of_workdays)
        no_of_daywork = WORKING_DAYS_NUMBERS[get_number_of_working_days_month(month_calendar)]

        month_working_days = request.form["no_of_working_days_in_nonth"]
        no_of_workdays = request.form["no_of_working_days_per_person"]

        session["team_crew"] = schedule.crew
        session["month_calendar"] = month_calendar
        session["schedule_schedule"] = schedule.schedule
        session["schedule_name"] = schedule.schedule_name

        if request.form["save_schedule"] == u"Zapisz Grafik w bazie danych":     # Create new schedule

            save_schedule_to_db(schedule)
            flash(u"Dokonano zapisu grafiku pracy {} w bazie danyc.".format(schedule.schedule_name))

            return redirect(url_for('existing_schedule', schedule_name=schedule.schedule_name))

        elif request.form["save_schedule"] == u"Zapisz w formacie PDF":

            from write_pdf import WritePDF

            buffor = io.BytesIO()
            pdf_buffor = WritePDF(buffor, schedule, month_calendar, month_working_days, no_of_workdays)
            pdf_buffor.run()                                    #  tu jest błąd  i jest kwestia buffor
            pdf = buffor.getvalue()
            # print("PDF CREATED !!!!")

            return Response(pdf,
                            mimetype='application/pdf',
                            headers={'Content-Disposition':u'attachment;filename=grafik.pdf'})
                            # BRAk polskich liter w nazwie pliku!!!!!

        elif request.form["save_schedule"] == u"Uzupełnij Grafik Automatycznie !":     # Create new schedule

            # print("START")
            person_per_day = int(request.form["no_of_person_day"])      # liczba osón na dyżurze dziennym
            person_per_night = int(request.form["no_of_person_night"])  # liczba osón na dyżurze nocnym
            no_of_daywork = WORKING_DAYS_NUMBERS[get_number_of_working_days_month(month_calendar)]

            from fill_schedule import fill_the_schedule

            number_of_tries = 10
            while number_of_tries:
                try:
                    schedule.schedule = fill_the_schedule(schedule,
                                                          no_of_daywork,
                                                          person_per_day,
                                                          person_per_night)

                    session["team_crew"] = schedule.crew
                    session["month_calendar"] = month_calendar
                    session["schedule_schedule"] = schedule.schedule
                    session["schedule_name"] = schedule.schedule_name

                    flash(u"Dokonano automatycznego uzupełnienia grafiku {}.".format(schedule.schedule_name))
                    return redirect(url_for('existing_schedule', schedule_name=schedule.schedule_name))

                except IndexError:
                    number_of_tries -= 1

            session["team_crew"] = schedule.crew
            session["month_calendar"] = month_calendar
            session["schedule_schedule"] = schedule.schedule
            session["schedule_name"] = schedule.schedule_name

            flash(u"Atomatyczne uzupełnienie grafiku {} nie powiodło się !!! ;-(\n"
                  u"Zalecamy zmianę parametrów automatycznego uzupełniania grafiku "
                  u"na mniej wymagające.".format(schedule.schedule_name))

            return redirect(url_for('existing_schedule', schedule_name=schedule.schedule_name))


# @app.route('/uploads/<filename>/')
# def uploaded_file(filename):
#
#     # 1   DZIAŁA
#     # return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
#
#     # 2   DZIAŁA
#     # print(help(send_from_directory))   otwiera plik w przeglądarce
#     # return send_from_directory("/home/marcin/Pulpit/MyProjectGitHub/robocze/", "grafik.pdf")
#
#     # 3   DZIAŁA          umożliwia ściągnięcie pliku na dysk albo otwarcie
#     # resp = make_response(open("/home/marcin/Pulpit/MyProjectGitHub/robocze/grafik.pdf", "rb").read())
#     # resp.content_type = "document/pdf"
#     # return resp
#
#
#     # 4   DZIAŁA          umożliwia ściągnięcie pliku na dysk albo otwarcie
#     # response = Response(mimetype='application/pdf')
#     # response.
#
#     resp = make_response(open(filename, "rb").read())
#     # resp = make_response(filename)
#
#
#     resp.content_type = "document/pdf"
#     return resp


if __name__ == '__main__':

    app.debug = False
    app.run()

    # Below code works ONLY if app.debug = False and have to be used in production

    # def start_app():
    #     app.debug = False
    #     app.run()
    #
    # def open_webbroser():
    #     webbrowser.open("http://127.0.0.1:5000")
    #
    # try:
    #     one = threading.Thread(target=start_app)
    #     one.start()
    #     second = threading.Thread(target=open_webbroser)
    #     second.start()
    # except:
    #     print("Error")





