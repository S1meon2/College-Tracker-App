import sqlite3
from Assignment_WEB import scrape_cengage, scrape_zybooks, scrape_blackboard

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

        memConnection = sqlite3.connect(":memory:")

        memControl = memConnection.cursor()

        memControl.execute("""CREATE TABLE IF NOT EXISTS

                login (name TEXT, username TEXT, password TEXT, isSigned BLOB)

            """)

        memControl.execute("INSERT OR IGNORE INTO login VALUES (?, ?, ?, ?)", data)

        memConnection.commit()
        memConnection.close()

        print(name + " has been connected!")

def recieve_login():
    connection = sqlite3.connect('logins.db')
    control = connection.cursor()
    control.execute("SELECT * FROM login")
    logins = control.fetchall()

    all_data = " "
    for login in logins:

        if login[0] == "cengage":
            all_data += scrape_cengage(login[0], login[1], login[2])

        if login[0] == "zybooks":
           all_data += scrape_zybooks(login[0], login[1], login[2])

        if login[0] == "blackboard":
            all_data += scrape_blackboard(login[0], login[1], login[2])

    return all_data

def scrape_test():
    connection = sqlite3.connect('logins.db')
    control = connection.cursor()
    control.execute("SELECT * FROM login")
    logins = control.fetchone()

    data = ""

    name = logins[0]
    username = logins[1]
    password = logins[2]

    connection = sqlite3.connect('classes.db')
    control = connection.cursor()
    control.execute("SELECT * FROM class")
    classItem = control.fetchone()
    data = scrape_zybooks(name ,username, password, classItem[3])

    return data


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

        memConnection = sqlite3.connect(":memory:")

        memControl = memConnection.cursor()

        memControl.execute("""CREATE TABLE IF NOT EXISTS

                        class (classname TEXT, webname TEXT, classid TEXT, isSigned BLOB)

                    """)

        memControl.execute("INSERT OR IGNORE INTO class VALUES (?, ?, ?, ?)", data)

        memConnection.commit()
        memConnection.close()

        print(classname + " has been added and can now be scraped!")


"""Manually delete Tables & Data"""
connection = sqlite3.connect('logins.db')
control = connection.cursor()
#control.execute("DROP TABLE class")
control.execute(" DELETE FROM login WHERE name = 'blackboard' ")
connection.commit()
connection.close()