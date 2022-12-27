from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdrivermanager.chrome import ChromeDriverManager
import time
import os
import csv
from config import get

chrome_options = Options()
chrome_options.add_argument('--headless') #to make chrome window invisible
chrome_options.add_argument('--window-size=1920x1080') #to maximize window in order to view all elements of the web application
chrome_options.add_argument('--disable-gpu') #to avoid errors related to headless on windows
chrome_options.add_argument('--disable-browser-side-navigation')

def main():
    if not os.path.isdir('auto_place'):
        os.mkdir('auto_place')
    for username in os.listdir('auto_place'):
        credential1 = username.rstrip('.csv')
        login(credential1)

def login(credential1):
    service = Service()
    driver = webdriver.Chrome(service=service, options=chrome_options)
    try:
        driver.get(get('metro_website'))
        element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'input-text')))
    except Exception as e:
        print(e)
        driver.quit()
        time.sleep(300)
        main()
    res = driver.execute_script('return document.documentElement.outerHTML')
    soup = BeautifulSoup(res, features='html.parser')
    try:
        login = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'login-button')))
    except Exception as e:
        print(e)
        driver.quit()
        time.sleep(300)
        main()
    username = driver.find_element(By.NAME,'username')
    password = driver.find_element(By.NAME,'password')
    with open('config.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if credential1==row[0]:
                credential2=row[1]
    username.send_keys(credential1)
    password.send_keys(credential2)
    login.click()
    time.sleep(10)
    try:
        error = driver.find_element(By.NAME,'Login-error-msg')
        if error.is_visible():
            nonexistent(credential1)
    except:
        try:
            place(credential1, driver)
        except Exception as e:
            print(e)
            driver.quit()
            time.sleep(300)
            main()

def place(credential1, driver):
    driver.switch_to.frame('main')
    try:
        close = driver.find_element(By.NAME,'closeButton')
        close.click()
    except:
        pass
    trade = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.LINK_TEXT, 'TRADE')))
    trade.click()
    orders = []
    path = os.path.join('auto_place', credential1 + '.csv')
    with open(path, 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            orders.append(row)
    for order in orders:
        submit = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, 'btnprevw')))
        if order[0]=='buy':
            buy = driver.find_element(By.XPATH,'//input[@value=\'BUY\']')
            if not buy.is_selected():
                buy.click()
        else:
            sell = driver.find_element(By.XPATH,'//input[@value=\'SELL\']')
            if not sell.is_selected():
                sell.click()
        stock = driver.find_element(By.NAME,'seccode')
        stock.send_keys(order[1])
        quantity = driver.find_element(By.NAME,'volume')
        quantity.send_keys(order[2])
        price = driver.find_element(By.ID,'price')
        price.send_keys(order[3])
        term = Select(driver.find_element(By.ID,'term'))
        term.select_by_value(order[4])
        submit.click()
        time.sleep(10)
        with open('config.csv') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if credential1==row[0]:
                    credential2=row[1]
        try:
            password = driver.find_element(By.ID,'password')
            password.send_keys(credential2)
            confirm = driver.find_element(By.ID,'Image1')
            confirm.click()
        except:
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            back = driver.find_element(By.ID,'NOBack')
            back.click()
            stock.clear()
            quantity.clear()
            price.clear()
            continue
        path = os.path.join('auto_place', credential1 + '.csv')
        data = []
        with open(path, 'r') as file:
            csv_reader = csv.reader(file)
            i=0
            for row in csv_reader:
                if i>0:
                    data.append(row)
                i+=1
        with open(path, 'w', newline='') as file:
            csv_writer = csv.writer(file)
            for datum in data:
                csv_writer.writerow(datum)
    os.remove(path)
    driver.quit()

def nonexistent(username):
    data = []
    with open('config.csv', 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if row[0]==username:
                pass
            else:
                data.append(row)
    with open('config.csv', 'w', newline='') as file:
        csv_writer = csv.writer(file)
        for row in data:
            csv_writer.writerow(row)
    path = os.path.join('auto_place', username + '.csv')
    os.remove(path)

main()