import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import time
import json
import google.generativeai as genai

def setup_gemini(api_key):
    """Initializes the Gemini model."""
    genai.configure(api_key=api_key)

    # We use Flash because it's fast and perfect for parsing simple text like assignments
    model = genai.GenerativeModel('gemini-2.5-flash')
    return model

# Configure your Gemini API Key here
GENAI_API_KEY = "your_apikey"
genai.configure(api_key=GENAI_API_KEY)

#############################################################################################



def extract_assignments(raw_text):
    """Uses Gemini to turn scraped text into a list of structured assignments."""

    # We use Flash because it's the fastest and cheapest for this task
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        generation_config={"response_mime_type": "application/json"}
    )

    prompt = f"""
    I am going to give you raw text scraped from a university website. 
    Extract every assignment, quiz, or project mentioned.

    Return a JSON list of objects. Each object must have:
    - 'title': The name of the assignment (e.g., 'Calculus HW 4')
    - 'due_date': The date in YYYY-MM-DD format. If only a day of the week is mentioned, 
      assume it refers to the upcoming occurrence of that day from today's date ({datetime.date.today()}).

    Raw Scraped Text:
    {raw_text}
    """

    response = model.generate_content(prompt)

    # Because we requested JSON mode, we can safely load the text as a list
    assignments = json.loads(response.text)
    return assignments


# This scope allows your app to read and write to the user's Google Tasks
SCOPES = ['https://www.googleapis.com/auth/tasks']


def get_tasks_service():
    """Handles the OAuth 2.0 flow and returns a Google Tasks service object."""
    creds = None

    # The file token.json stores the user's access and refresh tokens.
    # It is created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # This requires the 'credentials.json' file you downloaded from Google Cloud
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Create the service object to interact with Google Tasks
    return build('tasks', 'v1', credentials=creds)


def sync_assignments_to_tasks(raw_scraped_text):
    print("AI is processing assignments...")
    try:
        assignments = extract_assignments(raw_scraped_text)
        service = get_tasks_service()

        for item in assignments:
            # 1. Define the task_body INSIDE the loop for each assignment
            task_body = {
                'title': item['title'],
                'due': f"{item['due_date']}T23:59:59Z"
            }

            # 2. Insert the task to the @default list INSIDE the loop
            result = service.tasks().insert(tasklist='@default', body=task_body).execute()

            # 3. Print the success message with the Task ID
            print(f"Successfully added: {result.get('title')} | Task ID: {result.get('id')}")

            # Wait 1 second between tasks to avoid hitting Google Tasks limits
            time.sleep(1)

        # This prints only after the loop finishes successfully
        print("\nAll assignments have been synced to your Google Tasks!")

    except Exception as e:
        if "429" in str(e):
            print("Rate limit hit. Waiting 60 seconds...")
            time.sleep(60)
        else:
            print(f"Error: {e}")




    ###DEBUG

def check_task_lists():
    service = get_tasks_service()

    # Ask Google for all your task lists
    results = service.tasklists().list(maxResults=10).execute()
    items = results.get('items', [])

    print("\n--- Your Google Task Lists ---")
    if not items:
        print("No task lists found.")
    else:
        for item in items:
            print(f"List Name: {item['title']} | List ID: {item['id']}")


