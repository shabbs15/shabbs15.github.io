import sqlite3

exampleMode = True

class model():
    def __init__(self):
        self.conn = sqlite3.connect("wall.db", check_same_thread=False)
        self.cursor = self.conn.cursor()


    def getPosts(self):
        self.cursor.execute("""
        SELECT * FROM wall ORDER BY datetime(Date) DESC;
        """)

        return self.cursor.fetchall()

    def addToTheWall(self, message, user, date):
        self.cursor.execute("INSERT INTO wall (Message, User, Date) VALUES (?,?,?)",(message, user, date))    
        self.conn.commit()