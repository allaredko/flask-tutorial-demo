from sqlalchemy import MetaData, create_engine, Table, Column, select, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

metadata = MetaData()
# ToDo: do not use check_same_thread
engine = create_engine('sqlite:///user_database', connect_args={'check_same_thread': False}, echo=False)  # echo=False
Base = declarative_base()
db_session = sessionmaker(bind=engine)()


# Table city
class City(Base):
    __tablename__ = 'city'
    city_id = Column(Integer, primary_key=True)
    city_name = Column(String)
    city_climate = Column(String)

    city_meteo_data = relationship("Meteo", backref="city")


# Table meteo
class Meteo(Base):
    __tablename__ = 'meteo'
    id = Column(Integer, primary_key=True)
    city_id = Column(ForeignKey('city.city_id'))
    month = Column(String)
    average_humidity = Column(Integer)
    average_temperature = Column(Float)


# Retrieving data from the database
def get_cities():
    return db_session.query(City)


# ToDo: type annotations
def get_city_temperature(city):
    return [month.average_temperature for month in city.city_meteo_data]


def get_city_humidity(city):
    return [month.average_humidity for month in city.city_meteo_data]


data = get_cities()

MONTHS = [record.month for record in data[0].city_meteo_data]
CITIES = [city.city_name for city in data]
