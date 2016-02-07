# -*- coding: utf-8 -*-

from flask import Flask, render_template, url_for, flash, redirect, request, g
import sqlite3

DATABASE = "database.db"

# def get_db():
#     """ Connecting to the databese."""
#     db = getattr(g, '_database', None)
#     if db is None:
#         db = g._database = sqlite3.connect(DATABASE)
#         print "Connect to DB \n"
#     return db
#
# @app.teardown_appcontext
# def close_connection(exception):
#     """ Closing connection to database"""
#     db = getattr(g, '_database', None)
#     if db is not None:
#         db.close()


class SqliteDb(object):

    def database_check(self):

        self.conn = sqlite3.connect(DATABASE)
        self.cur = self.conn.cursor()

        self.cur.execute("SELECT name FROM sqlite_master WHERE type = 'table';")
        self.table_names = [elem[0] for elem in self.cur.fetchall()]

        print "self.table_names-1", type(self.table_names), self.table_names

        if "TEAM" not in self.table_names:
            self.conn.execute("CREATE TABLE TEAM (team_name TEXT, team TEXT)")
        if "SCHEDULES" not in self.table_names:
            self.conn.execute("CREATE TABLE SCHEDULES (date TEXT, team_name TEXT, schedule TEXT)")

        print "self.table_names-2", type(self.table_names), self.table_names
        self.conn.close()

    def save_team_to_db(self, team_to_save):

        self.con = sqlite3.connect(DATABASE)
        with self.con:
            self.cur = self.con.cursor()
            self.cur.executemany("INSERT INTO TEAM VALUES(?, ?)", (team_to_save,))
            print "ZAPISANO TEAM W DB!!!!!!!!!!!"
        self.conn.close()

    def read_team_names_db(self):

        self.conn = sqlite3.connect(DATABASE)
        self.cur = self.conn.cursor()

        self.cur.execute("SELECT * FROM TEAM")
        rows = self.cur.fetchall()
        self.team_names = [row[0] for row in rows]

        print len(rows)

        print "self.team_names"
        for team in self.team_names:
            print "team", team

        print "powyżej powinna być baza danych"
        self.conn.close()

    def delete_team(self, team_name_to_delete):

        self.conn = sqlite3.connect(DATABASE)
        self.cur = self.conn.cursor()

        self.cur.execute("DELETE from TEAM where team_name = '%s';" % team_name_to_delete)

        self.conn.commit()
        print "Total number of rows deleted :", self.conn.total_changes
        self.conn.close()

    def read_one_team_db(self, team_to_edit):
        self.conn = sqlite3.connect(DATABASE)
        self.cur = self.conn.cursor()

        self.cur.execute("SELECT * FROM TEAM")

        rows = self.cur.fetchall()

        for row in rows:
            if row[0] == team_to_edit:
                self.team_to_edit = row
        self.conn.close()
        print "self.team_to_edit", self.team_to_edit
