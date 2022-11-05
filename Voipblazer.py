from dotenv import dotenv_values

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import telebot


env_conf = dotenv_values(".env")

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
    print("Could not find the login form, exiting...")
    exit(0)

login.find_element(
    By.XPATH, "div[2]/form/table/tbody/tr[1]/td[2]/input").send_keys(env_conf.get("VOIP_BLAZER_ID"))
login.find_element(
    By.XPATH, "div[2]/form/table/tbody/tr[2]/td[2]/input").send_keys(env_conf.get("VOIP_BLAZER_PASSWORD"))
login.find_element(
    By.XPATH, 'div[2]/form/table/tbody/tr[5]/td[2]/input').send_keys(Keys.ENTER)

balance = driver.find_element(By.CLASS_NAME, "balance").text
print("The current balance: " + balance)

if float(balance.replace("€ ", "").replace(",", "")) <= 700:
    alert = "<b>ALERT!</b>\nThe VoIP balance is low: {0}".format(balance)
    bot = telebot.TeleBot(env_conf.get("TELEGRAM_BOT_TOKEN"))
    bot.send_message(chat_id=env_conf.get("TELEGRAM_CHAT_ID"),
                     parse_mode="HTML",
                     disable_notification=True,
                     text=alert)
