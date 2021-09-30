import sqlite3
from os import path, getcwd


class db:
    def __init__(self, db='hacksec_mail.db'):
        self.conn = sqlite3.connect(path.join("/opt/hacksec_tempmail", "db", db))
        self.cur = self.conn.cursor()
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS hacksec (
            id	INTEGER UNIQUE NOT NULL PRIMARY KEY AUTOINCREMENT,
            from_email	TEXT,
            to_email	TEXT,
            date	TEXT,
            subject	TEXT,
            content	TEXT
        )
        """)
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS user (
            id	INTEGER UNIQUE NOT NULL PRIMARY KEY AUTOINCREMENT,
            username	TEXT NOT NULL UNIQUE,
            password	TEXT NOT NULL,
            active	INTEGER NOT NULL
        )
        """)
        self.conn.commit()

    def insert(self, email):
        self.cur.execute(
            "INSERT INTO hacksec VALUES (NULL, ?, ?, ?, ?,?)", (email.from_email, email.to, email.date, email.subject, email.content))
        self.conn.commit()
        return True

    def view(self):
        self.cur.execute("SELECT * FROM hacksec")
        rows = self.cur.fetchall()
        return rows

    def view_single(self, id):
        self.cur.execute("SELECT * FROM hacksec WHERE id=?", (id,))
        rows = self.cur.fetchall()
        return rows

    def search(self, from_email="", subject=""):
        self.cur.execute(
            "SELECT * FROM hacksec WHERE from_email=? OR subject=?", (from_email, subject))
        rows = self.cur.fetchall()
        return rows

    def delete(self, id):
        self.cur.execute("DELETE FROM hacksec WHERE id=?", (id,))
        self.conn.commit()
        return True

    def delete_all(self,to):
        self.cur.execute("DELETE * FROM hacksec WHERE to_email=?", (to,))
        self.conn.commit()
        return True

    def find_by_user(self,to):
        self.cur.execute("SELECT * FROM hacksec WHERE to_email=?", (to,))
        rows = self.cur.fetchall()
        return rows

    def __del__(self):
        self.conn.close()
