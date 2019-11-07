import requests
from flask import Flask
from bs4 import BeautifulSoup

URL = "https://www.saltimporten.com"

def get_todays_menu():
    response = requests.get(URL, verify=False)
    soup = BeautifulSoup(response.text, "html.parser")
    current = soup.find("li", class_="current")
    meal = current.find("div", class_="meal")
    print(meal.string)
    return meal.string

get_todays_menu()

app = Flask(__name__)

@app.route('/')
def meal_of_the_day():
    try:
        meal = get_todays_menu()
        return meal
    except e:
        return "i'm not working today"

