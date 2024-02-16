import os
import mysql.connector as mysql

class Global:
    def __init__(self):
        self.db = mysql.connect(host=os.getenv("DB_HOST"),
                                port=os.getenv("DB_PORT"),
                                user=os.getenv("DB_USERNAME"),
                                password=os.getenv("DB_PASSWORD"),
                                database=os.getenv("DB_DATABASE"))
        self.cursor = self.db.cursor()

    def get_top(self, limit: int = 10) -> list:
        self.cursor.execute("SELECT pseudo, score FROM user_score ORDER BY score DESC LIMIT %s", (limit,))
        fetched = self.cursor.fetchall()
        return fetched
    
    def get_number_of_entries(self) -> int:
        self.cursor.execute("SELECT COUNT(*) FROM user_score")
        fetched = self.cursor.fetchone()
        return fetched[0]

    def get_average(self) -> int:
        self.cursor.execute("SELECT score FROM user_score")
        fetched = self.cursor.fetchall()
        total = 0
        for i in fetched:
            total += i[0]
        return round(total / len(fetched), 2)