import requests
from config import BASEROW_TOKEN
from aiogram.dispatcher.filters.state import State, StatesGroup
import holidays
from datetime import date
from datetime import datetime, timedelta

api_url = "https://api.baserow.io/api/database/rows/table/"
HEADERS = {"Authorization": f'Token {BASEROW_TOKEN}'}
HEADERS_JSON = {"Authorization": f'Token {BASEROW_TOKEN}', "Content-Type": "application/json"}
ADMIN_ACCESS_TABLE = 136952
BOOKING_TABLE = 136953

def check_isadmin(user_id:int):
    results = requests.get(f'{api_url}{ADMIN_ACCESS_TABLE}/?user_field_names=true',headers=HEADERS).json()
    try:
        for item in results['results']:
            if user_id == int(item['TelegramID']):
                type = True
                break
        return type
    except:
        type = False
        return type

def check_hasbooking(tele_id):
    results = requests.get(f'{api_url}{BOOKING_TABLE}/?user_field_names=true',headers=HEADERS).json()
    try:
        for item in results['results']:
            if tele_id == int(item['Telegram ID']):
                type = True
                break
        return type
    except:
        type = False
        return type

def get_booking_by_id(tele_id):
    results = requests.get(f'{api_url}{BOOKING_TABLE}/?user_field_names=true',headers=HEADERS).json()
    data = None
    for item in results['results']:
        if tele_id == int(item['Telegram ID']):
            data = item['Date of Booking']
    return data

def rank_db_id(rank):
    rank_val = 0
    if rank == "PTE":
        rank_val = 412009
        return rank_val
    elif rank == "LCP":
        rank_val = 412010
        return rank_val
    elif rank == "CPL":
        rank_val = 412011
        return rank_val
    elif rank == "3SG":
        rank_val = 412012
        return rank_val
    elif rank == "2SG":
        rank_val = 412013
        return rank_val
    elif rank == "1SG":
        rank_val = 412014
        return rank_val
    elif rank == "SSG":
        rank_val = 412015
        return rank_val
    elif rank == "MSG":
        rank_val = 412016
        return rank_val
    
def coy_db_id(coy):
    coy_val = 0
    if coy == "ALPHA":
        coy_val = 412017
        return coy_val
    elif coy == "CHARLIE":
        coy_val = 412018
        return coy_val
    elif coy == "HMCT":
        coy_val = 412019
        return coy_val
    elif coy == "MANDAI":
        coy_val = 412020
        return coy_val
    elif coy == "KHATIB":
        coy_val = 412021
        return coy_val
    elif coy == "KRANJI":
        coy_val = 412022
        return coy_val
    elif coy == "LTC":
        coy_val = 412023
        return coy_val

def submit_booking(name, rank2, coy2, contact, date, tele_id:int):
    try:
        company_id = coy_db_id(coy2)
        rank_id = rank_db_id(rank2)
        submission = requests.post(
        "https://api.baserow.io/api/database/rows/table/136953/?user_field_names=true",
        headers={
        "Authorization": f'Token {BASEROW_TOKEN}',
        "Content-Type": "application/json"
        },
        json={
            "Name": name,
            "Company": company_id,
            "Date of Booking": date,
            "Rank": rank_id,
            "Contact": contact,
            "Telegram ID": tele_id
        }
    )
    except Exception as err:
        print(f'Error: {err}')

def remove_booking(telegram_id):
    results = requests.get(f'{api_url}{BOOKING_TABLE}/?user_field_names=true',headers=HEADERS).json()
    for item in results['results']:
        if telegram_id == int(item['Telegram ID']):
            row_id = item['id']
    requests.delete(f'{api_url}{BOOKING_TABLE}/{row_id}/',headers=HEADERS)
       
def if_holiday(date_str):
    holidayList = []
    currentYear = date.today().year
    date_object = datetime.strptime(date_str, '%Y-%m-%d').date()
    for holiday in holidays.Singapore(years=[currentYear]).items():
        holidayList.append(holiday[0])
    for i in range(len(holidayList)):
        if date_object == holidayList[i]:
            return True
    return False
    
def reservation_date():
    reservation_list = []
    date_str = str(date.today())
    strpDate = datetime.strptime(date_str, "%Y-%m-%d")
    i = len(reservation_list)
    reservation_date_time = strpDate + timedelta(days=i+1)
    reservation_date_str = str(reservation_date_time.strftime('%Y-%m-%d'))
    while len(reservation_list) < 5:
        if if_holiday(reservation_date_str) == False and reservation_date_time.weekday() < 5:
            reservation_list.append(reservation_date_str)
            reservation_date_time +=  timedelta(days=i+1)
            reservation_date_str = str(reservation_date_time.strftime('%Y-%m-%d'))
        else:
            reservation_date_time +=  timedelta(days=i+1)
            reservation_date_str = str(reservation_date_time.strftime('%Y-%m-%d'))
    return(reservation_list)

def check_spotsleft(user_day):
    results = requests.get(f'{api_url}{BOOKING_TABLE}/?user_field_names=true',headers=HEADERS).json()
    A_counter = 20
    R_counter = 0
    spots_left = 20
    for item in results['results']:
        if user_day == str(item['Date of Booking']):
            R_counter +=1
            spots_left = A_counter - R_counter
    return spots_left  

def display_data(the_date):
    results = requests.get(f'{api_url}{BOOKING_TABLE}/?user_field_names=true',headers=HEADERS).json()
    name_list = []
    rank_list = []
    company_list = []
    date_list = []
    contact_list = []
    id_list = []
    final_list = []
    for item in results['results']:
        if the_date == str(item['Date of Booking']):
            row_id = item['id']
            itemise = requests.get(f'{api_url}{BOOKING_TABLE}/{row_id}/?user_field_names=true',headers=HEADERS).json()
            name_list.append(itemise['Name'])
            rank_list.append(itemise['Rank']['value'])
            company_list.append(itemise['Company']['value'])
            date_list.append(itemise['Date of Booking'])
            contact_list.append(itemise['Contact'])
            id_list.append(itemise['Telegram ID'])
    for i in range (len(name_list)):
        test01 = "Name: "+name_list[i]+"\nRank: "+rank_list[i]+"\nCompany: "+company_list[i]+"\nDate of Booking: "+date_list[i]+"\nContact: "+contact_list[i]+"\nTelegram ID: "+id_list[i]
        final_list.append(test01)
    return final_list
