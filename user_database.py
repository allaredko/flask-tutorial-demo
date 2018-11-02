from sqlalchemy import MetaData, create_engine, Table, Column, select, ForeignKey

metadata = MetaData()
engine = create_engine('sqlite:///user_database')

# Table city
city_table = Table('city', metadata,
                   Column('city_id', int, primary_key=True),
                   Column('city_name', str),
                   Column('city_climate', str),
                   autoload=True, autoload_with=engine,
                   )
# Table meteo
meteo_table = Table('meteo', metadata,
                    Column('city_id', int, ForeignKey("city.city_id")),
                    Column('month', str),
                    Column('average_humidity', int),
                    Column('average_temperature', float),
                    autoload=True, autoload_with=engine,
                    )


# Retrieving data from the database
def get_data():
    with engine.connect() as connection:
        meteo_data = connection.execute(select([meteo_table])).fetchall()
        city_data = connection.execute(select([city_table])).fetchall()
        return city_data, meteo_data
