import sqlite3
from Assignment_WEB import scrape_cengage, scrape_zybooks, scrape_blackboard, scrape_demo

# Global variable to hold the in-memory database connection
mem_connection = None

def get_mem_connection():
    """
    Creates and returns a single in-memory database connection.
    Initializes tables if the connection is new.
    """
    global mem_connection
    if mem_connection is None:
        mem_connection = sqlite3.connect(':memory:')
        control = mem_connection.cursor()
        # Create login table for in-memory use
        control.execute("""CREATE TABLE IF NOT EXISTS
            login (name TEXT, username TEXT, password TEXT, isSigned TEXT)
        """)
        # Create class table for in-memory use
        control.execute("""CREATE TABLE IF NOT EXISTS
            class (classname TEXT, webname TEXT, classid TEXT, assignmentpage TEXT, isSigned BLOB)
        """)
    return mem_connection


def create_login_table():
    connection = sqlite3.connect('ububble.db')

    control = connection.cursor()

    control.execute("""CREATE TABLE IF NOT EXISTS
    
        login (name TEXT, username TEXT, password TEXT, isSigned BLOB)
    
    """)

def create_class_table():
    connection = sqlite3.connect('ububble.db')

    control = connection.cursor()

    control.execute("""CREATE TABLE IF NOT EXISTS

        class (name TEXT, website TEXT, id TEXT)

    """)

def create_account_table():
    connection = sqlite3.connect('ububble.db')

    control = connection.cursor()

    control.execute("""CREATE TABLE IF NOT EXISTS

        account (username TEXT, pin TEXT, login TEXT, classes TEXT)

    """)

########################################################################################################################

def send_login(name, userName, userPass, isSigned):
    data = (name, userName, userPass, isSigned)

    if isSigned != "user":

        connection = sqlite3.connect("ububble.db")

        control = connection.cursor()

        control.execute("""CREATE TABLE IF NOT EXISTS

                        login (name TEXT, username TEXT, password TEXT, isSigned TEXT)

                    """)

        control.execute("INSERT OR IGNORE INTO login VALUES (?, ?, ?, ?)", data)

        connection.commit()
        connection.close()

        print( name + " has been connected!")

    else:
        print("in memory to send")
        memConnection = get_mem_connection()
        memControl = memConnection.cursor()
        memControl.execute("INSERT OR IGNORE INTO login VALUES (?, ?, ?, ?)", data)
        memConnection.commit()
        # Do not close the connection, as it's shared.

        print(name + " has been connected! (in memory)")

def recieve_scraped(name, isSigned):
    if isSigned != "user":
        connection = sqlite3.connect('ububble.db')
        control = connection.cursor()
        control.execute("SELECT * FROM login")
        logins = control.fetchall()

        all_data = ""

        if name == "All":
            for login in logins:

                if login[0] == "cengage" and login[3] == isSigned:
                    all_data += scrape_cengage(login[0], login[1], login[2])

                if login[0] == "zybooks" and login[3] == isSigned:
                    all_data += scrape_zybooks(login[0], login[1], login[2])

                if login[0] == "blackboard" and login[3] == isSigned:
                    all_data += scrape_blackboard(login[0], login[1], login[2])

                if login[0] == "demo" and login[3] == isSigned:
                    all_data += scrape_demo(login[1], login[2], "file:///C:/Users/indmi/Documents/Codex/2026-06-25/i/outputs/mock-edu-portal.html")
    else:
        print("In memory to recieve")
        connection = get_mem_connection()
        memControl = connection.cursor()
        memControl.execute("SELECT * FROM login")
        logins = memControl.fetchall()

        all_data = ""

        if name == "All":
            for login in logins:

                if login[0] == "cengage" and login[3] == isSigned:
                    all_data += scrape_cengage(login[0], login[1], login[2])

                if login[0] == "zybooks" and login[3] == isSigned:
                    all_data += scrape_zybooks(login[0], login[1], login[2])

                if login[0] == "blackboard" and login[3] == isSigned:
                    all_data += scrape_blackboard(login[0], login[1], login[2])

                if login[0] == "demo" and login[3] == isSigned:
                    all_data += scrape_demo(login[1], login[2],"file:///C:/Users/indmi/Documents/Codex/2026-06-25/i/outputs/mock-edu-portal.html")
    return all_data




def send_class(classname, webname, classid, assignmentpage, isSignedIn):
    data = (classname, webname, classid, assignmentpage, isSignedIn)

    if isSignedIn != "":

        connection = sqlite3.connect("classes.db")

        control = connection.cursor()

        control.execute("""CREATE TABLE IF NOT EXISTS

                        class (classname TEXT, webname TEXT, classid TEXT, assignmentpage TEXT, isSigned BLOB)

                    """)

        control.execute("INSERT OR IGNORE INTO class VALUES (?, ?, ?, ?, ?)", data)

        connection.commit()
        connection.close()

        print(classname + " has been added and can now be scraped!")

    else:

        memConnection = get_mem_connection()
        memControl = memConnection.cursor()
        # The table is now created in get_mem_connection, and the schema is corrected.
        # The data tuple has 5 elements, so we need 5 placeholders.
        memControl.execute("INSERT OR IGNORE INTO class VALUES (?, ?, ?, ?, ?)", data)
        memConnection.commit()
        # Do not close the connection.

        print(classname + " has been added and can now be scraped!")


"""Manually delete Tables & Data"""
connection = sqlite3.connect('ububble.db')
control = connection.cursor()
#control.execute("DROP TABLE class")
#control.execute(" DELETE FROM login WHERE name = 'blackboard' ")
connection.commit()
connection.close()