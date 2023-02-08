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
    elif rank == "LCP":
        rank_val = 412010
    elif rank == "CPL":
        rank_val = 412011
    elif rank == "3SG":
        rank_val = 412012
    elif rank == "2SG":
        rank_val = 412013
    elif rank == "1SG":
        rank_val = 412014
    elif rank == "SSG":
        rank_val = 412015
    elif rank == "MSG":
        rank_val = 412016
    elif rank == "CFC":
        rank_val = 416022
    return rank_val

def hub_db_id(hub):
    hub_val = 0
    if hub == "HQ TPT":
        hub_val = 415990
    elif hub == "1 TPT":
        hub_val = 415991
    elif hub == "3 TPT":
        hub_val = 415992
    elif hub == "WEST":
        hub_val = 415993
    elif hub == "EAST":
        hub_val = 415994
    return hub_val
    
def coy_db_id(coy):
    coy_val = 0
    if coy == "1TPT HQ":
        coy_val = 415995
    if coy == "ALPHA":
        coy_val = 412017
    elif coy == "CHARLIE":
        coy_val = 412018
    elif coy == "HMCT":
        coy_val = 412019
    elif coy == "MANDAI":
        coy_val = 412020
    elif coy == "KRANJI":
        coy_val = 412021
    elif coy == "KHATIB":
        coy_val = 412022
    elif coy == "LTC":
        coy_val = 412023
    elif coy == "HQ TPT":
        coy_val = 415996
    elif coy == "3TPT HQ":
        coy_val = 415997
    elif coy == "AIR TERMINAL":
        coy_val = 415998
    elif coy == "SEA TERMINAL":
        coy_val = 416025
    elif coy == "LARC V":
        coy_val = 415999
    elif coy == "CHANGI":
        coy_val = 416000
    elif coy == "TUAS":
        coy_val = 416001
    elif coy == "CLEMENTI":
        coy_val = 416002
    elif coy == "SELARANG":
        coy_val = 416003
    elif coy == "SELETAR":
        coy_val = 416004
    elif coy == "NEE SOON":
        coy_val = 416005
    elif coy == "BEDOK":
        coy_val = 416006
    elif coy == "TEKONG":
        coy_val = 416007
    elif coy == "JURONG":
        coy_val = 416009
    elif coy == "KEAT HONG":
        coy_val = 416008
    elif coy == "PASIR LABA":
        coy_val = 416010
    elif coy == "SUNGEI GEDONG":
        coy_val = 416011
    elif coy == "WEST HQ":
        coy_val = 416170
    elif coy == "EAST HQ":
        coy_val = 416171
    return coy_val

def submit_booking(name, rank2, hub, coy2, contact, date, count:int, tele_id:int):
    try:
        company_id = coy_db_id(coy2)
        rank_id = rank_db_id(rank2)
        hub_id = hub_db_id(hub)
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
            "Telegram ID": tele_id,
            "Count": count,
            "Hub": hub_id
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
        if if_holiday(reservation_date_str) == False and reservation_date_time.weekday() < 5 and check_spotsleft(reservation_date_str) > 0 :
            reservation_list.append(reservation_date_str)
            reservation_date_time +=  timedelta(days=i+1)
            reservation_date_str = str(reservation_date_time.strftime('%Y-%m-%d'))
        else:
            reservation_date_time +=  timedelta(days=i+1)
            reservation_date_str = str(reservation_date_time.strftime('%Y-%m-%d'))
    return(reservation_list)

def check_spotsleft(user_day): #counts total spots left
    results = requests.get(f'{api_url}{BOOKING_TABLE}/?user_field_names=true',headers=HEADERS).json()
    A_counter = 20
    R_counter = 0
    nVar = 0
    spots_left = 20
    for item in results['results']:
        if user_day == str(item['Date of Booking']):
            nVar = int(item['Count'])
            R_counter += nVar
    spots_left = A_counter - R_counter
    return spots_left 

def count_total_signups(user_day): #counts total spots booked
    results = requests.get(f'{api_url}{BOOKING_TABLE}/?user_field_names=true',headers=HEADERS).json()
    R_counter = 0
    nVar = 0
    for item in results['results']:
        if user_day == str(item['Date of Booking']):
            nVar = int(item['Count'])
            R_counter += nVar
    return R_counter

def display_data(the_date):
    results = requests.get(f'{api_url}{BOOKING_TABLE}/?user_field_names=true',headers=HEADERS).json()
    name_list = []
    rank_list = []
    hub_list = []
    company_list = []
    date_list = []
    count_list = []
    contact_list = []
    id_list = []
    final_list = []
    for item in results['results']:
        if the_date == str(item['Date of Booking']):
            row_id = item['id']
            itemise = requests.get(f'{api_url}{BOOKING_TABLE}/{row_id}/?user_field_names=true',headers=HEADERS).json()
            name_list.append(itemise['Name'])
            rank_list.append(itemise['Rank']['value'])
            hub_list.append(itemise['Hub']['value'])
            company_list.append(itemise['Company']['value'])
            date_list.append(itemise['Date of Booking'])
            count_list.append(itemise['Count']) #but this returns total... dafaq
            contact_list.append(itemise['Contact'])
            id_list.append(itemise['Telegram ID'])
    for i in range (len(name_list)):
        test01 = "Name: "+name_list[i]+"\nRank: "+rank_list[i]+"\Hub: "+hub_list[i]+"\nCompany: "+company_list[i]+"\nDate of Booking: "+date_list[i]+"\nCount: "+count_list[i]+"\nContact: "+contact_list[i]+"\nTelegram ID: "+id_list[i]
        final_list.append(test01)
    return final_list
display_data("2023-02-07")
