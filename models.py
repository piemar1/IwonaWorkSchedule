# -*- coding: utf-8 -*-
#!/usr/bin/python
__author__ = 'Marcin Pieczyński'


class Team:
    def __init__(self, team_name, creation_date, crew):
        self.team_name = team_name
        self.creation_date = creation_date
        self.crew = crew

    def __str__(self):
        return "{}, {}, {}".format(self.team_name, self.creation_date, self.crew)


class Schedule:
    def __init__(self, schedule_name, creation_date, month, year, crew, schedule):
        self.schedule_name = schedule_name
        self.creation_date = creation_date
        self.crew = crew
        self.month = month
        self.year = year
        self.schedule = schedule

    def __str__(self):
        return "{}, {}, {}, {},{}, {}".format(self.schedule_name, self.creation_date,
                                                  self.month, self.year,
                                                  self.crew, self.schedule)

    # def __str__(self):
    #     return "{}, {}, {}, {}".format(self.schedule_name, self.creation_date,
    #                                    self.month, self.year)


if __name__ == "__main__":

    import datetime
    date = datetime.date

    team = Team("drużynaA", date.today(), "person1, person2, person3")
    print(team)

    schedule = Schedule("scheduleA", date.today(), 5, 2016,
                        "person1, person2, person3", "D.N, D.D, .DN")
    print(schedule)