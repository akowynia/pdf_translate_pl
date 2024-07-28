import sqlite3
import os


class db_operations:
    def __init__(self) -> None:
        self.createDatabase()
        pass
    def createDatabase(self):

        # tworzy folder configs jeśli nie istnieje
        if not os.path.isdir("configs"):
            os.makedirs("configs", exist_ok=True)
            config_path = os.path.abspath("configs")

        # tworzy bazę danych jeśli nie istnieje
        if not os.path.isfile("configs/translate_book.db"):
            try:
                db = sqlite3.connect("configs/translate_book.db")
                cursor = db.cursor()

                # wykonuje kwerendę tworzącą tabele
                cursor.execute('''
  CREATE TABLE BookInformation(
    id integer,
    bookName varchar(2000),
    page int,
    originalPage varchar(2000),
    translatedPage varchar(2000),
    PRIMARY KEY(id)

            );

                ''')

                db.commit()
                # cursor.execute(sql,data)
                db.close()
            except:
                print("Błąd tworzenia bazy danych")

    def insertData(self, bookName, page, originalPage, translatedPage):
        try:
            db = sqlite3.connect("configs/translate_book.db")
            cursor = db.cursor()
            cursor.execute(
                "INSERT INTO BookInformation(bookName, page, originalPage, translatedPage) VALUES(?,?,?,?)", (bookName, page, originalPage, translatedPage))
            db.commit()
            db.close()
        except:
            print("Błąd dodawania danych")

    def selectData(self,bookName):
        try:
            db = sqlite3.connect("configs/translate_book.db")
            cursor = db.cursor()
            cursor.execute("SELECT translatedPage FROM BookInformation WHERE bookName = ? order by page",(bookName,))
            data = cursor.fetchall()
            db.close()
            return data
        except:
            print("Błąd pobierania danych")
            
    def checkData(self,bookName):
        try:
            db = sqlite3.connect("configs/translate_book.db")
            cursor = db.cursor()
            cursor.execute("SELECT * FROM BookInformation WHERE bookName = ?",(bookName,))
            data = cursor.fetchall()
            db.close()
            if len(data) == 0:
                return False
            else:
                return True
        except:
            print("Błąd pobierania danych")
    
    def last_page(self,bookName):
        try:
            db = sqlite3.connect("configs/translate_book.db")
            cursor = db.cursor()
            cursor.execute("SELECT page FROM BookInformation WHERE bookName = ? order by page desc limit 1",(bookName,))
            data = cursor.fetchall()
            db.close()
            return data
        except:
            print("Błąd pobierania danych")



        