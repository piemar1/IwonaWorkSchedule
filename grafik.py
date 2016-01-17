import datetime
import calendar


# obecna data

now = datetime.datetime.now()
print "a", str(now)
print "b", now.month
print "c", now.year


print datetime.date.today()

m = datetime.date(2016, 1, 15)
print m.ctime()
print m.year
print m.month
print m.day

print 30 * "%"
c = calendar.Calendar(1)
print c.itermonthdates(2016, 1)

# for elem in c.itermonthdates(2016, 10):
#     print elem
# print 30 * "$"
# for elem in c.itermonthdays2(2016, 10):
#     print elem

print c.monthdatescalendar(2016, 1)

print 30 * "#"

print calendar.weekday(2016, 1, 7)  # wskazuje dzien tygodnia mon = 0, tue = 1 ....
print calendar.monthrange(2016, 1)  # 1 = styczen (dzien tygodnia rozpoczynajacy miesiac, liczba dni w miesiacu)

print calendar.monthrange(2016, 12)
print calendar.weekheader(10)

print calendar.monthcalendar(2016, 1)  # ciekawa lista z tygodniami i dniami tygodnia

