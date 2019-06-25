import mysql.connector
import time
import threading
from database.data_schema import users_table

connection = None


#
# cursor = connection.cursor()
#
# query = "SELECT * FROM data_schema.users"
# cursor.execute(query)
#
# for (password) in cursor:
#     print(password)


def connect():
    global connection
    connection = mysql.connector.connect(user='kd85nasm9l',
                                         password='vAJzxpPSW98HuZs',
                                         host='kaibchat.cr4kq43qy8ak.us-east-2.rds.amazonaws.com',
                                         database='kd85nasm9l',
                                         use_pure=True)
    return connection
    # thread = threading.Thread(target=update_connection)
    # thread.start()


def is_connected():
    global connection
    return connection.is_connected()


def update_connection():
    global connection
    while is_connected():
        users_table.is_user_exists(connection, "123")
        time.sleep(10000)
