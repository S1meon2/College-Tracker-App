

import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import getpass

### The Goal is to get the estimated total grades for the propmted course
### This includes accounting for the grades that will be dropped

print("Your Computer Science assignments: ")


#   Open Chrome
page_to_scrape = webdriver.Chrome()

#   Open Website
page_to_scrape.get("https://ualearn.blackboard.com/")

time.sleep(5)

  # Sign in process #
page_to_scrape.find_element(By.CLASS_NAME, "button-1").click()
#   Input Username
username = page_to_scrape.find_element(By.ID, "user_id")
username.send_keys("'your_username'")
#   Input Password
password = page_to_scrape.find_element(By.ID, "password")
my_pass = "'your_password'"
password.send_keys(my_pass)
#   Sign in button
page_to_scrape.find_element(By.ID, "entry-login").click()
# wait to load
time.sleep(8)
#   The Page we want
page_to_scrape.get("https://ualearn.blackboard.com/ultra/courses/_369185_1/grades")
time.sleep(4)

# --------------------------------------------------------------------------------------

#   Pull the name of each (completed) assignment and thier corresponding grades



parent = page_to_scrape.find_element(By.XPATH, "//course-student-grades[@id='student-tab-panel-grades']")
children = parent.find_elements(By.XPATH, ".//div[contains(@class, 'MuiTypographyroot')]")

for child in children:

    print(child.text)

# Go through each layer of the html to find page # out of max page #
parent_page = page_to_scrape.find_element(By.XPATH, "//div[contains(@class, 'makeStylespaginationContainer')]")
paren_page = parent_page.find_element(By.XPATH, ".//div[contains(@class, 'makeStylesroot')]")
pare_page = paren_page.find_element(By.XPATH, ".//div[contains(@class, 'makeStylespaginationLabel')]")
par_page = pare_page.find_element(By.XPATH, ".//div[contains(@class, 'makeStylesroot')]")
page_num = par_page.find_element(By.XPATH, ".//div[contains(@class, 'makeStyleshideOffScreen')]")

print(page_num.text)




num_1 = page_num.text[5]
num_2 = page_num.text[10]

#repeat the pull untill max page is reached
if num_1 != num_2 :
    print()
    print("page: " + str(int(num_1) + 1))
    print()
    paren_page.find_element(By.XPATH, "//button[@data-analytics-id='course.student.grade.components.common.pagination.pageUpButton']").click()
    time.sleep(4)

  #same process as before (scrape grades)
    parent = page_to_scrape.find_element(By.XPATH, "//course-student-grades[@id='student-tab-panel-grades']")
    children = parent.find_elements(By.XPATH, ".//div[contains(@class, 'MuiTypographyroot')]")

    for child in children:
        print(child.text)
    time.sleep(4)
    num_1 = int(num_1) + 1


#   End the webscraping
page_to_scrape.quit()

# ----------------------------------------------------------------------------------------
# If you want to check all the html use this:
# print(page_to_scrape.page_source)
# -------------^

