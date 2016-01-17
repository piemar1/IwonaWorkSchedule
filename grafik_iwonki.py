# -*- coding: utf-8 -*-

import random
import string
import sys
import logging
from flask import Flask, render_template, url_for, flash, redirect, request
import datetime
import calendar
# import urllib2


DEBUG = True  # configuration
SECRET_KEY = 'l55Vsm2ZJ5q1U518PlxfM5IE2T42oULB'

app = Flask(__name__)
app.config.from_object(__name__)

# app.logger.addHandler(logging.StreamHandler(sys.stdout))
# app.logger.setLevel(logging.ERsROR)

grafik = None

def u(s):
    return unicode(s, 'utf-8').encode('utf-8')

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

@app.route('/')     # Pierwsza strona
def index():
    global grafik
    grafik = GrafikIwonki()
    return render_template('Grafik Iwonki.html', months=grafik.months, years=grafik.years,
                           current_month=grafik.current_month, current_year=grafik.current_year)   # przekierowanie do pliku


@app.route('/new_schedule', methods=['POST'])
def start_new_schedule():
    global grafik
    grafik = GrafikIwonki()
    selected_month = request.form['month']
    selected_year = int(request.form['year'])
    n = grafik.months.index(selected_month) + 1         # number of selected month
    month_data = calendar.monthrange(selected_year, n)


    print selected_month, n, selected_year
    print month_data
    return render_template('New_schedule.html', months=grafik.months, years=grafik.years,
                           current_month=grafik.current_month, current_year=grafik.current_year,
                           day_no=month_data[1], work=grafik.work)   # przekierowanie do pliku





@app.route('/create_team', methods=['POST'])
def create_team():
    global grafik
    if not grafik:
        grafik = GrafikIwonki()
    return render_template('Create_team.html', size=grafik.team_size, today=grafik.today,
                           months=grafik.months, years=grafik.years,)   # przekierowanie do pliku


@app.route('/delete_team', methods=['POST'])
def delete_team():
    global grafik
    return render_template('Create_team.html', size=grafik.team_size, today=grafik.today,
                           months=grafik.months, years=grafik.years,)   # przekierowanie do pliku


@app.route('/plus_person', methods=['POST'])
def plus_person():
    global grafik
    grafik.team_size += 1
    return render_template('Create_team.html', size=grafik.team_size, today=grafik.today,
                           months=grafik.months, years=grafik.years,)   # przekierowanie do pliku


@app.route('/minus_person', methods=['POST'])
def minus_person():
    global grafik
    grafik.team_size -= 1
    if grafik.team_size == 0:
        grafik.team_size = 1
    return render_template('Create_team.html', size=grafik.team_size, today=grafik.today,
                           months=grafik.months, years=grafik.years,)   # przekierowanie do pliku


@app.route('/save_team', methods=['POST'])
def save_team():
    global grafik
    if not grafik:
        grafik = GrafikIwonki()
    team = [request.form['team_name']]
    try:
        team.append(request.form['person0'])
        team.append(request.form['person1'])
        team.append(request.form['person2'])

    except:
        pass


    # searchword = request.args.get('team_name', '')

    # for i in range(grafik.team_size):
    #     team.append(request.form["person" + str(i)])


    print grafik.team_size
    print team
    print "team was saved"
    return render_template('Create_team.html', size=grafik.team_size, today=grafik.today,
                           months=grafik.months, years=grafik.years,no="xxx")





# @app.route('/newgame', methods=['POST'])
# def start_new_game():      # kasowanie dotychczasowej gry i rozpoczęśie od nowa
#     global game
#     game = None      # rozpoczyna grę od nowa !!!!!!
#     return redirect(url_for('update_game_status'))  # przekierowanie















if __name__ == '__main__':
    app.run()