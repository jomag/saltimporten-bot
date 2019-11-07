import requests
from flask import Flask
from bs4 import BeautifulSoup

URL = "https://www.saltimporten.com"

def get_todays_menu():
    response = requests.get(URL, verify=False)
    soup = BeautifulSoup(response.text, "html.parser")
    current = soup.find("li", class_="current")
    meal = current.find("div", class_="meal")
    return meal.string

app = Flask(__name__)

@app.route('/')
def index():
    try:
        meal = get_todays_menu()
        return f"Todays main course is: {meal}"
    except e:
        return "i'm not working today"

if __name__ == "__main__":
    app.run(threaded=True, port=5000)

