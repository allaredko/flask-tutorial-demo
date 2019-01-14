from io import BytesIO
import matplotlib.pyplot as plt
from user_database import data, MONTHS, get_city_temperature, get_city_humidity, CITIES


def get_main_image():
    """Rendering the scatter chart"""
    yearly_temp = []
    yearly_hum = []

    for city in data:
        yearly_temp.append(sum(get_city_temperature(city))/12)
        yearly_hum.append(sum(get_city_humidity(city))/12)

    plt.clf()
    plt.scatter(yearly_hum, yearly_temp, alpha=0.5)
    plt.title('Yearly Average Temperature/Humidity')
    plt.xlim(70, 95)
    plt.ylabel('Yearly Average Temperature')
    plt.xlabel('Yearly Average Relative Humidity')
    for i, txt in enumerate(CITIES):
         plt.annotate(txt, (yearly_hum[i], yearly_temp[i]))

    img = BytesIO()
    plt.savefig(img)
    img.seek(0)
    return img


def get_city_image(city_id):
    """Rendering line charts with city specific data"""
    city = data.get(city_id)
    city_temp = get_city_temperature(city)
    city_hum = get_city_humidity(city)

    plt.clf()
    plt.plot(MONTHS, city_temp, color='blue', linewidth=2.5, linestyle='-')
    plt.ylabel('Mean Daily Temperature', color='blue')
    plt.yticks(color='blue')
    plt.twinx()
    plt.plot(MONTHS, city_hum, color='red', linewidth=2.5, linestyle='-')
    plt.ylabel('Average Relative Humidity', color='red')
    plt.yticks(color='red')
    plt.title(city.city_name)

    img = BytesIO()
    plt.savefig(img)
    img.seek(0)
    return img
