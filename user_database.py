from sqlalchemy import MetaData, create_engine, Table, select

metadata = MetaData()
engine = create_engine('sqlite:///user_database')
MeteoData = Table('Meteo', metadata, autoload=True, autoload_with=engine)


# Retrieving meteo data from the database
def get_data():
    connection = engine.connect()
    selection = select([MeteoData])
    data = connection.execute(selection).fetchall()
    connection.close()
    return data
