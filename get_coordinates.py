from geopy.geocoders import Nominatim #Подключаем библиотеку
from geopy.distance import geodesic #И дополнения

def get_coord(city_name):
    geolocator = Nominatim(user_agent="Tester") #Указываем название приложения
    address_1 = str(city_name) #Получаем название первого города
    location_1 = geolocator.geocode(address_1) #Получаем полное название первого города
    return [location_1.latitude, location_1.longitude]