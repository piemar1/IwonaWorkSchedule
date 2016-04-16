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


class Person:
    def __init__(self, name, schedule):
        self.name = name
        self.schedule = schedule
        self.working_days = self.get_working_days_number_person()

    def __str__(self):
        return str(self.name)

    def get_working_days_number_person(self):
        """
        Funkcja zwraca liczbę dyżurów dziennych lub nocnych w ciągu miesiąca grafiku.
        """
        number = 0
        for day in self.schedule:
            if day == u"D" or day == u"N":
                number += 1
        return number

    def wheather_day_is_free(self, number):
        """
        Metoda zwraca True jeśli osoba może przyjąć dyżur, False jeśli nie może przyjąć dyżuru.
        """
        if self.schedule[number] == ".":
            return True
        return False

    def take_work(self, day_number, work):
        """
        Metoda wprowadza zmiany w grafiku dla zadanego, grafiku, dnia i rodzaju dyżuru
        """
        if day_number == 0:
            self.schedule = "{}{}".format(work, self.schedule[1:])

        else:
            self.schedule = "{}{}{}".format(self.schedule[:day_number],
                                            work,
                                            self.schedule[day_number + 1:])

    def filtre_double_work(self):
        """
        Metoda zwraca True jeśli osoba nie ma podwójnego dyżuru ND - nocka - dniówka 24h, inaczej False.
        """
        if "ND" in self.schedule:
            return False
        return True

    def filtre_work_days_in_week(self, working_days_number):
        """
        Metoda zwraca True jeśli liczba dni roboczych w schedule nie przekracza 4, inaczej False.
        """
        def filtr_working_days_in_week(str, working_days_number):
            """
            Funkcja zwraca True jeśli liczba dni roboczych w str nie przekracza 4, inaczej False
            """
            number = 0
            for day in str:
                if day == u"D" or day == u"N":
                    number += 1
            if number > working_days_number:
                return False
            return True

        schedule_parts = [self.schedule[numbers:numbers + 7] for numbers in range(len(self.schedule) - 7)]
        results = [filtr_working_days_in_week(parts, working_days_number) for parts in schedule_parts]

        if all(results):
            return True
        return False

    def filtre_work_days_in_month(self, no_of_working_days):
        """
        Metoda zwraca Trur jeśli osoba ma mniej dni roboczych w miesiącu niż no_of_working_days, inaczej False.
        """
        if self.get_working_days_number_person() <= no_of_working_days:
            return True
        return False


if __name__ == "__main__":

    import datetime
    date = datetime.date

    team = Team("drużynaA", date.today(), "person1, person2, person3")
    print(team)

    schedule = Schedule("scheduleA", date.today(), 5, 2016,
                        ["person1", "person2", "person3"], ["D.N", "D.D", ".DN"])
    print(schedule)