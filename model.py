import sqlite3

exampleMode = True

class model():
    def __init__(self):
        self.conn = sqlite3.connect("wall.db", check_same_thread=False)
        self.cursor = self.conn.cursor()

        self.cursor.execute("SELECT * FROM sqlite_master WHERE type = 'table' AND name = 'wall'")
        if self.cursor.fetchone() == None:
            self.initDatabase()
        else:
            print("homeboy I beg you")

    def initDatabase(self):
        self.cursor.execute("""
        CREATE TABLE wall(
            PostId integer primary key,
            Message Text,
            User Text,
            Date Text
        )""")


    def getPosts(self):
        self.cursor.execute("""
        SELECT * FROM wall ORDER BY datetime(Date) DESC;
        """)

        return self.cursor.fetchall()

    def addToTheWall(self, message, user, date):
        self.cursor.execute("INSERT INTO wall (Message, User, Date) VALUES (?,?,?)",(message, user, date))    
        self.conn.commit()

    def deleteRecord(self, id):
        self.cursor.execute("""
        DELETE FROM wall
        WHERE PostId = ?
        """, (id,))

        self.conn.commit()