import sqlite3
import os
import json


class db_operations:
    def __init__(self) -> None:
        self.createDatabase()
        pass

    def createDatabase(self):
        """
        Creates the database and necessary tables if they don't exist.
        """
        if not os.path.isdir("configs"):
            os.makedirs("configs", exist_ok=True)

        if not os.path.isfile("configs/translate_book.db"):
            try:
                db = sqlite3.connect("configs/translate_book.db")
                cursor = db.cursor()
                cursor.execute('''
                    CREATE TABLE BookInformation(
                        id integer,
                        bookName varchar(1000),
                        page int,
                        originalPage TEXT,
                        translatedPage TEXT,
                        PRIMARY KEY(id)
                    );
                ''')
                db.commit()
                db.close()
            except Exception as e:
                print(f"Error with creating database: {e}")

    def insertData(self, bookName, page, originalPage, translatedPage):
        """
        Inserts data into the BookInformation table.
        """
        if isinstance(originalPage, (list, dict)):
            originalPage = json.dumps(originalPage, ensure_ascii=False)
        if isinstance(translatedPage, (list, dict)):
            translatedPage = json.dumps(translatedPage, ensure_ascii=False)

        try:
            db = sqlite3.connect("configs/translate_book.db")
            cursor = db.cursor()
            cursor.execute(
                "INSERT INTO BookInformation(bookName, page, originalPage, translatedPage) VALUES(?,?,?,?)",
                (bookName, page, originalPage, translatedPage))
            db.commit()
            db.close()
        except Exception as e:
            print(f"Error with inserting data: {e}")

    def selectData(self, bookName):
        """
        Retrieves translated pages from the BookInformation table for a given book name.
        """
        try:
            db = sqlite3.connect("configs/translate_book.db")
            cursor = db.cursor()
            cursor.execute("SELECT translatedPage FROM BookInformation WHERE bookName = ? ORDER BY page", (bookName,))
            data = cursor.fetchall()
            db.close()
            return data
        except Exception as e:
            print(f"Error with selecting data: {e}")
            return []

    def selectBlocksData(self, bookName):
        """
        Retrieves translated blocks from the BookInformation table for a given book name.
        Parses JSON strings back into Python objects.
        """
        try:
            db = sqlite3.connect("configs/translate_book.db")
            cursor = db.cursor()
            cursor.execute("SELECT translatedPage FROM BookInformation WHERE bookName = ? ORDER BY page", (bookName,))
            data = cursor.fetchall()
            db.close()

            result = []
            for row in data:
                val = row[0]
                if val:
                    try:
                        parsed = json.loads(val)
                        result.append(parsed)
                    except Exception:
                        result.append(val)
                else:
                    result.append([])
            return result
        except Exception as e:
            print(f"Error with selecting blocks data: {e}")
            return []


    def checkData(self, bookName):
        """
        Checks if data exists in the BookInformation table for a given book name.

        Args:
            bookName (str): The name of the book.

        Returns:
            bool: True if data exists, False otherwise.
        """
        try:
            db = sqlite3.connect("configs/translate_book.db")
            cursor = db.cursor()
            cursor.execute("SELECT * FROM BookInformation WHERE bookName = ?", (bookName,))
            data = cursor.fetchall()
            db.close()
            if len(data) == 0:
                return False
            else:
                return True
        except:
            print("Error with checking data")

    def last_page(self, bookName):
        """
        Retrieves the last page number from the BookInformation table for a given book name.

        Args:
            bookName (str): The name of the book.

        Returns:
            int: The last page number.
        """
        try:
            db = sqlite3.connect("configs/translate_book.db")
            cursor = db.cursor()
            cursor.execute("SELECT page FROM BookInformation WHERE bookName = ? ORDER BY page DESC LIMIT 1", (bookName,))
            data = cursor.fetchall()
            db.close()
            return data
        except:
            print("Error with checking last page")

    def list_books(self):
        """
        Retrieves all unique book names stored in the BookInformation table.

        Returns:
            list: A list of unique book names.
        """
        try:
            db = sqlite3.connect("configs/translate_book.db")
            cursor = db.cursor()
            cursor.execute("SELECT DISTINCT bookName FROM BookInformation")
            data = [row[0] for row in cursor.fetchall()]
            db.close()
            return data
        except Exception:
            print("Error with listing books")
            return []




        