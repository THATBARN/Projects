import os
import time
import telebot

from dotenv import dotenv_values

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


env_conf = dotenv_values(os.path.abspath(os.path.dirname(__file__)) + "/.env")

options = Options()
options.headless = True
driver = webdriver.Chrome(env_conf.get("CHROME_DRIVER_PATH"), options=options)

driver.get(env_conf.get("THIS_URL"))

driver.find_element(
    By.XPATH, '//*[@id="scroller"]/form/table/tbody/tr[6]/td/input').send_keys(env_conf.get("THIS_ID"))
driver.find_element(
    By.XPATH, '//*[@id="scroller"]/form/table/tbody/tr[8]/td/input').send_keys(env_conf.get("THIS_PASS"))
time.sleep(5)
login = driver.find_element(
    By.XPATH, '//*[@id="scroller"]/form/table/tbody/tr[11]/td/table/tbody/tr/td[1]/img')
if login is None:
    print("THiS Card: could not find the login form, exiting...")
    exit(0)

elem = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
    (By.XPATH, '//*[@id="scroller"]/form/table/tbody/tr[11]/td/table/tbody/tr/td[1]/img')))
elem.click()

time.sleep(5)

balance = driver.find_element(
    By.XPATH, '//*[@id="scroller"]/table/tbody/tr[3]/td/span')
balance = balance.get_attribute('textContent')
print("THiS Card Balance: ￦{0}".format(balance))

if float(balance.replace(",", "")) <= 500000:
    alert = "<b>ALERT!</b>\nCK (디스카드) balance is low: ￦{0}".format(balance)
    bot = telebot.TeleBot(env_conf.get("TELEGRAM_BOT_TOKEN"))
    bot.send_message(chat_id=env_conf.get("TELEGRAM_CHAT_ID"),
                     parse_mode="HTML",
                     disable_notification=True,
                     text=alert)
