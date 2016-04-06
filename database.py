# -*- coding: utf-8 -*-
#!/usr/bin/python
__author__ = 'Marcin Pieczyński'


import sqlite3
from models import Team, Schedule


DATABASE = "grafik_iwonki.db"


def db_init():
    """
    Inicjalizacja bazy w pliku w przypadku jej usunięcia.
    Tworzenie potrzebnych tabel w bazie
    """
    conn = sqlite3.connect(DATABASE)

    with conn:
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type = 'table';")
        table_names = [elem[0] for elem in cur.fetchall()]

        if "Teams" not in table_names:
            conn.execute('''CREATE TABLE Teams (team_name TEXT,
                                                creation_date TEXT,
                                                crew TEXT)''')
            print("Teams was created")
        if "Schedules" not in table_names:
            conn.execute('''CREATE TABLE Schedules (schedule_name TEXT,
                                                    creation_date TEXT,
                                                    month INT,
                                                    year INT,
                                                    crew TEXT,
                                                    schedule TEXT)''')
            print("Schedules was created")


def get_names_from_db(sqlScript):
    """
    Nawiązuje połączenie z bazą danych w celu odczytu nazw Teams lub Schedules
    """
    conn = sqlite3.connect(DATABASE)
    with conn:
        cur = conn.cursor()
        cur.execute(sqlScript)
        rows = cur.fetchall()
        names = [row[0] for row in rows]
        return names


def get_team_names_from_db():
    """
    Zwraca listę stringów z nazwami teams
    """
    sqlScript = "select * from Teams"
    return get_names_from_db(sqlScript)


def get_schedule_names_from_db():
    """
    Zwraca listę stringów z nazwami schedules
    """
    sqlScript = "select * from Schedules"
    return get_names_from_db(sqlScript)


def conn_to_db(sqlScript):
    """
    Nawiązuje połączenie z bazą danych w calu zapisu danych
    """
    conn = sqlite3.connect(DATABASE)
    with conn:
        cur = conn.cursor()
        cur.execute(sqlScript)


def save_team_to_db(team):
    """
    Zapisuje team do bazy, jako arg przyjmuję instancję Team.
    Jeżeli dany wpis w db już istnieje, usuwa poprzedni wpis i tworzy nowy.
    """
    team.crew_str = ",".join(team.crew)

    sqlScript = '''INSERT INTO
                   Teams (team_name, creation_date, crew)
                   VALUES ('{}', '{}', '{}')'''.format(team.team_name,
                                                       team.creation_date,
                                                       team.crew_str)
    if team.team_name in get_team_names_from_db():
        delete_team_in_db(team.team_name)

    return conn_to_db(sqlScript)


def save_schedule_to_db(schedule):
    """
    Zapisuje schedule do bazy, jako arg przyjmuję gotową instancję Schedule
    Jeżeli dany wpis w db już istnieje, usuwa poprzedni wpis i tworzy nowy.
    """
    schedule.crew = ",".join(schedule.crew)
    schedule.schedule = ",".join(schedule.schedule)

    sqlScript = '''INSERT INTO
                   Schedules (schedule_name, creation_date, month, year, crew, schedule)
                   VALUES ('{}', '{}', '{}', '{}', '{}', '{}')'''.format(schedule.schedule_name,
                                                                         schedule.creation_date,
                                                                         schedule.month,
                                                                         schedule.year,
                                                                         schedule.crew,
                                                                         schedule.schedule)

    if schedule.schedule_name in get_schedule_names_from_db():
        delete_schedule_in_db(schedule.schedule_name)

    return conn_to_db(sqlScript)


def delete_team_in_db(team_name_to_delete):
    """
    Usuwa wpis dla podanego team z bazy danych.
    """
    sqlScript = "DELETE from Teams where team_name = '{}';".format(team_name_to_delete)
    return conn_to_db(sqlScript)


def delete_schedule_in_db(schedule_name_to_delete):
    """
    Usuwa wpis dla podanego schedule z bazy danych.
    """
    sqlScript = "DELETE from Schedules where schedule_name = '{}';".format(schedule_name_to_delete)
    return conn_to_db(sqlScript)


def get_team_from_db(team_name_to_read):
    """
    Zwraca instancję Team na podstawie danych z db, jako arg przyjmuje team_name.
    """
    conn = sqlite3.connect(DATABASE)
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM Teams where team_name = '{}';".format(team_name_to_read))
        team_name, creation_date, crew = cur.fetchone()

        crew = crew.split(",")

        team = Team(team_name, creation_date, crew)
        return team


def get_schedule_from_db(schedule_name_to_read):
    """
    Zwraca instancję Schedule na podstawie danych z db, jako arg przyjmuje schedule_name.
    """
    conn = sqlite3.connect(DATABASE)
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM Schedules where schedule_name = '{}';".format(schedule_name_to_read))
        schedule_name, creation_date, month, year, crew, schedule = cur.fetchone()

        crew = crew.split(",")
        schedule = schedule.split(",")

        schedule = Schedule(schedule_name, creation_date, month, year, crew, schedule)
        return schedule


if __name__ == "__main__":

    import datetime
    date = datetime.date

    teamA = Team("drużynaA", date.today(), ["person1", "person2", "person3"])
    scheduleA = Schedule("scheduleA", date.today(), 5, 2016,
                         ["person1", "person2", "person3"], ["D.N", "D.D", ".DN"])
    print(teamA)
    print(scheduleA)

    db_init()

    # save_team_to_db(teamA)
    # save_schedule_to_db(scheduleA)

    # delete_team_in_db("drużynaA")
    # delete_schedule_in_db("scheduleA")

    print(get_team_names_from_db())
    print(get_schedule_names_from_db())

    # print(get_team_from_db("drużynaA"))
    # print(get_schedule_from_db("scheduleA"))













