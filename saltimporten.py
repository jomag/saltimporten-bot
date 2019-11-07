from io import BytesIO
from datetime import datetime
import requests
from flask import Flask, jsonify
from bs4 import BeautifulSoup
from PyPDF2 import PdfFileReader

URL = "https://www.saltimporten.com"
URBAN_DELI_URL = "https://www.urbandeli.org/sickla/"

weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']

def get_urban_deli():
    # First get link to PDF
    response = requests.get(URBAN_DELI_URL, verify=False)
    soup = BeautifulSoup(response.text, "html.parser")
    lunch = soup.find('h2', text="LUNCH")
    link = lunch.parent.parent['href']

    # Next, get PDF
    pdf_response = requests.get(link)
    pdf_file = BytesIO(pdf_response.content)
    reader = PdfFileReader(pdf_file)

    # Lunch menu is on page four
    page4 = reader.getPage(3)
    lines = page4.extractText().split('\n')
    
    # Extract lunch for each week day
    next_key = None
    dishes = {}

    for line in lines:
        line = line.strip()

        if next_key:
            dishes[next_key] = line
            next_key = None
        elif line.lower() in weekdays or line.lower() == 'vegan':
            next_key = line.lower()

    today = weekdays[datetime.today().weekday()]

    meat = "No lunch found for today"
    veg = "No veg alt found for today"

    try:
        meat = dishes[today]
    except KeyError:
        pass

    try:
        veg = dishes['vegan']
    except KeyError:
        pass

    return (meat.lower().capitalize(), veg.lower().capitalize())


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
        return jsonify({
            "response_type": "in_channel",
            "text": f"Today's main course is: *{meat}*. Veg of the week: *{veg}*"
        })
    except e:
        return "i'm not working today"

@app.route('/urban-deli', methods=['GET', 'POST'])
def urban_deli():
    try:
        meat, veg = get_urban_deli()
        return jsonify({
            "response_type": "in_channel",
            "text": f"Today's main course is: *{meat}*. Veg of the week: *{veg}*"
        })
    except e:
        return "i'm not working today"

if __name__ == "__main__":
    # print(get_todays_menu())
    print(get_urban_deli())


