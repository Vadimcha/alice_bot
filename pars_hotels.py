from imports import *
from get_coordinates import get_coord
import requests
from bs4 import BeautifulSoup as bs

def get_prices(city):
	cord = get_coord(city)
	URL_TEMPLATE = "https://city.travel/hotel/search/" + cord[0] + ',' + cord[1] +",IRL/1/04.04.2023/05.04.2023"
	r = requests.get(URL_TEMPLATE)
	print(r.status_code)