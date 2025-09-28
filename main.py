import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import getpass

#   Open Chrome
page_to_scrape = webdriver.Chrome()

#   Open Website
page_to_scrape.get("https://www.webassign.net/")

#   Press Sign In
page_to_scrape.find_element(By.ID, "menu-item-888").click()
#wait to load
time.sleep(3)
#   Input Username
username = page_to_scrape.find_element(By.ID, "idp-discovery-username")
username.send_keys(/'put username here'/)
#   Press Next
page_to_scrape.find_element(By.ID, "idp-discovery-submit").click()
#wait to load
time.sleep(3)
#   Input Username
password = page_to_scrape.find_element(By.ID, "okta-signin-password")
my_pass = /'put password here'/
password.send_keys(my_pass)
#   Sign in button
page_to_scrape.find_element(By.ID, "okta-signin-submit").click()
#wait to load
time.sleep(8)
#   The Page we want
page_to_scrape.get("https://www.webassign.net/v4cgi/student.pl?action=home/index&course=1184427,1560186&UserPass=854347c687428fbda172c9195f97c9e5")
#wait to load
time.sleep(8)

#--------------------------------------------------------------------------------------

#   Pull the name of each assignment and thier corresponding times/dates
names = page_to_scrape.find_elements(By.CLASS_NAME, "css-4qmd1n")
times = page_to_scrape.find_elements(By.CLASS_NAME, "css-atykpv")

#   Each is printed
for name, time in zip(names, times):
    print(name.text + " - " + time.text)

#   End the webscraping
page_to_scrape.quit()

#----------------------------------------------------------------------------------------

# If you want to check all the html use this:
#--print(page_to_scrape.page_source)--
#-------------^
