



import time
from selenium import webdriver
from selenium.webdriver.common.by import By

web = ""

def scrape_cengage(name, userName, userPass):
    import time

    if name == "cengage":
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
        username.send_keys(userName)
        #   Press Next
        page_to_scrape.find_element(By.ID, "idp-discovery-submit").click()
        #wait to load
        time.sleep(3)
        #   Input Username
        password = page_to_scrape.find_element(By.ID, "okta-signin-password")
        password.send_keys(userPass)
        #   Sign in button
        page_to_scrape.find_element(By.ID, "okta-signin-submit").click()
        #wait to load
        time.sleep(8)
        #   The Page we want
        page_to_scrape.get("https://www.webassign.net/v4cgi/student.pl?action=home/index&course=1224094,1606151&UserPass=c6d721955278892924e0df4d78ff9009")
        #wait to load
        time.sleep(8)

        #--------------------------------------------------------------------------------------

        #   Pull the name of each assignment and thier corresponding times/dates
        names = page_to_scrape.find_elements(By.CLASS_NAME, "css-4qmd1n")
        times = page_to_scrape.find_elements(By.CLASS_NAME, "css-atykpv")


        #   Each is printed
        print()
        for name, time in zip(names, times):
            print(name.text + " - " + time.text)
        print()

        #   End the webscraping
        page_to_scrape.quit()

        #----------------------------------------------------------------------------------------

        # If you want to check all the html use this:
        #--print(page_to_scrape.page_source)--
        #-------------^

def scrape_zybooks(name, userName, userPass):
    import time

    if name == "zybooks":

        #   Open Chrome
        page_to_scrape = webdriver.Chrome()

        #   Open Website
        page_to_scrape.get("https://learn.zybooks.com/signin")

        #   Input Username
        username = page_to_scrape.find_element(By.CSS_SELECTOR, "input[type='email']")
        username.send_keys(userName)
        #   Input Password
        password = page_to_scrape.find_element(By.CSS_SELECTOR, "input[type='password']")
        password.send_keys(userPass)

        time.sleep(15)
        #   Sign in button
        page_to_scrape.find_element(By.CLASS_NAME, "title").click()
        # wait to load
        time.sleep(3)
        #   The Page we want
        page_to_scrape.get(
            "https://learn.zybooks.com/zybook/UACS101YessickSpring2026?selectedPanel=assignments-panel")
        # wait to load
        time.sleep(15)

        # --------------------------------------------------------------------------------------

        #   Pull the name of each assignment and thier corresponding times/dates
        names = page_to_scrape.find_elements(By.CSS_SELECTOR, "h3[class='assignment-title my-auto primary-font-regular']")
        times = page_to_scrape.find_elements(By.CSS_SELECTOR, "div[class='due-date-text body-text text-13 flex items-center']")

        #   Each is printed
        print()
        for name, time in zip(names, times):
            print(name.text + " - " + time.text)
        print()


        #   End the webscraping
        page_to_scrape.quit()

        # ----------------------------------------------------------------------------------------

        # If you want to check all the html use this:
        #--print(page_to_scrape.page_source)--
        # -------------^

def scrape_blackboard(name, userName, userPass):
    import time

    if name == "blackboard":
        #   Open Chrome
        page_to_scrape = webdriver.Chrome()

        #   Open Website
        page_to_scrape.get("https://ualearn.blackboard.com/")

        time.sleep(5)

        page_to_scrape.find_element(By.CLASS_NAME, "button-1").click()
        #   Input Username
        username = page_to_scrape.find_element(By.ID, "user_id")
        username.send_keys(userName)
        #   Input Password
        password = page_to_scrape.find_element(By.ID, "password")
        password.send_keys(userPass)
        #   Sign in button
        page_to_scrape.find_element(By.ID, "entry-login").click()
        # wait to load
        time.sleep(8)
        #   The Page we want
        page_to_scrape.get("https://ualearn.blackboard.com/ultra/calendar")
        page_to_scrape.find_element(By.ID, "bb-calendar1-deadline").click()
        # wait to load
        time.sleep(2)

        # --------------------------------------------------------------------------------------

        #   Pull the name of each assignment and thier corresponding times/dates
        names = page_to_scrape.find_elements(By.CSS_SELECTOR,
                                             "a[ng-click='viewDueDateItem(dueDateItem)']")
        times = page_to_scrape.find_elements(By.CSS_SELECTOR,
                                             "div[class='content']")

        #   Each is printed
        print()
        for name, time in zip(names, times):
            print(name.text + " - " + time.text)
        print()

        #   End the webscraping
        page_to_scrape.quit()

        # ----------------------------------------------------------------------------------------

        # If you want to check all the html use this:
        # --print(page_to_scrape.page_source)--
        # -------------^