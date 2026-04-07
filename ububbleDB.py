import sqlite3
from Assignment_WEB import scrape_cengage, scrape_zybooks, scrape_blackboard

connection = sqlite3.connect('website_logins.db')

cursor = connection.cursor()

command1 = """CREATE TABLE IF NOT EXISTS

login(name TEXT PRIMARY KEY, username TEXT, password TEXT)

"""



#cursor.execute(command1)

def send_info(name, userName, userPass):

    data = [
        (name, userName, userPass),
    ]

    # Insert multiple rows efficiently
    cursor.executemany("INSERT OR IGNORE INTO login (name, username, password) VALUES (?, ?, ?)", data)
    connection.commit()

    cursor.execute("SELECT * FROM login")

    results = cursor.fetchall()

    #cursor.execute("DELETE * FROM login")

    print(results)

def recieve_info():
    connection = sqlite3.connect('website_logins.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM login")
    logins = cursor.fetchall()

    all_data = " "
    for login in logins:

        if login[0] == "cengage":
            all_data += scrape_cengage(login[0], login[1], login[2])

        if login[0] == "zybooks":
           all_data += scrape_zybooks(login[0], login[1], login[2])

        if login[0] == "blackboard":
            all_data += scrape_blackboard(login[0], login[1], login[2])

    return all_data


