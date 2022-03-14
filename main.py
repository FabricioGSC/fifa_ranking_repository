#!/usr/bin/python3
from cmath import exp
from dataclasses import dataclass
from timeit import repeat
from selenium import webdriver
from bs4 import BeautifulSoup
import os, time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import convert_csv

driver = webdriver.Firefox()

new_files = []
next_page_button = None

def main():
    time.sleep(5.0)
    men_ranking()
    women_ranking()
    convert_csv.convert
    

def men_ranking():
    driver.get('https://www.fifa.com/fifa-world-ranking/men')
    download('men')
    print('Finish to download men\'s ranking table')

def women_ranking():
    driver.get('https://www.fifa.com/fifa-world-ranking/women')
    download('women')
    print('Finish to download women\'s ranking table')

def download(origin: str):

    print(f'Starting Download for {origin}')
    
    time.sleep(2.0)
    check_button_of_trust()
    time.sleep(1.0)

    driver.maximize_window()

    drops = driver.find_elements(By.CLASS_NAME, 'ff-dropdown_dropupContentButton__3WmBL')
    print(f'We\'ve found {len(drops)} updates from this website')

    selector = driver.find_element(By.CSS_SELECTOR, '.card-heading-tiny')
    
    find_next_button()

    for drop in drops:
        date_value: str = drop.get_attribute('innerText')
        date_value = date_value.replace(' ','_')
        
        # Not continue to check other dates
        if(check_if_already_exists(date_value, origin)):
            break
        else:
            next_page_button.send_keys(Keys.HOME)
            time.sleep(1.0)
            selector.click()
            drop.click()
            time.sleep(2.0)
            download_table(date_value, origin)


    time.sleep(5.0)

def check_button_of_trust():
    try:
        button = driver.find_element(By.ID, 'onetrust-accept-btn-handler')
        button.click()
        print('Closing message about cookies ...')
    except:
        pass    
        

def check_if_already_exists(date_value: str, origin: str) -> bool:
    print(date_value)

    try:
        print(os.makedirs(f'{origin}/{date_value}'))
    except:
        print(f'The download of {date_value} has already done')
        return True
    
    return False

def download_table(date_value, origin):
    page_count = 0
    while True:

        file = open(f'{origin}/{date_value}/{date_value}_{page_count}.html', 'a')
        file.write(driver.page_source)
        file.close()

        try:
            next_page_button.click()
            page_count += 1
            time.sleep(1)
        except:
            break

def find_next_button():
    global next_page_button
    all_buttons = driver.find_elements(By.TAG_NAME, 'button')
    
    all_buttons.reverse()
    
    for button in all_buttons:
        aria_label: str = button.get_attribute('aria-label')
        
        if(aria_label != None and aria_label.startswith('Next')):
            next_page_button = button
            
            print('we found the magic button')
            break




if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f'Bad things occured ... =( \n {e}')
    finally:
        driver.close()
        print('Program is finished ...')


