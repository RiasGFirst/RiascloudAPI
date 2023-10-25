from dotenv import load_dotenv
import mysql.connector
import uuid
import os


class DataBase:

    def __init__(self):
        # Database Connection
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
        print(self.conn)
        self.cursor = self.conn.cursor()
        self.cursor.execute(f"""CREATE DATABASE IF NOT EXISTS {self.database}""")
        self.cursor.execute(f"""USE {self.database}""")
        self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS subreddit (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255))""")
        self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS user (id INT AUTO_INCREMENT PRIMARY KEY, user_id VARCHAR(255), user_token VARCHAR(255))""")
        self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS user_subreddit (id INT AUTO_INCREMENT PRIMARY KEY, user_id VARCHAR(255), subreddit_id INT, before_id VARCHAR(255))""")
        self.conn.commit()

    # USER TABLE
    def createUser(self):
        user_id = str(uuid.uuid4())[0:8]
        token_id = str(uuid.uuid4())
        self.cursor.execute("""INSERT INTO user (user_id, user_token) VALUES (%s, %s)""", (user_id, token_id))
        self.conn.commit()
        return user_id, token_id, "User Added"

    def verifyUser(self, user_id, token_id):
        self.cursor.execute("""SELECT * FROM user WHERE user_id = %s AND user_token = %s""", (user_id, token_id))
        result = self.cursor.fetchone()
        if result:
            stored_token = result[2]
            if stored_token == token_id:
                return True, "User ID and Token ID is valid"
        return False, "User ID or Token ID is not valid"

    # SUBREDDIT TABLE
    def verifySubreddit(self, subreddit):
        self.cursor.execute("""SELECT * FROM subreddit WHERE name = %s""", (subreddit,))
        result = self.cursor.fetchall()
        if result:
            return True
        else:
            return False

    def addSubreddit(self, subreddit):
        self.cursor.execute("""INSERT INTO subreddit (name) VALUES (%s)""", (subreddit,))
        self.conn.commit()
        return "Subreddit Added"

    def getSubredditId(self, subreddit):
        self.cursor.execute("""SELECT id FROM subreddit WHERE name = %s""", (subreddit,))
        result = self.cursor.fetchone()
        if result is not None:
            return result[0]
        else:
            return None

    # USER_SUBREDDIT TABLE
    def getUserSubreddit(self, user_id, token_id, subreddit):
        verify, error = self.verifyUser(user_id=user_id, token_id=token_id)
        if verify:
            subreddit_id = self.getSubredditId(subreddit=subreddit)
            self.cursor.execute("""SELECT * FROM user_subreddit WHERE user_id = %s AND subreddit_id = %s""", (user_id, subreddit_id))
            result = self.cursor.fetchone()
            if result is not None:
                return result
        else:
            return error

    def addUserSubreddit(self, user_id, token_id, subreddit, before_id):
        verify, error = self.verifyUser(user_id=user_id, token_id=token_id)
        subreddit_id = self.getSubredditId(subreddit=subreddit)
        if verify:
            subreddit_verify = self.getUserSubreddit(user_id=user_id, token_id=token_id, subreddit=subreddit)
            if subreddit_verify is not None:
                self.userSubredditUpdate(user_id=user_id, token_id=token_id, subreddit=subreddit, before_id=before_id, subreddit_id=subreddit_id, verify=verify, error=error)
            else:
                self.cursor.execute("""INSERT INTO user_subreddit (user_id, subreddit_id, before_id) VALUES (%s, %s, %s)""", (user_id, subreddit_id, before_id))
                self.conn.commit()
                return "User Subreddit Added"
        else:
            return error

    def userSubredditUpdate(self, user_id, token_id, subreddit, before_id, subreddit_id=None, verify=False, error=None):
        if verify:
            subreddit_verify = self.getUserSubreddit(user_id=user_id, token_id=token_id, subreddit=subreddit)
            if subreddit_verify is not None:
                self.cursor.execute("""UPDATE user_subreddit SET before_id = %s WHERE user_id = %s AND subreddit_id = %s""", (before_id, user_id, subreddit_id))
                self.conn.commit()
                return "User Subreddit Updated"
            else:
                return "User Subreddit Not Updated"
        else:
            return error