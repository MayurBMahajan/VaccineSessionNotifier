from constants import Constants
import requests
from fake_useragent import UserAgent
from datetime import datetime,timedelta
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


def get_availability_by_districtcode(district_code,date):
    url = Constants.availability_by_district_url.format(district_code,date)
    return get_sessions(url)


def today(day):
    tommorows_date = datetime.now()+timedelta(days=day)
    return tommorows_date.strftime(Constants.DD_MM_YYYY)


def check_vaccine_availibility(day):
    try:
        if DISTRICT_CODE:
            response = get_availability_by_districtcode(DISTRICT_CODE,today(day))
        if PINCODE:
            response = get_availability_by_pincode(PINCODE,today(day))
        if len(response['centers'])>0:
            if check_available_slots(response):
                print(response)
                sendEmail(EMAIL_ID,PASSWORD,json.dumps(response,indent=4, sort_keys=True))
            else:
                print("No Vaccine Sessions Available, Retrying in {} seconds".format(SLEEPER))
                time.sleep(SLEEPER)
                return
        else:
            print("No Vaccine Sessions Available, Retrying in {} seconds".format(SLEEPER))
            time.sleep(SLEEPER)
            return
    except Exception as e:
        pass


def check_available_slots(response):
    for centers in response['centers']:
        for session in centers['sessions']:
            if session['available_capacity'] > 0:
                print(centers)
                return True
    return False


if __name__ == "__main__":
    while True:
        for day in range(6):
            check_vaccine_availibility(day)
