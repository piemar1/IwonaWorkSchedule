# -*- coding: utf-8 -*-
__author__ = 'marcin'


schedule = u'...............................'

def input_work_to_person(one_schedule, day_number):
    """
    Metoda wprowadza zmiany w grafiku dla zadanego, grafiku, dnia i rodzaju dyżuru
    """
    output_schedule = ""

    if day_number == 0:
        output_schedule = "{}{}".format("D", one_schedule[1:])

    else:
        output_schedule = "{}{}{}".format(one_schedule[:day_number],
                                       "D",
                                       one_schedule[day_number + 1:])
    print(output_schedule, "\n")







if __name__ == '__main__':
    print("początek", schedule, "\n")

    for number in range(len(schedule)):
        print(number, len(schedule))
        input_work_to_person(schedule, number)


