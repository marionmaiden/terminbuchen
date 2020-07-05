import requests
import time
from bs4 import BeautifulSoup
from emailsender import EmailSender
import configparser
import json

# url = "https://service.berlin.de/terminvereinbarung/termin/tag.php?termin=1&anliegen[]=327537&dienstleisterlist=122210,122217,122219,122227&herkunft=http%3A%2F%2Fservice.berlin.de%2Fdienstleistung%2F327537%2F"
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
def checkTermin(email, config):
    found = False
    termins = ""

    urls = json.loads(config.get("urls", "urlArray"))

    # Loop forever
    while not found:

        # Run for each url in the list
        for url in urls:

            # Request page and parse to retrieve the months div
            page = requests.get(url)
            soup = BeautifulSoup(page.text, 'html.parser')
            months = soup.find_all(class_="calendar-month-table")

            # Iterate through each month and check for buchbar dates
            for month in months:

                termin = month.find_all(class_="buchbar")

                # Add date to String if there is a termin for it
                if len(termin) > 0:
                    termins += "<b>" + month.find(class_="month").text + "</b>: " + pretty(termin) + "<br>"
                    found = True


            # If any date found, print on screen and send e-mail
            if found:
                print("===================================")
                print(url + "<br>" + termins)
                print("===================================")
                email.sendEmail("<b>URL:</b>" + url + "<br>" +termins)

            # Clean variables and try other urls after sleep for 5 seconds
            found = False
            termins = ""
            print("Termin not found for url - " + url + " . Trying other urls in 5s")
            time.sleep(5)

        # No dates found. Retry in 50s for all URLS
        print("Termin not found for all URLS. Retrying in 50s")
        time.sleep(50)


# Init e-mail module, config parser and start date checker
def main():
    email = EmailSender(emailPropertiesFile)
    config = configparser.ConfigParser()
    config.read(emailPropertiesFile)
    checkTermin(email, config)

if __name__ == "__main__": main()
