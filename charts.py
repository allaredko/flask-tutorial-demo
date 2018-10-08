from io import BytesIO
import matplotlib.pyplot as plt
from user_database import get_data

MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
CITIES = ['St. Petersburg', 'Paris', 'Prague', 'Singapore', 'San Francisco']


def get_meteo_data_for_city(city):
    data = get_data()
    city_yearly_temp = 0
    city_yearly_hum = 0
    city_temp = []
    city_hum = []

    for record in data:
        if record[0] == city:
            city_temp.append(record[3])
            city_hum.append(record[2])
            city_yearly_temp += record[3]
            city_yearly_hum += record[2]

    return city_yearly_temp / 12, city_yearly_hum / 12, city_temp, city_hum


def get_main_image():
    """Rendering the scatter chart"""
    yearly_temp = []
    yearly_hum = []

    for city in CITIES:
        city_yearly_temp, city_yearly_hum, city_temp, city_hum = get_meteo_data_for_city(city)
        yearly_temp.append(city_yearly_temp)
        yearly_hum.append(city_yearly_hum)

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
    city = CITIES[city_id]
    _, _, city_temp, city_hum = get_meteo_data_for_city(city)

    plt.clf()
    plt.plot(MONTHS, city_temp, color="blue", linewidth=2.5, linestyle="-")
    plt.ylabel('Mean Daily Temperature', color="blue")
    plt.yticks(color="blue")
    plt.twinx()
    plt.plot(MONTHS, city_hum, color="red", linewidth=2.5, linestyle="-")
    plt.ylabel('Average Relative Humidity', color="red")
    plt.yticks(color="red")
    plt.title(city)

    img = BytesIO()
    print('before', len(img.getvalue()))
    plt.savefig(img)
    print('after', len(img.getvalue()))
    img.seek(0)
    return img
