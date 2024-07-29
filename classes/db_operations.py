import sqlite3
import os


class db_operations:
    def __init__(self) -> None:
        self.createDatabase()
        pass

    def createDatabase(self):
        """
        Creates the database and necessary tables if they don't exist.
        """
        # Create 'configs' folder if it doesn't exist
        if not os.path.isdir("configs"):
            os.makedirs("configs", exist_ok=True)
            config_path = os.path.abspath("configs")

        # Create database if it doesn't exist
        if not os.path.isfile("configs/translate_book.db"):
            try:
                db = sqlite3.connect("configs/translate_book.db")
                cursor = db.cursor()

                # Execute query to create tables
                cursor.execute('''
                    CREATE TABLE BookInformation(
                        id integer,
                        bookName varchar(1000),
                        page int,
                        originalPage varchar(9000),
                        translatedPage varchar(9000),
                        PRIMARY KEY(id)
                    );
                ''')

                db.commit()
                db.close()
            except:
                print("Error with creating database")

    def insertData(self, bookName, page, originalPage, translatedPage):
        """
        Inserts data into the BookInformation table.

        Args:
            bookName (str): The name of the book.
            page (int): The page number.
            originalPage (str): The original page content.
            translatedPage (str): The translated page content.
        """
        try:
            db = sqlite3.connect("configs/translate_book.db")
            cursor = db.cursor()
            cursor.execute(
                "INSERT INTO BookInformation(bookName, page, originalPage, translatedPage) VALUES(?,?,?,?)",
                (bookName, page, originalPage, translatedPage))
            db.commit()
            db.close()
        except:
            print("Error with inserting data")

    def selectData(self, bookName):
        """
        Retrieves translated pages from the BookInformation table for a given book name.

        Args:
            bookName (str): The name of the book.

        Returns:
            list: A list of translated pages.
        """
        try:
            db = sqlite3.connect("configs/translate_book.db")
            cursor = db.cursor()
            cursor.execute("SELECT translatedPage FROM BookInformation WHERE bookName = ? ORDER BY page", (bookName,))
            data = cursor.fetchall()
            db.close()
            return data
        except:
            print("Error with selecting data")

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



        