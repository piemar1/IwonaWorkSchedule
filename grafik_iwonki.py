# -*- coding: utf-8 -*-

# import random
# import string
# import sys
# import logging
# import urllib2

from flask import Flask, render_template, url_for, flash, redirect, request, g
import datetime
import calendar
import webbrowser
import sqlite3
from contextlib import closing


DEBUG = True  # configuration
SECRET_KEY = 'l55Vsm2ZJ5q1U518PlxfM5IE2T42oULB'
DATABASE = "database.db"

app = Flask(__name__)
app.config.from_object(__name__)   # wprowadzanie konfiguracja aplikacji z obecnej lokalizacji

# app.logger.addHandler(logging.StreamHandler(sys.stdout))
# app.logger.setLevel(logging.ERsROR)

grafik = None


def u(s):
    return unicode(s, 'utf-8').decode('utf-8')


def get_db():
    """ Connecting to the databese."""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        print "Connect to DB \n"
    return db


@app.teardown_appcontext
def close_connection(exception):
    """ Closing connection to database"""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


class GrafikIwonki(object):
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
        self.teams = None
        self.con = None
        self.cur = None

        self.database_check()
        self.save_team_to_db((u'2016-02-01', u'2016-02-01'))
        self.read_from_db()

    def database_check(self):
        self.con = sqlite3.connect(DATABASE)
        with self.con:
            self.cur = self.con.cursor()

            self.cur.execute("SELECT name FROM sqlite_master WHERE type = 'table';")
            self.table_names = [elem[0] for elem in self.cur.fetchall()]

            print "self.table_names", type(self.table_names), self.table_names

            if "TEAM" not in self.table_names:
                self.cur.execute("CREATE TABLE TEAM (team_name TEXT, team TEXT)")

            if "SCHEDULES" not in self.table_names:
                self.cur.execute("CREATE TABLE SCHEDULES (date TEXT, team_name TEXT, schedule TEXT)")

            print "self.cur.fetchall() -->", self.cur.fetchall(), len(self.cur.fetchall())
        self.con.close()

    def save_team_to_db(self, team_to_save):

        team_to_save = (u'2016-02-01', u'2016-02-01')

        self.con = sqlite3.connect(DATABASE)
        with self.con:
            self.cur = self.con.cursor()
            self.cur.executemany("INSERT INTO TEAM VALUES(?, ?)", (team_to_save,))
            print "ZAPISANO TEAM W DB!!!!!!!!!!!"
        self.con.close()

    def read_from_db(self):
        self.con = sqlite3.connect(DATABASE)
        with self.con:
            self.cur = self.con.cursor()

            self.cur.execute("SELECT * FROM TEAM")
            rows = self.cur.fetchall()
            print len(rows)
            for row in rows:
                print row
            print "powyżej powinna być baza danych"
        self.con.close()


# inicjalizacja strony
@app.route('/')     # Pierwsza strona
def index():
    global grafik
    grafik = GrafikIwonki()

    return render_template('Grafik Iwonki.html', months=grafik.months, years=grafik.years,
                           current_month=grafik.current_month, current_year=grafik.current_year)


# Obsługa klawiszy w głównym oknie, inicjalizacja i edycja grafiku oraz załóg
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
        if request.form["grafik_update"] == u"Stwórz nowy grafik":
            print selected_month, n, selected_year
            print month_data
            return render_template('New_schedule.html', months=grafik.months, years=grafik.years,
                                   current_month=grafik.current_month, current_year=grafik.current_year,
                                   day_no=month_data[1], work=grafik.work)
        elif request.form["grafik_update"] == u"Edycja grafiku":
            pass
        elif request.form["grafik_update"] == u"Usunięcie grafiku":
            pass

        elif request.form["grafik_update"] == u"Utwórz nową załogę":
            return render_template('Create_team.html', size=grafik.team_size, today=grafik.today,
                                   months=grafik.months, years=grafik.years,)

        elif request.form["grafik_update"] == u"Edytuj załogę":
            pass
        elif request.form["grafik_update"] == u"Usuń załogę":
            pass


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


# obsługa klawiszy w oknie z załogą, zapisywanie i edycja
@app.route('/update_team', methods=['POST', 'GET'])
def team_update():
    global grafik
    if not grafik:
        grafik = GrafikIwonki()

    team = [request.form['team_name']] + [request.form["person" + str(i)] for i in range(grafik.team_size)]
    team_to_save = (team[0], "###".join(team[1:]))

    print "team", team
    print "team_to_save", team_to_save

    if request.method == 'POST':
        if request.form["create_team"] == u"dodaj osobę":
            grafik.team_size += 1
        elif request.form["create_team"] == u"odejmij osobę":
            grafik.team_size -= 1
        elif request.form["create_team"] == u"Zapisz załogę":
            grafik.save_team_to_db(team_to_save)

    return render_template('Create_team.html', size=grafik.team_size, today=grafik.today,
                           months=grafik.months, years=grafik.years, team=team)






if __name__ == '__main__':
    app.run()
    webbrowser.open("127.0.0.1:5000")