from bs4 import BeautifulSoup #use pip to download
import requests #use pip to download
from selenium import webdriver #use pip to download #needed aside from BeautifulSoup because dynamic webpages need a "user"(the webdriver) to load all elements
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait #to allow wait
from selenium.webdriver.support import expected_conditions as EC #to allow expected conditions
from selenium.webdriver.chrome.options import Options #to allow add argument
from selenium.webdriver.chrome.service import Service
from webdrivermanager.chrome import ChromeDriverManager
import time
import csv
import os
from datetime import date
from config import get

chrome_options = Options()
chrome_options.add_argument('--headless') #to make chrome window invisible
chrome_options.add_argument('--window-size=1920x1080') #to maximize window in order to view all elements of the web application
chrome_options.add_argument('--disable-gpu') #to avoid errors related to headless on windows
chrome_options.add_argument('--disable-browser-side-navigation')

keys={}
html=[]

def main():
    keys.clear()
    html.clear()
    today = date.today()
    name = today.strftime("%m-%d-%y")
    name = name + '.csv'
    os.chdir(get('home_directory'))
    path = os.path.join('stock_data', name) #plsce where to save csv file
    if not os.path.isdir('stock_data'):
        os.mkdir('stock_data')
    if not os.path.isfile(path):
        link_gathering(startup())
        mass_scraping(path)
    data = []
    check = False
    with open(path, 'r', newline='') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            data.append(row[0])
            if row[0]=='2GO':
                if row[1]=='' and row[2]=='':
                    check = True
    if data[-1] != 'IPO' and check:
        os.remove(path)
        print('lag')
        time.sleep(300)
        main()

def data_collection(soup):
    i=0
    for word in soup.findAll('a', {'href': '#company'}):
        name = word.text
        temp = word.get('onclick').strip('cmDetail(\'').strip('\');return false').split('\',\'')
        if i%2==1:
            keys[name]=temp
        i+=1
def button_click(driver, soup, n):
    for word in soup.findAll('a', {'href': '#'}):
        if word.text==str(n):
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            time.sleep(5)
            try:
                driver.find_element("link text", str(n)).click()
            except:
                print('Lag')
                driver.quit()
                time.sleep(300)
                main()
            return 0
def startup():
    service = Service()
    driver = webdriver.Chrome(service=service,options=chrome_options)
    #download chromedriver and place its path here
    driver.set_page_load_timeout(30)
    try:
        driver.get(get('edge_directory')) #starting website remember to identity the html elements you want to interact with
    except Exception as e:
        print(e)
        driver.quit()
        time.sleep(300)
        main()
    try:
        element = WebDriverWait(driver,20).until(EC.presence_of_element_located((By.LINK_TEXT, '6')))
    except:
        print('Lag')
        driver.quit()
        time.sleep(300)
        main()
    return driver
def link_gathering(driver):
    res = driver.execute_script('return document.documentElement.outerHTML')
    soup = BeautifulSoup(res, features='html.parser')
    data_collection(soup)
    for n in range(2,7):
        try:
            element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.LINK_TEXT, '6')))
        except:
            print('Lag')
            driver.quit()
            time.sleep(300)
            main()
        button_click(driver, soup, n)
        time.sleep(5)
        try:
            if n==6:
                element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.LINK_TEXT, '5')))
            else:
                element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.LINK_TEXT, '6')))
        except:
            print('Lag')
            driver.quit()
            time.sleep(300)
            main()
        res = driver.execute_script('return document.documentElement.outerHTML')
        soup = BeautifulSoup(res, features='html.parser')
        data_collection(soup)
    driver.quit()

def mass_scraping(path):
    with open(path, 'w+', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(['code', 'last traded price', 'open','previous close', 'percent change', 'high', 'low', '52 week high', '52 week low', 'board lot', 'par value', 'market capitalization', 'outstanding shares', 'listed shares', 'issued shares'])
    for key in keys.keys():
        value = keys[key]
        url = get('stock_data') + value[0] + '&security_id=' + value[1]
        try:
            source_code = requests.get(url)
        except:
            os.remove(path)
            print('lag')
            time.sleep(300)
            main()
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, features='html.parser')
        temp = []
        for word in soup.find_all('td', {'style': 'text-align:right;padding-right:1.2em;'}):
            word = word.text.strip().replace(' ', '')
            temp.append(word)
        for word in soup.find_all('td', {'style': 'text-align:right;padding-right:1.5em;'}):
            word = word.text.strip().replace(' ', '')
            temp.append(word)
        data = []
        data.append(key)
        data.append(temp[0])
        data.append(temp[1])
        close = temp[2].split('\r\n')
        data.append(close[0])
        temp[3] = temp[3].strip('%)')
        change = temp[3].split('(')
        data.append(change[1])
        data.append(temp[4])
        data.append(temp[7])
        data.append(temp[12])
        data.append(temp[13])
        data.append(temp[19])
        data.append(temp[21])
        data.append(temp[15])
        data.append(temp[16])
        data.append(temp[17])
        data.append(temp[18])
        with open(path, 'a+', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(data)
        print(data)

main()