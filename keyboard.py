from aiogram.types import ReplyKeyboardMarkup

def admin_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    markup.add("Collate Data")
    return markup

def client_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    markup.add("Make Booking")
    markup.add("Request Admin Access")
    return markup

def rank_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    markup.add("PTE")
    markup.add("LCP")
    markup.add("CPL")
    markup.add("CFC")
    markup.add("3SG")
    markup.add("2SG")
    markup.add("1SG")
    markup.add("SSG")
    markup.add("MSG")
    return markup


def hub_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    markup.add("HQ TPT")
    markup.add("1 TPT")
    markup.add("3 TPT")
    markup.add("WEST")
    markup.add("EAST")
    return markup

def HQTPT_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    markup.add("HQ TPT")
    return markup

def first_coy_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    markup.add("1TPT HQ")
    markup.add("ALPHA")
    markup.add("CHARLIE")
    markup.add("HMCT")
    markup.add("MANDAI")
    markup.add("KHATIB")
    markup.add("KRANJI")
    markup.add("LTC")
    return markup

def third_coy_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    markup.add("3TPT HQ")
    markup.add("AIR TERMINAL")
    markup.add("SEA TERMINAL")
    markup.add("LARC V")
    markup.add("CHANGI")
    markup.add("TUAS")
    markup.add("CLEMENTI")
    return markup

def east_coy_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    markup.add("EAST HQ")
    markup.add("SELARANG")
    markup.add("SELETAR")
    markup.add("NEE SOON")
    markup.add("BEDOK")
    markup.add("TEKONG")
    return markup

def west_coy_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    markup.add("WEST HQ")
    markup.add("JURONG")
    markup.add("KEAT HONG")
    markup.add("PASIR LABA")
    markup.add("SUNGEI GEDONG")
    return markup


def confirmation_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    markup.add("✅")
    markup.add("❌")
    return markup

def rmv_kb():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    markup.add("Cancel Booking")
    return markup

def date_keyboard(reservationList:list):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    markup.add(reservationList[0])
    markup.add(reservationList[1])
    markup.add(reservationList[2])
    markup.add(reservationList[3])
    markup.add(reservationList[4])
    return markup
 
 

