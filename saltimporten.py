import requests
from flask import Flask
from bs4 import BeautifulSoup

URL = "https://www.saltimporten.com"

def get_todays_menu():
    response = requests.get(URL, verify=False)
    soup = BeautifulSoup(response.text, "html.parser")
    current = soup.find("li", class_="current")
    meat = current.find("div", class_="meal")
    veg = soup.find("div", class_="veg")
    veg = veg.parent.find("div", class_="meal")
    return meat.string, veg.string

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        meat, veg = get_todays_menu()
        return f"Today's main course is: *{meal}*. Veg of the week: *{veg}*"
    except e:
        return "i'm not working today"

if __name__ == "__main__":
    print(get_todays_menu())


