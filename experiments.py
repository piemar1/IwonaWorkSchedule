# -*- coding: utf-8 -*-
__author__ = 'marcin'

# import calendar
#
# dict_week_days = {0 : u"pon",
#              1 : u"wt",
#              2 : u"śr",
#              3 : u"czw",
#              4 : u"pt",
#              5 : u"sob",
#              6 : u"niedz"}
#
# day_no = calendar.monthrange(2016, 1)[1]
# week_day = calendar.monthrange(2016, 1)[0]
#
# week_days = []
#
# for day in xrange(day_no):
#     week_days.append(dict_week_days[week_day])
#     week_day += 1
#     if week_day == 7:
#         week_day = 0
# month_week_days = zip(range(day_no), week_days)
#
# print day_no, week_day
#
# print week_days
#
# print month_week_days
#
# for elem in month_week_days:
#     print elem




s = "D.DD......UUUUUUDDD....D...D.DN"

for numbers in range(0, len(s)-7):
    print(numbers)
    part = s[numbers:numbers + 7]
    print(part, len(part))


parts = [s[numbers:numbers + 7] for numbers in range(len(s) - 7)]
for part in parts:
    print(part, len(part))