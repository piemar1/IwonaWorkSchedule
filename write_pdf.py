# -*- coding: utf-8 -*-
#!/usr/bin/python

landscape__author__ = 'marcin'


from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import BaseDocTemplate, Frame, Paragraph, PageTemplate, Table, Spacer, TableStyle
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from models import Person, Schedule
import os
import io


# dodanie czcionki z polskimi literami
pdfmetrics.registerFont(TTFont('Tinos-Regular', 'static/fonts/Tinos-Regular.ttf'))
pdfmetrics.registerFont(TTFont('Tinos-Bold', 'static/fonts/Tinos-Bold.ttf'))

styles=getSampleStyleSheet()
style1 = ParagraphStyle(name="myStyleCenter", alignment=TA_CENTER, fontName="Tinos-Bold")
style2 = ParagraphStyle(name="myStyleLEFT", alignment=TA_LEFT, fontName="Tinos-Regular")
style3 = ParagraphStyle(name="myStyle", alignment=TA_CENTER, fontName="Tinos-Regular")

styles.add(style1)
styles.add(style2)
styles.add(style3)


class WritePDF:
    """
    Klasa zawierająca potrzebne metody do zapisu grafiku schedule w postaci tabeli w pliku pdf.
    """
    def __init__(self, file_like_handle, schedule, month_calendar, month_working_days, no_of_workdays):
        """Constructor"""

        self.schedule = schedule
        self.month_calendar = month_calendar
        self.month_working_days = month_working_days
        self.no_of_workdays = no_of_workdays

        self.width, self.height = letter
        self.styles = getSampleStyleSheet()

        self.buffer = file_like_handle
        self.story = []

    def run(self):
        """
        Run the report
        """
        def make_landscape(canvas,doc):
            canvas.setPageSize(landscape(letter))

        # file initialization in buffer !!!!
        self.doc = BaseDocTemplate(self.buffer,
                                   showBoundary=1,
                                   pagesize=landscape(letter))

        # create the frames. Here you can adjust the margins
        frame = Frame(self.doc.leftMargin-60,
                      self.doc.bottomMargin - 50,
                      self.doc.width + 120,
                      self.doc.height + 110, id='first_frame')

        # add the PageTempaltes to the BaseDocTemplate.
        # You can also modify those to adjust the margin if you need more control over the Frames.
        self.doc.addPageTemplates(PageTemplate(id='first_page',
                                               frames=frame,
                                               onPage=make_landscape))

        self.create_text()
        self.create_table()
        self.create_footer()
        self.doc.build(self.story)

    def create_text(self):
        """
        Create the document and write the text,
        """
        header_text = u"ROZKŁAD PRACY PERSONELU PIELEGNIARSKIEGO"
        p = Paragraph(header_text, styles['myStyleCenter'])
        self.story.append(p)
        self.story.append(Spacer(1, 0.5*cm))

        ptext = u"Szpital Kliniczny Przemienienia Pańskiego UM w Poznaniu"
        p = Paragraph(ptext, styles['myStyleLEFT'])
        self.story.append(p)
        self.story.append(Spacer(1, 0.5*cm))

        ptext = u"{} {} ==> liczba dni roboczych w miesiącu ==> {}, " \
                u"liczba dyżurów ==> {}".format(self.schedule.month,
                                                self.schedule.year,
                                                self.month_working_days,
                                                self.no_of_workdays)
        p = Paragraph(ptext, styles['myStyleLEFT'])
        self.story.append(p)

    def create_table(self):
        """
        Create the table
        """
        data = []

        # tworzenie danych dla pierwszych dwóch wierszy tabeli
        line = ["Lp", "Nazwisko i imię"]
        line.extend([str(no) for no, day in self.month_calendar])
        data.append(line)

        line = ["Lp", "Nazwisko i imię"]
        line.extend([day for no, day in self.month_calendar])
        data.append(line)

        # zbieranie info o columnach danych dla soboty i niedzieli
        weekend_columns = [n for n, elem in enumerate(line) if elem in ["so", "n"]]

        # wypełnianie tabeli dla poszczególnych osób
        for n, (person, one_schedule) in enumerate(zip(self.schedule.crew, self.schedule.schedule)):
            line = ["{}.".format(str(n +1 )), person]
            line.extend([daywork for daywork in one_schedule])
            data.append(line)

        # liczba wierszy w tabeli
        row_number = n + 2

        # ustawianie stylu / coloru dla soboty i niedzieli
        color_col = [('BACKGROUND', (col, 0), (col, row_number), colors.lightgrey) for col in weekend_columns]

        table = Table(data)
        table.hAlign = "CENTRE"

        # styl tabeli
        mytablestyle = [("FONTNAME", (0,0),(-1,-1), 'Tinos-Regular'),
                        ("FONTSIZE", (0,0),(-1,-1), 8.5),
                        ("SPAN", (0,0), (0,1)),
                        ("SPAN", (1,0), (1,1)),
                        ('ALIGN',(0,0),(-1,-1),'CENTER'),
                        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                        ('FONTNAME', (0,0), (-1,1), 'Tinos-Bold'),
                        ('FONTNAME', (0,0), (1,-1), 'Tinos-Bold'),
                        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                        ('BOX', (0,0), (-1,-1), 0.25, colors.black)]

        # dodanie do stylu tabeli kolorów dla soboty i niedzieli
        mytablestyle.extend(color_col)

        table.setStyle(TableStyle(mytablestyle))

        self.story.append(Spacer(1, 1*cm))
        self.story.append(table)


    def create_footer(self):

        header_text = u"Grafik przygotowany w programie GrafikIwonki. " \
                      u"Copyright Marcin Pieczyński, kontakt marcin-pieczynski@wp.pl"
        p = Paragraph(header_text, styles['myStyle'])
        self.story.append(Spacer(1, 0.5*cm))
        self.story.append(p)


if __name__ == "__main__":

    schedule_name = "FIRST Schedule"
    creation_date = "today"
    month = "styczeń"
    year = 2016
    crew = [u'Aaa', u'Bbb', u'C', u'D', u'E',
            u'F', u'G', u'H', u'I', u'J',
            u'K', u'L', u'Mmm', u'Nnn', u'O']

    schedule = [u'D.........UUUUUU..............N',
                u'.D...........................N.',
                u'..D.........................N..',
                u'...D.................UUUUUUN...',
                u'....D.....................N....',
                u'.....D...................N.....',
                u'......D.................N......',
                u'.......D...............N.......',
                u'........D.............N........',
                u'UUU...UUUUUUU........N.........',
                u'..........D.........N..........',
                u'...........D..UUUUUUUU.........',
                u'............D.....N............',
                u'.............D...N.............',
                u'..............D.N..............']

    first_schedule = Schedule(schedule_name, creation_date, month, year, crew, schedule)

    from main import get_month_calendar

    month_calendar = get_month_calendar(first_schedule.year, first_schedule.month)
    # print(month_calendar)



    t = WritePDF("test.pdf", first_schedule, month_calendar, 24, 14)
    t.run()












