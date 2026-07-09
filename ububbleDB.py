import sqlite3
from Assignment_WEB import scrape_cengage, scrape_zybooks, scrape_blackboard, scrape_demo
from kivymd.app import MDApp

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
            class (classname TEXT, webname TEXT, classid TEXT, assignmentpage TEXT, isSigned TEXT)
        """)
        # Create account table for in-memory use
        control.execute("""CREATE TABLE IF NOT EXISTS
            account (username TEXT, pin INTEGER)
        """)
    return mem_connection


def create_login_table():
    connection = sqlite3.connect('ububble.db')

    control = connection.cursor()

    control.execute("""CREATE TABLE IF NOT EXISTS
    
        login (name TEXT, username TEXT, password TEXT, isSigned TEXT)
    
    """)

    connection.commit()
    connection.close()

def create_class_table():
    connection = sqlite3.connect('ububble.db')

    control = connection.cursor()

    control.execute("""CREATE TABLE IF NOT EXISTS

        class (name TEXT, website TEXT, id TEXT)

    """)

    connection.commit()
    connection.close()

def create_account_table():
    connection = sqlite3.connect('ububble.db')

    control = connection.cursor()

    control.execute("""CREATE TABLE IF NOT EXISTS

        account (username TEXT, pin INTEGER)

    """)

    connection.commit()
    connection.close()

########################################################################################################################

def send_login(name, userName, userPass, isSigned):
    data = (name, userName, userPass, isSigned)

    if isSigned != "user":

        connection = sqlite3.connect("ububble.db")

        control = connection.cursor()

        create_login_table()

        control.execute("INSERT OR IGNORE INTO login VALUES (?, ?, ?, ?)", data)

        connection.commit()
        connection.close()

        MDApp.get_running_app().show_notif(name + " site has been connected!", "success")
        print( name + "site has been connected!")

    else:
        memConnection = get_mem_connection()
        memControl = memConnection.cursor()
        memControl.execute("INSERT OR IGNORE INTO login VALUES (?, ?, ?, ?)", data)
        memConnection.commit()
        # Do not close the connection, as it's shared.

        MDApp.get_running_app().show_notif(name + " site has been connected!", "success")
        print(name + " site has been connected! (in memory)")

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
        print("Working in memory...")
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

    if isSignedIn != "user":

        connection = sqlite3.connect("ububble.db")

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

def get_classes(isSignedIn):
    if isSignedIn != "user":
        connection = sqlite3.connect('ububble.db')
        control = connection.cursor()
        control.execute("SELECT classname, webname FROM class WHERE isSigned=?", (isSignedIn,))
        classes = control.fetchall()
        connection.close()
        return classes
    else:
        memConnection = get_mem_connection()
        memControl = memConnection.cursor()
        memControl.execute("SELECT classname, webname FROM class WHERE isSigned=?", (isSignedIn,))
        classes = memControl.fetchall()
        return classes

def delete_class(classname, isSignedIn):
    if isSignedIn != "user":
        connection = sqlite3.connect('ububble.db')
        control = connection.cursor()
        control.execute("DELETE FROM class WHERE classname=? AND isSigned=?", (classname, isSignedIn))
        connection.commit()
        connection.close()
    else:
        memConnection = get_mem_connection()
        memControl = memConnection.cursor()
        memControl.execute("DELETE FROM class WHERE classname=? AND isSigned=?", (classname, isSignedIn))
        memConnection.commit()

def send_account(username, pin):
    data = (username,pin)
    connection = sqlite3.connect('ububble.db')
    control = connection.cursor()
    create_account_table()

    # Query to check if the specific account already exists
    control.execute("SELECT * FROM account WHERE username = ? AND pin = ?", data)
    existing_account = control.fetchone()

    if existing_account:
        print("Signing you back in...")
        MDApp.get_running_app().show_notif("Signing you back in...", "success")
        connection.close()
        return retrieve_account(username, pin)
    else:
        control.execute("INSERT OR IGNORE INTO account VALUES (?,?)", data)
        print("Creating your account...")
        MDApp.get_running_app().show_notif("Creating your account...", "success")
        connection.commit()
        connection.close()
        return username

def retrieve_account(_username,_pin):
    connection = sqlite3.connect('ububble.db')
    control = connection.cursor()
    control.execute("SELECT * FROM account WHERE username = ? AND pin = ?", (_username, _pin))
    sign = control.fetchall()
    connection.close()

    if sign:
        return sign[0][0]
    return None

"""Manually delete Tables & Data"""
connection = sqlite3.connect('ububble.db')
control = connection.cursor()
#control.execute("DROP TABLE class")
#control.execute(" DELETE FROM login WHERE name = 'blackboard' ")
connection.commit()
connection.close()