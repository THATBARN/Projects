from dotenv import dotenv_values

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import telebot
import os


env_conf = dotenv_values(os.path.abspath(os.path.dirname(__file__)) + "/.env")

options = Options()
options.headless = True
driver = webdriver.Chrome(env_conf.get("CHROME_DRIVER_PATH"), options=options)

driver.get(env_conf.get("PDS_URL"))

driver.find_element(
    By.XPATH, '//*[@id="mt_id"]').send_keys(env_conf.get("PDS_ID"))
driver.find_element(
    By.XPATH, '//*[@id="mt_pwd"]').send_keys(env_conf.get("PDS_PASS"))


login = driver.find_element(By.XPATH, '//*[@id="loginBtn"]')
if login is None:
    print("PDS: could not find the login form, exiting...")
    exit(0)
login.click()

balance = driver.find_element(
    By.XPATH, '//*[@id="content"]/div[2]/div[2]/font').text
print("PDS Balance: ￦{0}".format(balance))

if float(balance.replace(",", "")) <= 1000000:
    alert = "<b>ALERT!</b>\nThe PDS balance is low: ￦{0}".format(balance)
    bot = telebot.TeleBot(env_conf.get("TELEGRAM_BOT_TOKEN"))
    bot.send_message(chat_id=env_conf.get("TELEGRAM_CHAT_ID"),
                     parse_mode="HTML",
                     disable_notification=True,
                     text=alert)
