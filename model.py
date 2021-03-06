import sqlite3, os

exampleMode = True

class model():
    def __init__(self):
        self.conn = sqlite3.connect("wall.db", check_same_thread=False, isolation_level=None)
        self.conn.execute('pragma journal_mode=wal')
        self.cursor = self.conn.cursor()

        self.cursor.execute("SELECT * FROM sqlite_master WHERE type = 'table' AND name = 'user'")
        if self.cursor.fetchone() == None:
            print("resetting the database")
            self.initDatabase()

    def initDatabase(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = self.cursor.fetchall()
        
        for table, in tables:
            self.cursor.execute(f"DROP TABLE {table}")

        print(self.cursor.fetchall())

        self.cursor.execute("""
        CREATE TABLE wall(
            PostId integer primary key,
            Message Text,
            User Text,
            Date Text
        )""")

        self.cursor.execute("""
        CREATE TABLE user(
            UserId integer primary key,
            Username Text,
            Password Text
        )""")
        self.conn.commit()

    def getPosts(self):
        self.cursor.execute("""
        SELECT * FROM wall ORDER BY datetime(Date) DESC;
        """)

        return self.cursor.fetchall()

    def addToTheWall(self, message, user, date):
        self.cursor.execute("INSERT INTO wall (Message, User, Date) VALUES (?,?,?)",(message, user, date))    
        self.conn.commit()
    
    def addUser(self, username, password):
        self.cursor.execute("INSERT INTO user (Username, Password) VALUES (?,?)",(username, password))
        self.conn.commit()

    def login(self,username, password):
        self.cursor.execute("""
        SELECT username, password FROM user WHERE username=?   
        """, (username,))

        result = self.cursor.fetchone()
        if result:
            # account exists in the system
            if password == result[1]:
                return True
            else:
                return False
        else:
            # create an account homeboy
            self.addUser(username, password)
            return True

    def deleteRecord(self, id):
        self.cursor.execute("""
        DELETE FROM wall
        WHERE PostId = ?
        """, (id,))

        self.conn.commit()

    def deleteAllPosts(self):
        self.cursor.execute("""
        DELETE FROM wall;
        """)
        
        self.conn.commit()