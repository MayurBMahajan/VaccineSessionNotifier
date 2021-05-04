from vaccineSessionNotifier.constants import Constants
import requests
from fake_useragent import UserAgent
from datetime import datetime
from userInput import *
from emailSend import sendEmail
import json,time


def get_sessions(url):
    user_agent = UserAgent()
    headers = {'User-Agent': user_agent.random}
    response = requests.get(url, headers=headers)
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        return e
    return response.json()


def get_availability_by_pincode(pin_code: str, date: str):
    url = Constants.sessions_by_pin_7_days.format(pin_code,date)
    return get_sessions(url)


def today():
    return datetime.now().strftime(Constants.DD_MM_YYYY)


def check_vaccine_availibility():
    response = get_availability_by_pincode(PINCODE,today())
    print(response)
    if len(response['centers'])>0:
        sendEmail(EMAIL_ID,PASSWORD,json.dumps(response,indent=4, sort_keys=True))
    else:
        print("No Vaccine Sessions Available, Retrying in {} seconds".format(SLEEPER))
        time.sleep(SLEEPER)
        check_vaccine_availibility()


if __name__ == "__main__":
    check_vaccine_availibility()
