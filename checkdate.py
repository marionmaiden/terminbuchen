import requests
import time
from bs4 import BeautifulSoup
from emailsender import EmailSender

url = "https://service.berlin.de/terminvereinbarung/termin/tag.php?termin=1&anliegen[]=327537&dienstleisterlist=122210,122217,122219,122227&herkunft=http%3A%2F%2Fservice.berlin.de%2Fdienstleistung%2F327537%2F"
emailPropertiesFile = "./resources/email.properties"

"""
"""
def pretty(arr):
    out = ""

    for a in arr:
        out += "[" + a.text + "]"

    return out

"""
"""
def checkTermin(email):
    found = False
    termins = ""

    while not found:

        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')

        months = soup.find_all(class_="calendar-month-table")


        for month in months:

            termin = month.find_all(class_="buchbar")

            if len(termin) > 0:
                termins += "<b>" + month.find(class_="month").text + "</b>: " + pretty(termin) + "<br>"
                found = True


        if found:
            print(termins)
            email.sendEmail(termins)
        else:
            print("Termin not found retrying in 100s")
            time.sleep(100)



def main():
    email = EmailSender(emailPropertiesFile)
    checkTermin(email)

if __name__ == "__main__": main()
