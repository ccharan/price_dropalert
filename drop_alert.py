# -*- coding: utf-8 -*-
"""
Created on Sat May  8 21:19:57 2021

@author: Charan C
"""

from bs4 import BeautifulSoup
from requests import get
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from time import sleep

"""This function is used to get the product price""""
def get_product_price(url, HEADERS):
    try:
        response = get(url, headers=HEADERS)
        amazon_html = BeautifulSoup(response.text, "lxml")
        price_block = amazon_html.find('span', attrs={"id":"priceblock_saleprice"})
        product_price = price_block.string
        print(product_price)

        price_list = product_price.split()
        price_list = price_list[1].split('.')
        price = int(price_list[0].replace(',',''))
        return price
    except BaseException as e:
        print(e)

"""This function is used to get the product title"""
def get_product_title(url, HEADERS):
    try:
        response = get(url, headers=HEADERS)
        amazon_html = BeautifulSoup(response.text, "lxml")
        product_title = amazon_html.find('span', attrs={"id":"productTitle"})
        product_title = product_title.string
        product_title = product_title.lstrip().rstrip()
        print(product_title)
        return product_title
    except BaseException as e:
        print(e)


HEADERS = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})

url = 'https://www.amazon.in/All-new-Fire-TV-Stick-with-Alexa-Voice-Remote/dp/B07ZZX5ZSW'

# email details
from_email = 'xyz@gmail.com'
from_email_password = "password"
to_email = 'xyz@gmail.com'

TARGET_PRICE = 3000
SECONDS = 300

product_title = get_product_title(url, HEADERS)

mail_content = f"Hi Charan, \n\nThe Price is dropped for your product {product_title} \nURL: {url} \n\nThanks"

# run the code continuously 
while True:
    price = get_product_price(url, HEADERS)
    
    # get the price, if product price is less than expected target price, then trigger the alert mail, 
    # else keep checking the product price.
    try:
        if price < TARGET_PRICE:
            message = MIMEMultipart()
            message['From'] = from_email
            message['To'] = to_email
            message['Subject'] = f'Alert! the product price dropped to Rs:{price}'  
            # The body and the attachments for the mail
            message.attach(MIMEText(mail_content, 'plain'))
            # create SMTP session for sending the mail, use gmail with port
            session = smtplib.SMTP('smtp.gmail.com', 587)
            # enable security
            session.starttls()
            # login with mail_id and password
            session.login(from_email, from_email_password)
            text = message.as_string()
            session.sendmail(from_email, to_email, text)
            session.quit()
            print('Mail Sent successfully to ',to_email)
            # sleep for SECONDS and then again check
            sleep(SECONDS)
        else:
            print(f'Will check the product price after {SECONDS} sec')
            # sleep for SECONDS and then again check
            sleep(SECONDS)
    except BaseException as e:
        print(e)
