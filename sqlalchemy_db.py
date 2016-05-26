__author__ = 'Marcin Pieczyński'


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_models import Base, DbTeam, DbSchedule
from models import Team, Schedule



# pobranie i drukowanie nazw wszystkich tabel w bazie danych
# from sqlalchemy.engine import reflection
# insp = reflection.Inspector.from_engine(engine)
# print(insp.get_table_names())


def conn_to_db():
    """
    Nawiązuje połączenie z bazą danych w calu zapisu danych.
    """

    engine = create_engine('sqlite:///sqlalchemy_db.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    return DBSession()


def save_team_to_db(team):
    """
    Zapisuje team do bazy, Jako arg przyjmuje instancję Team.
    Jeżeli dany wpis w db już istnieje, usuwa poprzedni wpis i tworzy nowy.
    """

    session = conn_to_db()
    if team.team_name in get_team_names_from_db():
        delete_team_in_db(team.team_name)

    team.crew_str = ",".join(team.crew)

    new_team = DbTeam(team_name = team.team_name,
                       creation_date = team.creation_date,
                       crew = team.crew_str)

    session.add(new_team)
    session.commit()


def save_schedule_to_db(schedule):
    """
    Zapisuje schedule do bazy, jako arg przyjmuję gotową instancję Schedule
    Jeżeli dany wpis w db już istnieje, usuwa poprzedni wpis i tworzy nowy.
    """
    session = conn_to_db()
    if schedule.schedule_name in get_schedule_names_from_db():
        delete_schedule_in_db(schedule.schedule_name)

    schedule.crew_str, schedule.schedule_str = ",".join(schedule.crew), ",".join(schedule.schedule)
    team_from_db = session.query(DbTeam).filter(DbTeam.crew == schedule.crew_str).one()

    new_schedule = DbSchedule(schedule_name = schedule.schedule_name,
                              creation_date = schedule.creation_date,
                              month = schedule.month,
                              year = schedule.year,
                              crew = team_from_db,
                              schedule = schedule.schedule_str)
    session.add(new_schedule)
    session.commit()


def get_team_names_from_db():
    """
    Zwraca listę stringów z nazwami teams.
    """

    session = conn_to_db()

    team_list = session.query(DbTeam).all()
    team_names = [dbteam.team_name for dbteam in team_list]
    return team_names


def get_schedule_names_from_db():
    """
    Zwraca listę stringów z nazwami schedules.
    """

    session = conn_to_db()

    schedule_list = session.query(DbSchedule).all()
    schedule_names = [dbschedule.schedule_name for dbschedule in schedule_list]
    return schedule_names


def delete_team_in_db(team_name_to_delete):
    """
    Usuwa wpis dla podanego team z bazy danych.
    """

    session = conn_to_db()
    team_from_db = session.query(DbTeam).filter(DbTeam.team_name == team_name_to_delete).one()

    session.delete(team_from_db)
    session.commit()


def delete_schedule_in_db(schedule_name_to_delete):
    """
    Usuwa wpis dla podanego schedule z bazy danych.
    """

    session = conn_to_db()
    schedule_from_db = session.query(DbSchedule).filter(DbSchedule.schedule_name == schedule_name_to_delete).one()

    session.delete(schedule_from_db)
    session.commit()


def get_team_from_db(team_name_to_read):
    """
    Zwraca instancję Team na podstawie danych z db, jako arg przyjmuje team_name.
    """

    session = conn_to_db()

    team_from_db = session.query(DbTeam).filter(DbTeam.team_name == team_name_to_read).one()
    team = Team(team_from_db.team_name, team_from_db.creation_date, team_from_db.crew.split(","))

    return team



def get_schedule_from_db(schedule_name_to_read):
    """Zwraca instancję Schedule na podstawie danych z db, jako arg przyjmuje schedule_name."""

    session = conn_to_db()
    schedule_from_db = session.query(DbSchedule).filter(DbSchedule.schedule_name == schedule_name_to_read).one()

    try:
        team = schedule_from_db.crew
        crew = team.crew.split(",")
    except AttributeError:
        return False

    schedule = Schedule(schedule_from_db.schedule_name,
                        schedule_from_db.creation_date,
                        schedule_from_db.month,
                        schedule_from_db.year,
                        crew,
                        schedule_from_db.schedule.split(","))
    return schedule

if __name__ == '__main__':

    import datetime
    date = datetime.date

    teamA = Team("drużynaA", date.today(), ["person1", "person2", "person3"])
    teamB = Team("drużynaB", date.today(), ["person444", "person2222", "personX"])
    teamC = Team("drużynaC", date.today(), ["person1111", "person666", "person55555"])

    scheduleA = Schedule("scheduleA", date.today(), 5, 2016,
                         ["person1", "person2", "person3"], ["D.N", "D.D", ".DN"])

    # save_team_to_db(teamA)
    # get_team_from_db("drużynaC")
    # delete_team_in_db("drużynaC")

    # save_schedule_to_db(scheduleA)
    # get_schedule_from_db("2016-05-13 wprowadź nazwę dla grafiku ...")
    # delete_schedule_in_db("scheduleA")

    get_team_names_from_db()
    get_schedule_names_from_db()
