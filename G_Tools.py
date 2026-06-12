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
with open("api_key.txt", "r") as f:
    GENAI_API_KEY = f.read().strip()
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
       - 'title': The name of the assignment
       - 'due_date': The date in YYYY-MM-DD format. Today's date is {datetime.date.today()}.
       - 'due_time': The specific time it is due in 12-hour HH:MM am or pm format (e.g., '2:30 pm' or '11:59 pm'). If no time is mentioned, default to '11:59 pm'.


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


       # --- NEW STEP: Scan for duplicates across ALL lists ---
       print("Scanning current tasks to prevent duplicates...")
       existing_task_titles = []


       # Get all lists
       tasklists_result = service.tasklists().list().execute()
       for t_list in tasklists_result.get('items', []):
           # Get all tasks in each list (showHidden=True includes completed tasks)
           tasks_result = service.tasks().list(tasklist=t_list['id'], showHidden=True).execute()
           for t in tasks_result.get('items', []):
               # We save the title of every task you currently have
               existing_task_titles.append(t['title'])


       # Get today's date for the past-due filter
       today = datetime.date.today()


       for item in assignments:
           due_date_obj = datetime.datetime.strptime(item['due_date'], "%Y-%m-%d").date()


           # This is what the title will look like
           formatted_title = f"{item['title']} (Due: {item['due_time']})"


           # Filter 1: Is it due today or in the future?
           if due_date_obj >= today:


               # Filter 2: Does it already exist?
               # We check if the base assignment title is ANYWHERE inside your existing tasks
               is_duplicate = any(item['title'] in existing_title for existing_title in existing_task_titles)


               if is_duplicate:
                   print(f"Skipped duplicate: '{item['title']}' already exists.")
                   continue  # This skips the rest of the loop and moves to the next assignment


               # If it's not a duplicate, build and insert it
               task_body = {
                   'title': formatted_title,
                   'notes': f"Exact Due Time: {item['due_time']}",
                   'due': f"{item['due_date']}T00:00:00Z"
               }


               # Inserting into your specific "HW and Assignments" list
               result = service.tasks().insert(tasklist='YTAwSUV3aEgzU0N5QUNOXw', body=task_body).execute()
               print(f"Successfully added: {result.get('title')} | Task ID: {result.get('id')}")


               time.sleep(1)  # Prevent 429 errors
           else:
               print(f"Skipped past assignment: {item['title']} (Was due: {item['due_date']})")


       print("\nAll future, non-duplicate assignments have been synced to your Google Tasks!")


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