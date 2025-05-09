import mysql.connector
from henryInterfaceClasses import Author, Book, BranchandCopies, Category, CategoryandBook, Publisher, PublisherandBook

class HenryDAO:
    '''
    This class connects to MySQL and uses the connection to retrieve the needed information
    from the database.
    
    Method:
        __init__ : This method connects to MySQL.
        
        getAuthorData: This method gets the author data needed for the author tab.
        
        getBookData: This method gets the book data used in the author tab.
        
        getBranchandCopies: This method gets the branch and number of copies data used in
        all three tabs.
        
        getCategoryData: This method gets the category data needed for the category tab.
        
        getCategoryandBookData: This method gets the category and book data used in the category tab.
        
        getPublisherData: This method gets the publisher data needed for the publisher tab.
        
        getPublisherandBookData: This method gets the publisher and book data used in the publisher tab.
        
        close: This method closes the cursor and the connection to MySQL.
            
    '''
    def __init__(self):
        self.mydb = mysql.connector.connect(
            user='my_user', #change to your MySQL user
            password='my_password', #change to your MySQL password
            database='bookstore',
            host='my_host') #change to your host
        self.mycur = self.mydb.cursor()
        
    def getAuthorData(self):
        self.mycur.execute("SELECT AUTHOR_NUM, CONCAT(AUTHOR_FIRST, ' ', AUTHOR_LAST) FROM HENRY_AUTHOR ORDER BY AUTHOR_NUM;")
        return Author(self.mycur.fetchall())
    
    def getBookData(self):
        self.mycur.execute("SELECT AUTHOR_NUM, TITLE, PRICE, HENRY_BOOK.BOOK_CODE FROM HENRY_BOOK INNER JOIN HENRY_WROTE ON HENRY_BOOK.BOOK_CODE = HENRY_WROTE.BOOK_CODE ORDER BY AUTHOR_NUM;")
        return Book(self.mycur.fetchall())
    
    def getBranchandCopiesData(self):
        self.mycur.execute("SELECT AUTHOR_NUM, TITLE, BRANCH_NAME, ON_HAND FROM HENRY_BOOK INNER JOIN HENRY_INVENTORY ON HENRY_BOOK.BOOK_CODE = HENRY_INVENTORY.BOOK_CODE INNER JOIN HENRY_BRANCH ON HENRY_INVENTORY.BRANCH_NUM = HENRY_BRANCH.BRANCH_NUM INNER JOIN HENRY_WROTE ON HENRY_BOOK.BOOK_CODE = HENRY_WROTE.BOOK_CODE ORDER BY AUTHOR_NUM;")
        return BranchandCopies(self.mycur.fetchall())
    
    def getCategoryData(self):
        self.mycur.execute("SELECT DISTINCT(TYPE) FROM HENRY_BOOK;")
        return Category(self.mycur.fetchall())
    
    def getCategoryandBookData(self):
        self.mycur.execute("SELECT HENRY_AUTHOR.AUTHOR_NUM, TYPE, TITLE, PRICE FROM HENRY_AUTHOR INNER JOIN HENRY_WROTE ON HENRY_AUTHOR.AUTHOR_NUM = HENRY_WROTE.AUTHOR_NUM INNER JOIN HENRY_BOOK ON HENRY_WROTE.BOOK_CODE = HENRY_BOOK.BOOK_CODE ORDER BY HENRY_AUTHOR.AUTHOR_NUM;")
        return CategoryandBook(self.mycur.fetchall())
    
    def getPublisherData(self):
        self.mycur.execute("SELECT PUBLISHER_CODE, PUBLISHER_NAME FROM HENRY_PUBLISHER ORDER BY PUBLISHER_NAME;")
        return Publisher(self.mycur.fetchall())
    
    def getPublisherandBookData(self):
        self.mycur.execute("SELECT HENRY_BOOK.PUBLISHER_CODE, PUBLISHER_NAME, TITLE, PRICE FROM HENRY_BOOK INNER JOIN HENRY_PUBLISHER ON HENRY_BOOK.PUBLISHER_CODE = HENRY_PUBLISHER.PUBLISHER_CODE ORDER BY PUBLISHER_NAME;")
        return PublisherandBook(self.mycur.fetchall())
    
    def close(self):
        self.mycur.close()
        self.mydb.close()
