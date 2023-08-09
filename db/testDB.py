from dotenv import load_dotenv
import mysql.connector
import os


class DataBase:

    def __init__(self):
        load_dotenv()
        self.host = os.getenv("DB_HOST")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.database = os.getenv("DB_DATABASE")

        self.conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.cursor = self.conn.cursor()
        self.cursor.execute("""CREATE DATABASE IF NOT EXISTS riascloudAPI""")
        self.cursor.execute("""USE riascloudAPI""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS subreddit (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), before_id VARCHAR(255))""")
        self.conn.commit()

    def verifySubreddit(self, subreddit):
        self.cursor.execute("""SELECT * FROM subreddit WHERE name = %s""", (subreddit,))
        result = self.cursor.fetchall()
        if result:
            return True
        else:
            return False

    def addSubreddit(self, subreddit, before_id):
        self.cursor.execute("""INSERT INTO subreddit (name, before_id) VALUES (%s, %s)""", (subreddit, before_id))
        self.conn.commit()
        return "Subreddit Added"

    def updateSubreddit(self, subreddit, before_id):
        self.cursor.execute("""UPDATE subreddit SET before_id = %s WHERE name = %s""", (before_id, subreddit))
        self.conn.commit()
        return "Subreddit Updated"

    def getBeforeId(self, subreddit):
        self.cursor.execute("""SELECT before_id FROM subreddit WHERE name = %s""", (subreddit,))
        result = self.cursor.fetchall()
        return result[0][0]

    def getAllSubreddit(self):
        self.cursor.execute("""SELECT * FROM subreddit""")
        result = self.cursor.fetchall()
        return result

    def deleteSubreddit(self, subreddit):
        self.cursor.execute("""DELETE FROM subreddit WHERE name = %s""", (subreddit,))
        self.conn.commit()
        return "Subreddit Deleted"