"""Welcome to U-Bubble's Web Scraper!"""
# Selenium Imports
from selenium import webdriver
from selenium.webdriver.common.by import By
####################################################################################################################################

def scrape_demo(userName, userPass, assignmentPage):

    import time # Logic needed for pauses in webscraping scripts
    if assignmentPage:
        #   Open Chrome
        page_to_scrape = webdriver.Chrome()

        #   Open Website
        page_to_scrape.get(assignmentPage)

        time.sleep(5)


        #   Input Username
        username = page_to_scrape.find_element(By.ID, "username")
        username.send_keys(userName)
        #   Input Password
        password = page_to_scrape.find_element(By.ID, "password")
        password.send_keys(userPass)
        #   Sign in button
        page_to_scrape.find_element(By.ID, "sign-in-button").click()
        # wait to load
        time.sleep(8)
        #   The Page we want
        #page_to_scrape.get("file:///C:/Users/indmi/Documents/Codex/2026-06-25/i/outputs/mock-edu-portal.html")
        # wait to load
        time.sleep(2)

        # --------------------------------------------------------------------------------------

        #   Pull the name of each assignment and thier corresponding times/dates
        courseName = page_to_scrape.find_elements(By.CLASS_NAME, "course-name")
        names = page_to_scrape.find_elements(By.CLASS_NAME, "assignment-title")
        times = page_to_scrape.find_elements(By.CLASS_NAME, "due-date")

        all = ""
        #   Each is printed
        print()
        for courseName, name, time in zip(courseName,names,times):
            print(courseName.text + ": " + name.text + " - " + time.text)
            all += courseName.text + ": " + name.text + " - " + time.text
        print()

        return all

        #   End the webscraping
        page_to_scrape.quit()

    #scrape_demo("username","password","file:///C:/Users/indmi/Documents/Codex/2026-06-25/i/outputs/mock-edu-portal.html")


#####################################################################################################################################
def scrape_zybooks(userName, userPass, assignmentPage):
    import time
    if assignmentPage:
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
        page_to_scrape.get("https://learn.zybooks.com/zybook/UACS101YessickSpring2026?selectedPanel=assignments-panel")
        # wait to load
        time.sleep(15)

        # --------------------------------------------------------------------------------------

        #   Pull the name of each assignment and thier corresponding times/dates
        names = page_to_scrape.find_elements(By.CSS_SELECTOR, "h3[class='assignment-title my-auto primary-font-regular']")
        times = page_to_scrape.find_elements(By.CSS_SELECTOR, "div[class='due-date-text body-text text-13 flex items-center']")

        all = ""
        #   Each is printed
        print()
        for name, time in zip(names, times):
            print(name.text + " - " + time.text)
            all += " " + name.text + " - " + time.text
        print()

        #   End the webscraping
        page_to_scrape.quit()
        return all

        # ----------------------------------------------------------------------------------------

        # If you want to check all the html use this:
        #--print(page_to_scrape.page_source)--
        # -------------^

######################################################################################################################################################
def scrape_blackboard(userName, userPass, assignmentPage):
    import time
    if assignmentPage:
        #   Open Chrome
        page_to_scrape = webdriver.Chrome()

        #   Open Website
        page_to_scrape.get("https://ualearn.blackboard.com/")

        time.sleep(5)

        page_to_scrape.find_element(By.CLASS_NAME, "button-1").click()
        print("Clicked OK")

        '''Click Login with bamaid'''
        page_to_scrape.find_element(By.XPATH, "//div[@id='login-block']//button[contains(text(), 'Login with myBama ID')]").click()
        print("Clicked Login with myBama ID")

        #   Input Username (may need to fix)
        username = page_to_scrape.find_element(By.ID, "identifier")
        username.send_keys(userName)
        print("Entered Username")

        '''Click Next'''
        page_to_scrape.find_element(By.XPATH, "//button[@data-se='save' and text()='Next']").click()
        print("Clicked Next")

        time.sleep(5)

        #   Input Password (may need to fix)
        password = page_to_scrape.find_element(By.ID, "credentials.passcode")
        password.send_keys(userPass)
        print("Entered Password")

        #   Verify button (may need to fix)
        page_to_scrape.find_element(By.XPATH, "//button[@data-se='save' and text()='Verify']").click()
        print("Clicked Verify")

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

        all = ""
        #   Each is printed
        print()
        for name, time in zip(names, times):
            print(name.text + " - " + time.text)
            all += " " + name.text + " - " + time.text
        print()

        #   End the webscraping
        page_to_scrape.quit()
        return all
        # ----------------------------------------------------------------------------------------

        # If you want to check all the html use this:
        # --print(page_to_scrape.page_source)--
        # -------------^

#####################################################################################################################################
def scrape_cengage(userName, userPass, assignmentPage):
    import time
    if assignmentPage:
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
        page_to_scrape.get(assignmentPage)
        #wait to load
        time.sleep(8)

        #--------------------------------------------------------------------------------------

        #   Pull the name of each assignment and thier corresponding times/dates
        names = page_to_scrape.find_elements(By.CLASS_NAME, "css-4qmd1n")
        times = page_to_scrape.find_elements(By.CLASS_NAME, "css-atykpv")

        all = ""
        #   Each is printed
        print()
        for name, time in zip(names, times):
            print(name.text + " - " + time.text)
            all += " " + name.text + " - " + time.text
        print()

        #   End the webscraping
        page_to_scrape.quit()
        return all

        #----------------------------------------------------------------------------------------

        # If you want to check all the html use this:
        #--print(page_to_scrape.page_source)--
        #-------------^

#########################################################################################################################################333