# -*- coding: utf-8 -*-

from flask import Flask, render_template, url_for, flash, redirect, request, g
import datetime
import calendar
import webbrowser
from grafik_iwonki_db import SqliteDb


DEBUG = True  # configuration
SECRET_KEY = 'l55Vsm2ZJ5q1U518PlxfM5IE2T42oULB'


app = Flask(__name__)
app.config.from_object(__name__)   # wprowadzanie konfiguracja aplikacji z obecnej lokalizacji

# app.logger.addHandler(logging.StreamHandler(sys.stdout))
# app.logger.setLevel(logging.ERsROR)

grafik = None


def u(s):
    return unicode(s, 'utf-8').decode('utf-8')


class GrafikIwonki(SqliteDb, object):
    def __init__(self):
        self.months = [u"styczeń", u"luty", u"marzec", u"kwiecień", u"maj", u"czerweic", u"lipiec",
                       u"sierpień", u"wrzesień", u"październik", u"listopad", u"grudzień"]
        self.years = range(2016, 2020)
        self.team_size = 10
        self.today = datetime.date.today()

        now = datetime.datetime.now()
        self.current_month = self.months[now.month-1]
        self.current_year = now.year
        self.work = [u"D", u"N", u"."]

        self.table_names = None
        self.team_names = None
        self.conn = None
        self.cur = None

        self.database_check()
        self.read_team_names_db()


# inicjalizacja strony
@app.route('/')     # Pierwsza strona
def index():
    global grafik
    grafik = GrafikIwonki()
    flash(u"Witam w aplikacji do układania grafików pracy.")
    return render_template('Grafik Iwonki.html', months=grafik.months, years=grafik.years,
                           current_month=grafik.current_month, current_year=grafik.current_year,
                           team_names=grafik.team_names)


# Obsługa klawiszy w panelu głównym, inicjalizacja i edycja grafiku oraz załóg
@app.route('/grafik_update', methods=['POST', 'GET'])
def grafik_update():
    global grafik
    grafik = GrafikIwonki()
    selected_month = request.form['month']
    selected_year = int(request.form['year'])
    n = grafik.months.index(selected_month) + 1         # number of selected month
    month_data = calendar.monthrange(selected_year, n)

    # print "request.form", (request.form)   # drukuje słownik z tekstami z okien

    if request.method == 'POST':
        if request.form["grafik_update"] == u"Stwórz nowy grafik":     # Create new schedule

            print selected_month, n, selected_year
            print month_data
            flash(u"Otworzono okno służące do tworzenia nowego grafiku pracy - do dzieła!")
            return render_template('New_schedule.html', months=grafik.months, years=grafik.years,
                                   current_month=grafik.current_month, current_year=grafik.current_year,
                                   day_no=month_data[1], work=grafik.work, team_names=grafik.team_names)

        elif request.form["grafik_update"] == u"Edycja grafiku":     # Edit existed schedule
            pass
        elif request.form["grafik_update"] == u"Usunięcie grafiku":  # Delete existed schedule
            pass

        elif request.form["grafik_update"] == u"Utwórz nową załogę":     # Create new team

            flash(u"Otworzono okno służące do wprowadzenia nowej drużyny do rejestru aplikacji.")
            return render_template('Create_team.html', size=grafik.team_size, today=grafik.today,
                                   team_names=grafik.team_names, months=grafik.months, years=grafik.years)

        elif request.form["grafik_update"] == u"Edytuj załogę":          # Edit existed team

            team_to_edit = request.form["edit_team"]
            grafik.read_one_team_db(team_to_edit)

            team = [grafik.team_to_edit[0]] + [elem for elem in grafik.team_to_edit[1].split("###")]
            grafik.team_size = len(team)-1

            print "len(team)", len(team)
            flash(u"Otworzono okno służące do edycji załogi '{}'.".format(grafik.team_to_edit[0]))
            return render_template('Create_team.html', size=grafik.team_size, today=grafik.today,
                                   months=grafik.months, years=grafik.years, team=team, team_names=grafik.team_names)

        elif request.form["grafik_update"] == u"Usuń załogę":             # Delete /existed team
            team_to_delate = request.form["edit_team"]
            #
            # Tutaj trzeba koniecznie wprowadzic okno z potwierdzeniem
            # czy na pewno użytkownik chce usunąć daną załogę
            #
            print "team_to_delate --> ", team_to_delate
            grafik.delete_team(team_to_delate)
            grafik.read_team_names_db()

            flash(u"Uwaga! Załoga '{}' została usunięta z rejestru aplikacji.".format(team_to_delate))
            return render_template('Grafik Iwonki.html', months=grafik.months, years=grafik.years,
                                   current_month=grafik.current_month, current_year=grafik.current_year,
                                   team_names=grafik.team_names)


# obsługa klawiszy w oknie z załogą, zapisywanie i edycja
@app.route('/update_team', methods=['POST', 'GET'])
def team_update():
    global grafik
    if not grafik:
        grafik = GrafikIwonki()

    team = [request.form['team_name']] + \
           [request.form["person" + str(i)] for i in range(grafik.team_size) if request.form["person" + str(i)]]
    team_to_save = (team[0], "###".join(team[1:]))


    print "team", team
    print "team_to_save", team_to_save

    if request.method == 'POST':
        if request.form["create_team"] == u"dodaj osobę":
            grafik.team_size += 1
            flash(u"Do załogi '{}' dodano nową osobę.".format(team[0]))

        elif request.form["create_team"] == u"odejmij osobę":
            grafik.team_size -= 1
            flash(u"Załogę '{}' zmniejszono o jedną osobę.".format(team[0]))

        elif request.form["create_team"] == u"Zapisz załogę":

            if team_to_save[0] in grafik.team_names:
                grafik.delete_team(team_to_save[0])

            grafik.save_team_to_db(team_to_save)
            grafik.read_team_names_db()
            flash(u"Załoga '{}' została dodana do rejestru. "
                  u"Można teraz przystąpić do układania grafiku pracy.".format(team[0]))

    return render_template('Create_team.html', size=grafik.team_size, today=grafik.today,
                           months=grafik.months, years=grafik.years, team=team,
                           team_names=grafik.team_names)


# obsługa klawiszy w oknie z grafikiem, zapisywanie i edycja
@app.route('/schedule_update', methods=['POST', 'GET'])
def schedule_update():
    global grafik
    grafik = GrafikIwonki()
    selected_month = request.form['month']
    selected_year = int(request.form['year'])
    n = grafik.months.index(selected_month) + 1         # number of selected month
    month_data = calendar.monthrange(selected_year, n)

    # print "request.form", (request.form)   # drukuje słownik z tekstami z okien
    # for elem,e in request.form:
    #     print elem, e

    return render_template('New_schedule.html', months=grafik.months, years=grafik.years,
                           current_month=grafik.current_month, current_year=grafik.current_year,
                           day_no=month_data[1], work=grafik.work)   # przekierowanie do pliku


if __name__ == '__main__':
    app.run()
    webbrowser.open("127.0.0.1:5000")