import sqlite3

class sqliteDb:
    def __init__(self,db_path):
        self.con = sqlite3.connect(db_path)
        self.cur = self.con.cursor()
        

    def create_stock_table(self,table_name):
        self.cur.execute("CREATE TABLE IF NOT EXISTS \"{0}\" (id INTEGER NOT NULL UNIQUE,comment VARCHAR,PRIMARY KEY(id AUTOINCREMENT));".format(table_name))
    
    def insert(self,data,table_name,colum):
        if(isinstance(data,str)):
            self.cur.execute("INSERT INTO \"{0}\" ({1}) VALUES (\"{2}\");".format(table_name,colum,data))
            return
        for element in data:
            self.cur.execute("INSERT INTO \"{0}\" ({1}) VALUES (\"{2}\");".format(table_name,colum,element))

    def commit(self):
        self.con.commit()

    def close(self):
        self.con.close()

def main():
    db = sqliteDb("C:\\db\\mydb.db")
    table_name = ['2021/09/24-GG','2021/09/27-GG','2021/09/28-GG']
    db.insert(table_name,"TW_Stock","table_name")
    db.commit()
    db.close()

if __name__=='__main__':
    main()
