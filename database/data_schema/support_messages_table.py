from mysql.connector.cursor import MySQLCursorPrepared


def send_support_message(connection, name, email, subject, message, user_id=0):
    query = """INSERT INTO data_schema.support_messages (name, email, subject, message_text, user_id) VALUES (%s, %s, %s, %s, %s)"""
    cursor = connection.cursor(cursor_class=MySQLCursorPrepared)
    cursor.execute(query, (name, email, subject, message, user_id))
    connection.commit()
