import mysql.connector
from mysql.connector import Error
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
import time
import requests
import json
import config
import re
from datetime import datetime

# takes 9 days right now
startTime = datetime.now()

# start by testing if I can add info from one skin to database, then 5 skins then all skins
def getAllSkins():
    # declaring for database
    ID = 1
    # database connection
    connection = mysql.connector.connect(**db_config)


    # establish webdriver
    driver = webdriver.Chrome()
    # chrome_options = ChromeOptions()
    # chrome_options.add_extension('extension_5_10_1_0.crx')
    # driver = webdriver.Chrome(options = chrome_options)
    
    # load steam login
    driver.get("https://help.steampowered.com/en/wizard/Login")
    time.sleep(3)
    # login to steam
    loginForm = driver.find_element("xpath", '//*[@id="wizard_contents"]/div/div/div/div/div/div[2]/div/form/div[1]/input')
    loginForm.send_keys(config.login['user'])
    passForm = driver.find_element("xpath", '//*[@id="wizard_contents"]/div/div/div/div/div/div[2]/div/form/div[2]/input')
    passForm.send_keys(config.login['password'])
    passForm.submit()
    time.sleep(10)

    # load steam market
    marketURL = 'https://steamcommunity.com/market/search?q=&category_730_ItemSet%5B%5D=any&category_730_ProPlayer%5B%5D=any&category_730_StickerCapsule%5B%5D=any&category_730_Tournament%5B%5D=any&category_730_TournamentTeam%5B%5D=any&category_730_Type%5B%5D=any&category_730_Weapon%5B%5D=any&appid=730'
    driver.get(marketURL)
    time.sleep(3)

    numItems = driver.find_element("xpath", '//*[@id="searchResults_total"]')
    count = 0
    # create loop to get every item from every page
    #for i in range(1, numItems + 1):
    for i in range(1, 5):

        # 10 items per page
        if count == 10:
            time.sleep(10)
            # click next page button
            buttonShow = driver.find_element("xpath", '/html/body/div[1]/div[7]/div[4]/div[1]/div[4]/div[2]/div[2]/div/div[2]/div[1]/span[3]')
            buttonShow.click()
            time.sleep(10)
            count = 0
        # click on items in the steam market
        item = driver.find_element("xpath", f'//*[@id="result_{count}"]')
        item.click()
        time.sleep(10)
        # get name of item
        Item = driver.find_element("xpath", '//*[@id="mainContents"]/div[1]/div/a[2]')
        ItemName = Item.text
        print(ItemName)
        # get item URL for search history
        currentURL = driver.current_url
        endURL = get_last_part_of_url(currentURL)
        # load sale history page
        salesURL = 'https://steamcommunity.com/market/pricehistory/?currency=3&appid=730&market_hash_name=' + endURL
        time.sleep(10)
        driver.get(salesURL)
        payload = driver.find_element("xpath", '/html/body/pre')
        payload_text = payload.text
        extractedDetails = extract_price_details(payload_text)
        # split payload into varables
        for detail in extractedDetails:
            DatePurchased = detail['DatePurchased']
            HourPurchased = detail['HourPurchased']
            AvgPrice = detail['AvgPrice']
            Quantity = detail['Quantity']
            insert_transactions(connection, ID, ItemName, DatePurchased, HourPurchased, AvgPrice, Quantity)
            ID+=1

        count += 1
        # go back to previous page
        driver.back()
        driver.back()
        time.sleep(10)

    
def insert_transactions(connection, ID, ItemName, DatePurchased, HourPurchased, AvgPrice, Quantity):
        try:
            cursor = connection.cursor()
            sql = "INSERT INTO Transactions (ID, ItemName, DatePurchased, HourPurchased, AvgPrice, Quantity) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (ID, ItemName, DatePurchased, HourPurchased, AvgPrice, Quantity)
            cursor.execute(sql, val)
            connection.commit()
            return cursor.lastrowid
        except Error as e:
            print(f"Error inserting data into Transactions: {e}")
            return None

def get_last_part_of_url(url: str) -> str:
    # Split the URL by '/' and return the last non-empty part
    return url.rstrip('/').split('/')[-1]

def extract_price_details(json_payload):
    data = json.loads(json_payload)
    
    # List to store the extracted details
    extracted_data = []

    # Process each entry in the 'prices' array
    for entry in data['prices']:
        # Extract components from the entry
        date_str, price, quantity = entry

        # Parse and format the date
        try:
            # Parse the date assuming the format 'Month Day Year Hour: +Timezone'
            date_obj = datetime.strptime(date_str, '%b %d %Y %H: +0')
            date_purchased = date_obj.strftime('%Y-%m-%d')
            hour_purchased = date_obj.strftime('%H:%M')
        except ValueError:
            # Handle errors if date parsing fails
            date_purchased = None
            hour_purchased = None
        
        # Convert price to float and quantity to int
        try:
            avg_price = float(price)
        except ValueError:
            avg_price = None

        try:
            quantity = int(quantity)
        except ValueError:
            quantity = None

        # Append the extracted details to the list
        extracted_data.append({
            'DatePurchased': date_purchased,
            'HourPurchased': hour_purchased,
            'AvgPrice': avg_price,
            'Quantity': quantity
        })

    return extracted_data
# Configure MySQL Databse
db_config = {
    "host": config.database['host'],
    "user": config.database['user'],
    "password": config.database['password'],
    "database": config.database['database'],
}

getAllSkins()
print(datetime.now() - startTime)
