from imports import *
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

def get_prices():#alice_request):
	opts = FirefoxOptions()
	opts.add_argument("--headless")
	service = Service(executable_path="./geckodriver")
	driver = webdriver.Firefox(firefox_binary="/usr/bin/firefox-esr", service=service, options=opts)
	driver.get("https://www.aviasales.ru/?params=LED1")
	driver.implicitly_wait(30)
	# ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,)
	# your_element = WebDriverWait(driver, 120, ignored_exceptions=ignored_exceptions)\
    #                     .until(expected_conditions.presence_of_element_located((By.CLASS_NAME, "form-tabs__item"))).click()
	# print(your_element)
	# driver.find_element(By.LINK_TEXT, "Отели").
	elems = driver.find_elements(By.TAG_NAME, "a")
	for i in elems:
		print(i.text)
	# driver.implicitly_wait(20)
	driver.save_full_page_screenshot("./page.png")
	#return alice_request.response("ABOBA")

get_prices()