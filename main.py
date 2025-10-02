while (True) :
    import csv
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.by import By
    import time
    import getpass

    print("What website do you need to get your homework from?  Options: Cengage, zyBooks, Blackboard --> ")
    web = input()

    if web == "Cengage":
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
        username.send_keys("/*username*/")
        #   Press Next
        page_to_scrape.find_element(By.ID, "idp-discovery-submit").click()
        #wait to load
        time.sleep(3)
        #   Input Username
        password = page_to_scrape.find_element(By.ID, "okta-signin-password")
        my_pass = "/*password*/"
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

    if web == "zyBooks":
        #   Open Chrome
        page_to_scrape = webdriver.Chrome()

        #   Open Website
        page_to_scrape.get("https://learn.zybooks.com/signin")

        #   Input Username
        username = page_to_scrape.find_element(By.CSS_SELECTOR, "input[type='email']")
        username.send_keys("/*email*/")
        #   Input Password
        password = page_to_scrape.find_element(By.CSS_SELECTOR, "input[type='password']")
        my_pass = "/*password*/"
        password.send_keys(my_pass)
        #   Sign in button
        page_to_scrape.find_element(By.CLASS_NAME, "title").click()
        # wait to load
        time.sleep(8)
        #   The Page we want
        page_to_scrape.get(
            "https://learn.zybooks.com/zybook/UACS100Fall2025?selectedPanel=assignments-panel")
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

    if web == "Blackboard":
        #   Open Chrome
        page_to_scrape = webdriver.Chrome()

        #   Open Website
        page_to_scrape.get("https://ualearn.blackboard.com/")

        time.sleep(5)

        page_to_scrape.find_element(By.CLASS_NAME, "button-1").click()
        #   Input Username
        username = page_to_scrape.find_element(By.ID, "user_id")
        username.send_keys("/*username*/")
        #   Input Password
        password = page_to_scrape.find_element(By.ID, "password")
        my_pass = "/*password*/"
        password.send_keys(my_pass)
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
