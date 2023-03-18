from dotenv import dotenv_values

import pickle
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import os
import telebot


env_conf = dotenv_values(os.path.abspath(os.path.dirname(__file__)) + "/.env")

options = Options()
options.headless = True
driver = webdriver.Chrome(env_conf.get("CHROME_DRIVER_PATH"), options=options)

driver.get(env_conf.get("VOIP_BLAZER_URL"))
elements = driver.find_elements(By.CLASS_NAME, 'myloginform')

login = None
for element in elements:
    block_style = element.get_attribute("style")
    if block_style == "display: block;":
        login = element
        break
if login is None:
    print("VoIP Blazer: could not find the login form, exiting...")
    exit(0)

login.find_element(
    By.XPATH, "div[2]/form/table/tbody/tr[1]/td[2]/input").send_keys(env_conf.get("VOIP_BLAZER_ID"))
login.find_element(
    By.XPATH, "div[2]/form/table/tbody/tr[2]/td[2]/input").send_keys(env_conf.get("VOIP_BLAZER_PASSWORD"))
login.find_element(
    By.XPATH, 'div[2]/form/table/tbody/tr[5]/td[2]/input').send_keys(Keys.ENTER)

current_balance = driver.find_element(By.CLASS_NAME, "balance").text
print("VoIP Blazer Balance: {0}".format(current_balance))

try:
    file = open(".voippickle", 'rb')
    pickled_list = pickle.load(file)
    message_status = pickled_list[1]
    previous_balance = pickled_list[0]
except Exception as e:
    print("Cannot load the pickled data:", e)
    message_status = False
    previous_balance = current_balance

def send_alert():
    alert = "<b>ALERT!</b>\nVoIP balance is low: {0}".format(current_balance)
    bot = telebot.TeleBot(env_conf.get("TELEGRAM_BOT_TOKEN"))
    bot.send_message(chat_id=env_conf.get("TELEGRAM_CHAT_ID"),
                 parse_mode="HTML",
                 disable_notification=True,
                 text=alert)

def dump_data(current_balance, message_status):
    data = []
    data.append(current_balance)
    data.append(message_status)
    print(data)
    file = open('.voippickle', 'wb')
    pickle.dump(data, file)

previous_balance_int = float(previous_balance.replace(",", "").replace("€ ", ""))
current_balance_int = float(current_balance.replace(",", "").replace("€ ", ""))

if current_balance_int >= 1500:
    message_status = False
    dump_data(current_balance, message_status)
    print("Current balance is greater than 1,500.")
    exit(0)

if message_status == True:
    if previous_balance_int - 500 < current_balance_int:
        print("The alert has already been sent.")
        exit(0)
    else:
        send_alert()
        dump_data(current_balance, message_status)
        print("We have resent the alert")
        exit(0)

send_alert()
message_status = True
dump_data(current_balance, message_status)
print("We have sent an alert, as the current balance is less than 1,500.")
exit(0)
