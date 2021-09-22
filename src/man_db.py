import sqlite3
import os
from datetime import datetime


class Man_Db:
    def __init__(self, path):
        self.path = path
        self.create_db_history()

    def create_db_history(self):
        path = self.path
        if not os.path.exists(path):
            # conn = sqlite3.connect("..\\ressources\\data\\db.db")
            Id = ""
            Date = ""
            Url = ""
            Event = ""
            conn = sqlite3.connect(str(path))
            c = conn.cursor()
            sql = "CREATE TABLE history(Id TEXT, Date TEXT, Url TEXT, Event TEXT)"
            c.execute(sql)
            conn.commit()
            conn.close()
            x = 1
            while x < 11:
                conn = sqlite3.connect(str(path))
                c = conn.cursor()
                sql = "INSERT INTO history(Id, Date, Url, Event) VALUES ( '" + str(Id) + "', '" + str(Date) + "', '" + str(
                    Url) + "', '" + str(Event) + "')"
                c.execute(sql)
                conn.commit()
                conn.close()
                x = x + 1
        return (0)

    def write_db_history(self, Id, Date, Url, Event):
        path = self.path
        # conn = sqlite3.connect("..\\ressources\\data\\db.db")
        conn = sqlite3.connect(str(path))
        c = conn.cursor()
        sql = "INSERT INTO history(Id, Date, Url, Event) VALUES ( '" + str(Id) + "', '" + str(Date) + "', '" + str(
            Url) + "', '" + str(Event) + "')"
        c.execute(sql)
        conn.commit()
        conn.close()
        return (0)

    def read_db_history(self, item="*", Order=""):
        path = self.path
        # conn = sqlite3.connect("..\\ressources\\data\\db.db")
        conn = sqlite3.connect(str(path))
        c = conn.cursor()
        sql = "SELECT %s from history %s" % (str(item), str(Order))
        c.execute(sql)
        items = c.fetchall()
        conn.close()
        return (items)
