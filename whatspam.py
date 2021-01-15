#  Created by Florian-Mahlberg https://github.com/Florian-Mahlberg/
#  On thursday, the 14th january
#  Orginal by zensajnani https://github.com/zensajnani/whatsapp_bot

import time
import pickle
import random
import sys
import string
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.common.exceptions import InvalidArgumentException, NoSuchElementException, InvalidSessionIdException
from selenium.webdriver.support import expected_conditions as EC
from urllib3.exceptions import MaxRetryError
import requests

# variable to store the name of the contact
contact = "Testing"
#variable to store message
message = "Hi, this is a automated Text message by https://github.com/Florian-Mahlberg/whatspam"
timeForFor = 20
time_for_ending_servers = 60
answer = "answer"
url = "https://web.whatsapp.com"
rightInfos = False
exitProgramm = False


#Wait for Code
def wait_for_code():
    try:
        element = driver.find_element_by_xpath('//*[@id="side"]/div[1]/div/label/div/div[2]')
    except NoSuchElementException:
        return False
    if(element.is_displayed() == True):
        return True
    else:
        return False

#Checks infos
def check_contact_info():
    try:
        while True:
            answer = input('\n'+'\n'+"Are these info's correct: " + '\n' + "Contact: " + contact+ '\n' + "Message: " + message + '\n' + "Time to spam: " + str(timeForFor) + '\n'+ "y/n: ")
            if answer[0] == "y":
                return True
            else:
                if answer[0] == "n":
                    return False
    except IndexError:
        return False

#Sets infos
def set_contact():
    loc = input("Please input contact's name: ")
    if loc == "" or loc == " ":
        return "Testing"
    else:
        return loc

def set_message():
    loc = input("Please input message to spam: ")
    if loc == "" or loc == " ":
        return "Hi, this is a automated Text message by https://github.com/Florian-Mahlberg/whatspam"
    else:
        return loc

def set_times():
    try:
        return int(input("Please input time to spam: "))
    except ValueError:
        return 20

#finding search bar
def find_contact(contact):
    inp_xpath_search = '//*[@id="side"]/div[1]/div/label/div/div[2]'
    inp_xpath_cancel = '//*[@id="side"]/div[1]/div/button/div[2]'
    input_box_search = WebDriverWait(driver, 50).until(lambda driver: driver.find_element_by_xpath(inp_xpath_search))
    cancel = driver.find_element_by_xpath(inp_xpath_cancel)
    input_box_search.click() #clicks on search bar
    time.sleep(0)
    input_box_search.send_keys(contact) #enters name of contact
    time.sleep(0.2)

    try:
        #finds contact
        selected_contact = driver.find_element_by_xpath("//span[@title='"+contact+"']")
        selected_contact.click() # select contact
        time.sleep(0.2)
        cancel.click()
    except NoSuchElementException:
        time.sleep(0.2)
        cancel.click()
    except StaleElementReferenceException:
        time.sleep(0.2)
        cancel.click()

#find message box
def send_message(message):
    inp_xpath = '//*[@id="main"]/footer/div[1]/div[2]/div/div[2]'
    input_box = driver.find_element_by_xpath(inp_xpath)
    time.sleep(0.2)
    input_box.send_keys(message + Keys.ENTER) #enters message
    time.sleep(0)

#check if, the contact exist
def exist_contact(contact):
    inp_xpath_search = '//*[@id="side"]/div[1]/div/label/div/div[2]'
    inp_xpath_cancel = '//*[@id="side"]/div[1]/div/button/div[2]'
    input_box_search = WebDriverWait(driver, 50).until(lambda driver: driver.find_element_by_xpath(inp_xpath_search))
    cancel = driver.find_element_by_xpath(inp_xpath_cancel)
    input_box_search.click() #clicks on search bar
    time.sleep(0)
    input_box_search.send_keys(contact) #enters name of contact
    time.sleep(0.2)

    try:
        #finds contact
        selected_contact = driver.find_element_by_xpath("//span[@title='"+contact+"']")
        time.sleep(0.2)
        selected_contact.click() # select contact
        time.sleep(0.2)
        cancel.click()
        return True
    except NoSuchElementException:
        time.sleep(0.2)
        cancel.click()
        return False

#Func that returns aria label and sends message
def for_send_message(count, messages, timeForFor):
    send_message(f'{message} {count+1}/{timeForFor}')
    btn = driver.find_element_by_xpath('//*[@id="main"]/div[3]/div/div/div[3]/div[last()]/div/div/div/div[2]/div/div')
    return btn.find_element_by_css_selector('span').get_attribute("aria-label")

#open a Whatsapp Web interface which automatically asks you to scan the QR code
options = webdriver.ChromeOptions()
options.add_argument("user-data-dir=/Users/flo/Library/Application Support/Google/Chrome/Default")
options.add_argument("--app=https://web.whatsapp.com")
print("Please wait, while loading")
try:
    driver = webdriver.Chrome(executable_path="./chromedriver", options=options)
except InvalidArgumentException:
    print('\n'+ '\n'+ "I wanted to start Chrome, but you started it already." + '\n'+ "Please close it, so I can create a fresh browser webpage!"+ '\n'+ '\n')
    sys.exit()

#try, to check ctrl+c
try:
    #Waits for QR code
    while wait_for_code() == False:
        time.sleep(0.5)

    #waits until all Infos are correct
    while True:
        while rightInfos == False:
            contact = set_contact()
            message = set_message()
            try:
                timeForFor = set_times()
            except ValueError:
                timeForFor = 20
            rightInfos = check_contact_info()

        if(exist_contact(contact) == True):
            rightInfos = True
            break

    #clicks on the right contact
    find_contact(contact)

    #prints the automated message multiple times
    for count in range(timeForFor):
        aria_label = for_send_message(count, message, timeForFor)

    #Waits until all messages are send (max 30 sec). Else pings to whatsapp.com and checks, if the phone has no Internet connection
    i = 0
    while str(aria_label) == " Pending ":
        print("Contacting WhatsApp Servers " + str(i/2) + "/" + str(time_for_ending_servers/2))
        try:
            aria_label = btn.find_element_by_css_selector('span').get_attribute("aria-label")
        except MaxRetryError:
            response = os.system("ping -c 1 " + "whatsapp.com")
            if response == 0:
                print("Can't reach your phone, please check, if your Phone has a stable connection!")
            else:
                print("Can't contact the WhatsApp Servers, please check, that your Phone and Computer has a stable connection.")
            try:
                driver.close()
                driver.quit()
            except MaxRetryError:
                sys.exit()
        i = i + 1
        if i >= time_for_ending_servers:
            driver.close()
            driver.quit()
            exitProgramm = False
        time.sleep(0.5)

    try:
        driver.close()
        exitProgramm = False
    except ProtocolError:
        time.sleep(0)
    exitProgramm = False
finally:
    #This code will run after the rest
    if exitProgramm == True:
        #This code will run, after an error or Ctrl+c
        try:
            btn = driver.find_element_by_xpath('//*[@id="main"]/div[3]/div/div/div[3]/div[last()]/div/div/div/div[2]/div/div')
            aria_label = btn.find_element_by_css_selector('span').get_attribute("aria-label")

            print(" <- Thats a Ctrl+C ? I'll stop for you! Please don't press Ctrl+C until the programm is closed.")
            print("Waiting for messages, that didn't want to go to the Server...")

            #Waits until all Messages are send (max 30 sec.)
            i = 0
            while str(aria_label) == "Pending":
                print("Contacting WhatsApp Servers " + str(i/2) + "/" + str(time_for_ending_servers/2))
                aria_label = btn.find_element_by_css_selector('span').get_attribute("aria-label")
                i = i + 1
                if i >= range(time_for_ending_servers):
                    driver.close()
                    driver.quit()
                time.sleep(0.5)
            time.sleep(1)
            driver.close()
        #To many errors, if the Phone has no Internet (or Computer)
        except InvalidSessionIdException:
            time.sleep(0)
        except NoSuchElementException:
            time.sleep(0)
        except MaxRetryError:
            time.sleep(0)
    print("Bye, I hope you come back and don't forget me!")
