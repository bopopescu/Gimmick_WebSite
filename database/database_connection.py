import mysql.connector

connection = None


class Database:

    def __init__(self):
        """Constructor"""
        self.connection = mysql.connector.connect(user='kd85nasm9l',
                                                  password='vAJzxpPSW98HuZs',
                                                  host='kaibchat.cr4kq43qy8ak.us-east-2.rds.amazonaws.com',
                                                  database='kd85nasm9l',
                                                  use_pure=True)

    def get_connection(self):
        self.connection = mysql.connector.connect(user='kd85nasm9l',
                                                  password='vAJzxpPSW98HuZs',
                                                  host='kaibchat.cr4kq43qy8ak.us-east-2.rds.amazonaws.com',
                                                  database='kd85nasm9l',
                                                  use_pure=True)
        return self.connection
