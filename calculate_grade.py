"""Here we have the first Grade calculation prototype. This is being tested on MATH 126 assignments.
Essentially, We webscrape past assignments then analyze each one for its type and percentage
Then calculate the final grade based off of that. This currently only works on webassign                                                                     """

####################################################################################################################

"""Hide Errors"""
import sys
import os

sys.stderr = open(os.devnull, 'w')

# We're using the (Selenium Webdriver) / Webscraper.
# We need the BY import to determine what type of HTML we pull from.
# Time will allow us to wait for web-pages to load
# If you haven't already TODO ---> pip install selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Now we need to import a LLamaExtract model so we can analyze our assignments
from pydantic import BaseModel, Field
from llama_cloud_services import LlamaExtract, SourceText

# API access to llama-cloud
os.environ["LLAMA_CLOUD_API_KEY"] = "llx###############################"
from llama_cloud_services import LlamaParse

parser = LlamaParse(
    parse_mode="parse_page_with_agent",
    model="openai-gpt-4-1-mini",
    high_res_ocr=True,
    adaptive_long_table=True,
    outlined_table_extraction=True,
    output_tables_as_HTML=True,
)


# ----------------------------------------------------------------------------------------------------

def Get_assignments():
    # Open Chrome and Minimize window
    page_to_scrape = webdriver.Chrome()
    page_to_scrape.minimize_window()
    #   Open Website
    page_to_scrape.get("https://www.webassign.net/")

    #   Press Sign In
    page_to_scrape.find_element(By.ID, "menu-item-888").click()

    # wait to load
    time.sleep(3)

    #   Input Username
    username = page_to_scrape.find_element(By.ID, "idp-discovery-username")
    username.send_keys("/Your Email/")

    #   Press Next
    page_to_scrape.find_element(By.ID, "idp-discovery-submit").click()

    # wait to load
    time.sleep(3)

    #   Input Username
    password = page_to_scrape.find_element(By.ID, "okta-signin-password")
    my_pass = "/Your password/"
    password.send_keys(my_pass)

    #   Sign in button
    page_to_scrape.find_element(By.ID, "okta-signin-submit").click()

    # wait to load
    time.sleep(3)

    #   The Page we want aka page where your assignments are
    page_to_scrape.get("https://www.webassign.net/v4cgi/student.pl?v=20260119051104indmind02@gmail.com@ua")

    # wait to load
    time.sleep(5)

    # Wait for the button to be clickable
    button = WebDriverWait(page_to_scrape, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Show Past Assignments']"))
    )

    # Scroll into view and click using JavaScript
    page_to_scrape.execute_script("arguments[0].scrollIntoView(true);", button)
    page_to_scrape.execute_script("arguments[0].click();", button)

    time.sleep(5)
    # --------------------------------------------------------------------------------------

    #   Pull the name of each assignment and thier corresponding grades
    names = page_to_scrape.find_elements(By.CLASS_NAME, "css-f213dh")
    score = page_to_scrape.find_elements(By.CLASS_NAME, "css-5p1x5e")

    return names, score


def Calculate(names, score):
    # How much homework
    h = 0
    # How many quizzes
    q = 0

    # Homework average
    hw = 0
    # Quiz average
    qz = 0

    # initialize HW Array
    homework_list = []
    # initialize QZ Array
    quiz_list = []

    # initialize Total Grade Percent
    total = 0

    # -------------------------------------------------------------------------------------------------

    for name, scor in zip(names, score):
        print("---------------------------------------------------------")
        print(name.text + " (" + scor.text + ") ")

        # Extraction Instructions you can change this to fit whatever assignments you have
        class Syllabus(BaseModel):
            type: str = Field(
                description="Determine the type of assignment this is and only output the type. If the text includes 'topic' then output: homework. If the text includes 'quiz' then output: quiz, anything that is pre-test or review does not have a type")
            percent: str = Field(
                description="Determine the percent based on calculating the fraction given, do not include the percent symbol in the output, output should look like this for example, if given 1 / 10 the output would be: 10 or 10.0, if given 18.5 / 20 the output would be:   92.5")

        extractor = LlamaExtract()

        # Create or Use existing extraction agent, comment out which one you're not using
        """agent = extractor.create_agent(name="Check_Percent6", data_schema= Syllabus)"""
        agent = extractor.get_agent(name="Check_Percent6")

        # Analyze assignment name and grade
        name_result = agent.extract(SourceText(text_content=name.text))
        grade_result = agent.extract(SourceText(text_content=scor.text))

        # Print Result of analysis, which in this case is assignment type and grade percent
        print(f"Assignment Type: {name_result.data['type']}")
        print(f"Grade on this assignment: {grade_result.data['percent']}")

        # homework count and add homework grade to the homework list
        if f"{name_result.data['type']}" == "homework":
            h = h + 1
            homework_list.append(float(f"{grade_result.data['percent']}"))

        # quiz count and add quiz grade to the quiz list
        if f"{name_result.data['type']}" == "quiz":
            q = q + 1
            quiz_list.append(float(f"{grade_result.data['percent']}"))

    # Add each homework then divide by homework count
    for homework in homework_list:
        hw = hw + homework
    hw = hw / h
    # Add each quiz then divide by quiz count
    for quiz in quiz_list:
        qz = qz + quiz
    qz = qz / q

    # get total grade
    total = (qz + hw) / 2

    print()
    print("---------------------------------------------------------------------")
    print("Your estimated grade is: " + str(total) + "%")
    print("---------------------------------------------------------------------")


Calculate(*Get_assignments())

