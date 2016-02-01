# ! /usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3 as lite

__author__ = 'Marcin Pieczyński'


def creating_team_table_sqlite():
    cursor.execute("CREATE TABLE TEAM (team_name TEXT, team TEXT)")
    cursor.executemany("INSERT INTO " + nazwa + " VALUES(?, ?, ?)", final_profile)


def get_tables_from_db(self):
    """
    The method for reading tables names from db.
    """
    self.cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table';")

    # Return list of tuples with the names of tables --> names of profiles.
    self.profiles_name_list = [elem[0] for elem in self.cursor.fetchall()]
    self.profiles_name_list = tuple(self.profiles_name_list)






class SQliteEdit:
    """
    The Class containing methods for reading and saving profiles in Profile_database.db file.
    """
    def __init__(self):
        """
        Init method of SQliteEdit class.
        """
        self.con = lite.connect('Profile_database.db')               # Opening of database file
        self.cursor = self.con.cursor()


    def get_tables_from_db(self):
        """
        The method for reading tables names from db.
        """
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table';")

        # Return list of tuples with the names of tables --> names of profiles.
        self.profiles_name_list = [elem[0] for elem in self.cursor.fetchall()]
        self.profiles_name_list = tuple(self.profiles_name_list)

    def get_data_from_profile(self, profile_to_use):
        """
        The methods for reading data from profile
        """
        self.cursor.execute("SELECT * FROM " + profile_to_use)

        for row in self.cursor.fetchall():
            if row[0] == "PvNa_UNITS":
                self.output_zakladki.append(row[1])

                a = [elem.strip() for elem in row[2].split(",")]
                self.output_leki.append(a)

            elif row[0] == "CEGLY":
                self.output_leki_cegly = [elem.strip() for elem in row[2].split(",")]

            elif row[0] == "lista_cegiel":
                self.output_lista_cegiel = [elem.strip() for elem in row[2].split(",")]

    def sqsave_profile(self, nazwa, final_profile):
        """
        The methods for saving prifile in db file
        """
        self.cursor.execute("DROP TABLE IF EXISTS " + nazwa)
        self.cursor.execute("CREATE TABLE " + nazwa + "(Typ TEXT, Id_Grupy TEXT, lek TEXT)")
        self.cursor.executemany("INSERT INTO " + nazwa + " VALUES(?, ?, ?)", final_profile)

    def sqdel_profile(self, profile_to_del):
        """
        The methods for deleting profile.
        """
        self.cursor.execute("DROP TABLE IF EXISTS " + profile_to_del)
