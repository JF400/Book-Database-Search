class Author:
    '''
    This class stores the author data, cleans it and puts it in a form that's used to code the tab.
    
    Method:
        __init__ : This method defines the author_list and calls clean_data().
        
        clean_data: This method ensures the data is in the correct datatypes and
        puts in a form that's used to code the tab.
        
    '''
    def __init__(self, author_list):
        self.author_list = author_list
        self.clean_data()
        
    def clean_data(self):
        self.author_list = [(int(number), str(full_name)) for
                     number, full_name in self.author_list]
        return self.author_list
    
class Book:
    '''
    This class stores the book data, cleans it and puts it in a form that's used to code the tab.
    
    Method:
        __init__ : This method defines the book_list and calls clean_data().
        
        clean_data: This method ensures the data is in the correct datatypes and
        puts in a form that's used to code the tab.
    
    '''
    def __init__(self, book_list):
        self.book_list = book_list
        self.clean_data()
              
    def clean_data(self):
        self.book_list = [(int(number), str(title), float(price), str(book_code)) for
                     number, title, price, book_code in self.book_list]
        return self.book_list

class BranchandCopies:
    '''
    This class stores the Branch and Number of Copies data, cleans it and puts it in a form that's used to code the tabs.
    
    Method:
        __init__ : This method defines the branch_and_copies_list and calls clean_data().
        
        clean_data: This method ensures the data is in the correct datatypes and
        puts in a form that's used to code the tabs.
        
    '''
    def __init__(self, branch_and_copies_list):
        self.branch_and_copies_list = branch_and_copies_list
        self.clean_data()
        
    def clean_data(self):
        self.branch_and_copies_list = [(int(number), str(title), str(branch_name), int(num_copies)) for
                                       number, title, branch_name, num_copies in self.branch_and_copies_list]
        return self.branch_and_copies_list
    
class Category:
    '''
    This class stores the category data. Note that the list was enough to code the tab.
    
    Method:
        __init__ : This method defines the category_list.
    
    '''
    def __init__(self, category_list):
        self.category_list = category_list

class CategoryandBook:
    '''
    This class stores the category and book data, cleans it and puts it in a form that's used to code the tab.
    
    Method:
        __init__ : This method defines the category_and_book_list and calls clean_data().
        
        clean_data: This method ensures the data is in the correct datatypes and
        puts in a form that's used to code the tab.
        
    '''
    def __init__(self, category_and_book_list):
        self.category_and_book_list = category_and_book_list
        self.clean_data()
        
    def clean_data(self):
        self.category_and_book_list = [(int(number), str(book_type), str(title), float(price)) for
                                       number, book_type, title, price in self.category_and_book_list]
        return self.category_and_book_list
    
class Publisher:
    '''
    This class stores the publisher data, cleans it and puts it in a form that's used to code the tab.
    
    Method:
        __init__ : This method defines the publisher_list and calls clean_data().
        
        clean_data: This method ensures the data is in the correct datatypes and
        puts in a form that's used to code the tab.
    
    '''
    def __init__(self, publisher_list):
        self.publisher_list = publisher_list
        self.clean_data()
        
    def clean_data(self):
        self.publisher_list = [(str(publisher_code), str(publisher))
                               for publisher_code, publisher in self.publisher_list]
    
class PublisherandBook:
    '''
    This class stores the publisher and book data, cleans it and puts it in a form that's used to code the tab.
    
    Method:
        __init__ : This method defines the publisher_and_book_list and calls clean_data().
        
        clean_data: This method ensures the data is in the correct datatypes and
        puts in a form that's used to code the tab.
        
    '''
    def __init__(self, publisher_and_book_list):
        self.publisher_and_book_list = publisher_and_book_list
        self.clean_data()
        
    def clean_data(self):
        self.publisher_and_book_list = [(str(publisher_code), str(publisher), str(title), float(price)) for
                               publisher_code, publisher, title, price in self.publisher_and_book_list]
        return self.publisher_and_book_list
