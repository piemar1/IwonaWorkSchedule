# -*- coding: utf-8 -*-

from flask import Flask, render_template, url_for, flash, redirect, request, g
import datetime
import calendar
import webbrowser
from grafik_iwonki_db import SqliteDb


"""
Do dodania i napisania
osobno liczba osób na dyżuże nocnym i dziennym
przykładowo:
nocny 3 osoby
dzienny 4 osoby

przykładowa liczba osób do grafiku 15-16 osób

dodać możliwość urlopu w grafiku:
dopisać U bez możliwośći wstawienia tam dyżuru


pod rząd tylko dwa dyżury:
dozwolone NN, DD
niedozwolone ND, DN

W tygodniu , (ostatnich 7 dniach) dozwolony tylko 4 dyżury

Łączna liczba dyżurów w miesiącu na osobę uzależniona od liczby dni pracujących w miesiącu- tabela od mamy
"""





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
        SqliteDb.__init__(self)
        self.months = [u"styczeń", u"luty", u"marzec", u"kwiecień", u"maj", u"czerweic", u"lipiec",
                       u"sierpień", u"wrzesień", u"październik", u"listopad", u"grudzień"]
        self.dict_week_days = {0: u"pon",
                               1: u"wt",
                               2: u"śr",
                               3: u"czw",
                               4: u"pt",
                               5: u"sob",
                               6: u"niedz"}

        self.years = range(2016, 2020)
        self.team_size = 15
        self.today = datetime.date.today()

        now = datetime.datetime.now()
        self.current_month = self.months[now.month-1]
        self.current_year = now.year
        self.work = (u"D", u"N", u'U', u".")

        self.schedule = []
        self.week_days = []
        self.week_day = None
        self.table_names = None
        self.team_names = None
        self.team = None
        self.days_in_month = None
        self.month_week_days = None

        self.database_check()
        self.read_team_names_db()

    def read_team(self):
        return [self.team_to_edit[0]] + [elem for elem in self.team_to_edit[1].split("###")]

    def read_current_team(self):
        return [request.form['team_name']] + \
               [request.form["person" + str(i)].strip()
                for i in range(self.team_size) if request.form["person" + str(i)]]

    def get_team_size(self):
        return len(self.team)-1

    def create_new_schedule(self):
        self.selected_month = request.form['month']
        self.selected_year = int(request.form['year'])
        self.n = self.months.index(self.selected_month) + 1         # number of selected month

        self.day_no = calendar.monthrange(self.selected_year, self.n)[1]
        self.week_day = calendar.monthrange(self.selected_year, self.n)[0]

        self.week_days = []
        for day in xrange(self.day_no):
            self.week_days.append(self.dict_week_days[self.week_day])
            self.week_day += 1
            if self.week_day == 7:
                self.week_day = 0

        self.month_week_days = zip([elem + 1 for elem in xrange(self.day_no)], self.week_days)

        # print "self.day_no, self.week_day", self.day_no, self.week_day
        # print self.month_week_days

        team_for_new_schedule = request.form["team_for_new_schedule"]
        self.read_one_team_db(team_for_new_schedule)

        self.team = self.read_team()
        self.team_size = self.get_team_size()
        no_of_hours = (x*10 for x in range(15, 22))

    def save_team(self, current_team):

        team_to_save = (current_team[0], "###".join(current_team[1:]))
        print "team_to_save", team_to_save

        if team_to_save[0] in self.team_names:
            self.delete_team(team_to_save[0])

        self.save_team_to_db(team_to_save)
        self.read_team_names_db()

    def edit_team(self):
        team_to_edit = request.form["edit_team"]
        self.read_one_team_db(team_to_edit)

        self.team = self.read_team()
        self.team_size = self.get_team_size()

    def delete_team(self, team_to_delate):
            #
            # Tutaj trzeba koniecznie wprowadzic okno z potwierdzeniem
            # czy na pewno użytkownik chce usunąć daną załogę
            #
            # print "team_to_delate --> ", team_to_delate
            grafik.delete_team_db(team_to_delate)
            grafik.read_team_names_db()


# inicjalizacja strony
@app.route('/')     # Pierwsza strona
def index():
    global grafik
    if not grafik:
        grafik = GrafikIwonki()
    flash(u"Witam w aplikacji do układania grafików pracy.")
    return render_template('Grafik Iwonki.html', months=grafik.months, years=grafik.years,
                           current_month=grafik.current_month, current_year=grafik.current_year,
                           team_names=grafik.team_names)


# Obsługa klawiszy w panelu głównym, inicjalizacja i edycja grafiku oraz załóg
@app.route('/grafik_update', methods=['POST', 'GET'])
def grafik_update():
    global grafik
    if not grafik:
        grafik = GrafikIwonki()

    print "GRAFIK UPDATE !!!!!!!!!!!!!!!!!!!!!!!!!!!!"

    # print "request.form", (request.form)   # drukuje słownik z tekstami z okien

    if request.method == 'POST':

        if request.form["grafik_update"] == u"Stwórz nowy grafik":     # Create new schedule

            grafik.create_new_schedule()
            no_of_hours = (x*10 for x in range(15, 22))
            flash(u"Otworzono okno służące do tworzenia nowego grafiku pracy dla załogi {}"
                  u" - do dzieła!".format(grafik.team[0]))

            return render_template('New_schedule.html',
                                   months          = grafik.months,
                                   years           = grafik.years,
                                   current_month   = grafik.current_month,
                                   current_year    = grafik.current_year,
                                   month_week_days = grafik.month_week_days,
                                   work            = grafik.work,
                                   team_names      = grafik.team_names,
                                   team            = grafik.team,
                                   team_size       = grafik.team_size,
                                   selected_month  = grafik.selected_month,
                                   selected_year   = grafik.selected_year,
                                   no_of_hours     = no_of_hours)

        elif request.form["grafik_update"] == u"Edycja grafiku":     # Edit existed schedule
            pass
        elif request.form["grafik_update"] == u"Usunięcie grafiku":  # Delete existed schedule
            pass

        elif request.form["grafik_update"] == u"Utwórz nową załogę":     # Create new team

            flash(u"Otworzono okno służące do wprowadzenia nowej drużyny do rejestru aplikacji.")
            return render_template('Create_team.html',
                                   size       = grafik.team_size,
                                   today      = grafik.today,
                                   team_names = grafik.team_names,
                                   months     = grafik.months,
                                   years      = grafik.years)

        elif request.form["grafik_update"] == u"Edytuj załogę":          # Edit existed team

            grafik.edit_team()

            flash(u"Otworzono okno służące do edycji załogi '{}'.".format(grafik.team_to_edit[0]))
            return render_template('Create_team.html',
                                   size       = grafik.team_size,
                                   today      = grafik.today,
                                   months     = grafik.months,
                                   years      = grafik.years,
                                   team       = grafik.team,
                                   team_names = grafik.team_names)

        elif request.form["grafik_update"] == u"Usuń załogę":             # Delete /existed team
            team_to_delate = request.form["edit_team"]
            grafik.delete_team(team_to_delate)

            flash(u"Uwaga! Załoga '{}' została usunięta z rejestru aplikacji.".format(team_to_delate))
            return render_template('Grafik Iwonki.html',
                                   months        = grafik.months,
                                   years         = grafik.years,
                                   current_month = grafik.current_month,
                                   current_year  = grafik.current_year,
                                   team_names    = grafik.team_names)


# obsługa klawiszy w oknie z załogą, zapisywanie i edycja
@app.route('/update_team', methods=['POST', 'GET'])
def team_update():
    global grafik
    if not grafik:
        grafik = GrafikIwonki()

    current_team = grafik.read_current_team()
    print "team", current_team

    if request.method == 'POST':
        if request.form["create_team"] == u"dodaj osobę":
            grafik.team_size += 1
            flash(u"Do załogi '{}' dodano nową osobę.".format(current_team[0]))

        elif request.form["create_team"] == u"odejmij osobę":
            grafik.team_size -= 1
            flash(u"Załogę '{}' zmniejszono o jedną osobę.".format(current_team[0]))

        elif request.form["create_team"] == u"Zapisz załogę":

            grafik.save_team(current_team)

            flash(u"Załoga '{}' została dodana do rejestru. "
                  u"Można teraz przystąpić do układania grafiku pracy.".format(current_team[0]))

    return render_template('Create_team.html',
                           size       = grafik.team_size,
                           today      = grafik.today,
                           months     = grafik.months,
                           years      = grafik.years,
                           team       = current_team,
                           team_names = grafik.team_names)


# obsługa klawiszy w oknie z grafikiem, zapisywanie i edycja
@app.route('/schedule_update', methods=['POST', 'GET'])
def schedule_update():
    global grafik
    if not grafik:
        grafik = GrafikIwonki()

    if request.method == 'POST':
        if request.form["save_schedule"] == u"Zapisz Grafik":     # Create new schedule

            print 50 * "#"
            print "team", grafik.team, "day_no", grafik.day_no

            # dane = request.form
            # for elem in dane:
            #      print elem
            # print 50 * "#"

            grafik.schedule = []
            for osoba in grafik.team[1:]:
                one = [osoba, ""]
                for day in xrange(grafik.day_no):
                    one[1] += request.form[osoba + u'_' + str(day + 1)]
                grafik.schedule.append(one)

            print "grafik.schedule", grafik.schedule
            print 50 * "###"
            for elem in grafik.schedule:
                print elem
            print 50 * "###"
            print list(enumerate(grafik.month_week_days))

            #  save_schedule()
            #  Stworzyć stringa do zapisu w db
            #  NazwaSchedule, data, osoba$$$grafik###osoba$$$grafik
            #

            flash(u"Uwaga! Próba zapisania grafiku dla załogi {} o.".format(grafik.team[0]))

            return render_template('New_schedule.html',
                                   months          = grafik.months,
                                   years           = grafik.years,
                                   current_month   = grafik.current_month,
                                   current_year    = grafik.current_year,
                                   work            = grafik.work,
                                   team            = grafik.team,
                                   month_week_days = list(enumerate(grafik.month_week_days)),
                                   schedule        = grafik.schedule)   # przekierowanie do pliku, day_no=month_data[1]


if __name__ == '__main__':
    # webbrowser.open("http://127.0.0.1:5000")
    app.run()

