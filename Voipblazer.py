import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import telebot
import re

PATH = "CHROME_DRIVER_PATH"
BLAZER_ID = "VOIP_BLAZER_ID"
BLAZER_PSW = "VOIP_BLAZER_PASSWORD"
BOT_TOKEN = "TELEGRAM_BOT_TOKEN"

options = Options()
options.headless = True
driver = webdriver.Chrome(os.getenv(PATH), options=options)

driver.get("https://www.voipblazer.com/buy_credit2/")
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

login.find_element(By.XPATH, "div[2]/form/table/tbody/tr[1]/td[2]/input").send_keys(os.getenv(BLAZER_ID))
login.find_element(By.XPATH, "div[2]/form/table/tbody/tr[2]/td[2]/input").send_keys(os.getenv(BLAZER_PSW))
login.find_element(By.XPATH, 'div[2]/form/table/tbody/tr[5]/td[2]/input').send_keys(Keys.ENTER)

balance = driver.find_element(By.CLASS_NAME, "balance").text
print("The current balance: " + balance)

b = float(balance.replace("€ ", "").replace(",", ""))
if b <= 700:
    bot = telebot.TeleBot(os.getenv(BOT_TOKEN))
    bot.send_message(5494804052, 'ALERT!\nVoIP Balance is low: ' + balance)




