import os
from functools import wraps
from flask import Flask, render_template, send_file, request, session, redirect, url_for, flash
from user_database import MeteoData, engine
from sqlalchemy import update, and_
from charts import get_city_image, get_main_image, CITIES, MONTHS, get_meteo_data_for_city

# Flask application instance
app = Flask(__name__)


# Entry point; the view for the main page
@app.route('/')
def main():
    return render_template('main.html', cities=enumerate(CITIES))


# The view for rendering the scatter chart
@app.route('/main.png')
def main_plot():
    img = get_main_image()
    return send_file(img, mimetype='image/png', cache_timeout=0)


# The view for the login page
@app.route('/login/<int:city_id>',  methods=["GET", "POST"])
def login(city_id):
    error = ''
    try:
        if request.method == "POST":
            attempted_username = request.form['username']
            attempted_password = request.form['password']
            # login verification
            if attempted_username == "admin" and attempted_password == "password":
                session['logged_in'] = True
                session['username'] = request.form['username']
                return redirect(url_for('edit_database', city_id=city_id))
            else:
                print("invalid credentials")
                error = "Invalid credentials. Please, try again."
        return render_template('login.html', error=error, city_name=CITIES[city_id], city_id=city_id)
    except Exception as error:
        return render_template("login.html", error=error, city_name=CITIES[city_id], city_id=city_id)


# Login session
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
        return redirect(url_for('login'))
    return wrap


# Views for the city details
@app.route('/city/<int:city_id>')
def city(city_id):
    return render_template('city.html', city_name=CITIES[city_id], city_id=city_id)


# Views for rendering city specific charts
@app.route('/city<int:city_id>.png')
def city_plot(city_id):
    img = get_city_image(city_id)
    return send_file(img, mimetype='image/png', cache_timeout=0,)


# Views for editing city specific data
@app.route('/edit/<int:city_id>', methods=["GET", "POST"])
@login_required
def edit_database(city_id):
    meteo = get_meteo_data_for_city(CITIES[city_id])
    try:
        if request.method == "POST":
            connection = engine.connect()
            for i in range(12):
                month_temperature = float(request.form['temperature%s' % i])
                month_humidity = int(request.form['humidity%s' % i])
                # database update
                stm = update(MeteoData).where(and_(MeteoData.c.City == CITIES[city_id], MeteoData.c.Month == MONTHS[i]))
                stm = stm.values(AverageHumidity=month_humidity, AverageTemperature=month_temperature)
                connection.execute(stm)
            connection.close()
            return redirect(url_for("main", city_id=city_id))
        else:
            return render_template("edit.html", city_name=CITIES[city_id], city_id=city_id, months=MONTHS, meteo=meteo)
    except Exception as error:
        return render_template("edit.html", city_name=CITIES[city_id], city_id=city_id, months=MONTHS, meteo=meteo,
                               error=error)


app.secret_key = os.environ['FLASK_WEB_APP_KEY']

if __name__ == '__main__':
    app.run()
