import tkinter as tk
from tkinter import ttk
from henryDAO import HenryDAO

def main():
    app = Application()
    app.mainloop()

class Application(tk.Tk):
    '''
    This class sets up the GUI including the tabs for "Search by Author", "Search by Category" and "Search by Publisher".
    
    '''
    def __init__(self):
        super().__init__()
        self.title("Henry Bookstore")
        self.option_add('*TCombobox*Listbox.foreground', 'blue')
        self.geometry('900x400')
        
        #Creating the three tabs.
        tabControl = ttk.Notebook(self)
        tabControl.pack(expand=2, fill="both")
        
        author_tab = HenrySBA(tabControl)
        tabControl.add(author_tab, text="Search by Author")
        
        category_tab = HenrySBC(tabControl)
        tabControl.add(category_tab, text="Search by Category")
        
        publisher_tab = HenrySBP(tabControl)
        tabControl.add(publisher_tab, text="Search by Publisher")


class HenrySBA(ttk.Frame):
    '''
    This class populates the "Search by Author" tab.
    
    Method:
        __init__ : This method populates the "Search by Author" tab with all of the labels and
        Comboboxes including populating the initial values.
        
        author_selected: This method is binded to the author combobox. When a new author from the combobox is
        selected, this method updates the book combobox and the price and the treeview. Note that this method
        also handles the special cases.
        
        book_selected: This method is binded to the book combobox. When a new book from the combobox is selected,
        this method updates the price and the treeview. Note that this method also handles the special cases.
            
    '''
    def __init__(self, parent):
        super().__init__(parent)
        
        #Creating a HenryDAO object and using it to get all the needed information from the database.
        self.HenryDAO_object = HenryDAO()
        self.author_info = HenryDAO.getAuthorData(self.HenryDAO_object)
        self.book_info = HenryDAO.getBookData(self.HenryDAO_object)
        self.branch_and_copies_info = HenryDAO.getBranchandCopiesData(self.HenryDAO_object)
        self.HenryDAO_object.close()
                
        self.author_lab = ttk.Label(self)
        self.author_lab.grid(row=5,column=3)
        self.author_lab['text'] = "Author Selection:"
        
        self.book_lab = ttk.Label(self)
        self.book_lab.grid(row=5, column=4)
        self.book_lab['text'] = "Book Selection:"
        
        #Creating and populating the author combobox.
        self.author_combo = ttk.Combobox(self, width=20, state="readonly")
        self.author_combo.grid(row=6,column=3)
        self.author_combo['values'] = [t[1] for t in self.author_info.author_list if t[0] in (v[0] for v in self.book_info.book_list)]
        self.author_combo.current(0)
        self.author_combo.bind("<<ComboboxSelected>>", self.author_selected)
        
        #Creating and populating the book combobox.
        self.book_combo = ttk.Combobox(self, width=35, state="readonly")
        self.book_combo.grid(row=6,column=4)
        self.book_combo['values'] = [t[1] for t in self.book_info.book_list if t[0] == 1]
        self.book_combo.current(0)
        self.book_combo.bind("<<ComboboxSelected>>", self.book_selected)
        
        #Creating the Price label.
        self.price = ttk.Label(self)
        self.price.grid(row=6,column=5)
        self.price['text'] = "Price: $" + str(self.book_info.book_list[0][2])
        
        #Creating and Populating the Treeview.
        self.av = ttk.Treeview(self, columns=('Branch', 'Copies'), show='headings', selectmode='extended')
        self.av_lab = ttk.Label(self)
        self.av_lab.grid(row=1,column=4)
        self.av_lab['text'] = "Available Copies"
        self.av.heading('Branch', text='Branch Name')
        self.av.heading('Copies', text='Copies Available')
        self.av.grid(row=2,column=4)
        for row in [(t[2], t[3]) for t in self.branch_and_copies_info.branch_and_copies_list if t[1] == self.book_combo['values'][0]]:
            self.av.insert("", "end", values=[row[0], row[1]])
            
    def author_selected(self, event=None):
        self.book_combo.set('')
        index_num = int(self.author_combo.current())
        if (index_num == 20):
            author_num = index_num + 3
            title = [t[1] for t in self.book_info.book_list if t[0] == author_num][0]
        elif (index_num == 21):
            author_num = index_num + 3
            title = [t[1] for t in self.book_info.book_list if t[0] == author_num][0]
        else:
            author_num = index_num + 1
            title = [t[1] for t in self.book_info.book_list if t[0] == author_num][0]
        #Updating the book combobox using author number to do so.
        self.book_combo['values'] = [t[1] for t in self.book_info.book_list if t[0] == author_num]
        #Updating the price.
        price = [t[2] for t in self.book_info.book_list if (t[1] == title) and (t[0] == author_num)][0]
        self.price.config(text = "Price: $" + str(price))
        self.book_combo.current(0)
        #Updating the Treeview.
        for record in self.av.get_children():
            self.av.delete(record)
        for row in [(t[2], t[3]) for t in self.branch_and_copies_info.branch_and_copies_list if (t[1] == self.book_combo['values'][0]) and (t[0] == author_num)]:
            self.av.insert("", "end", values = [row[0], row[1]])
        
    def book_selected(self, event=None):
        index_num = int(self.author_combo.current())
        if (index_num == 20):
            author_num = index_num + 3
        elif (index_num == 21):
            author_num = index_num + 3
        else:
            author_num = index_num + 1
        #Updating the price.
        price = [t[2] for t in self.book_info.book_list if (t[1] == self.book_combo.get()) and (t[0] == author_num)][0]
        self.price.config(text = "Price: $" + str(price))
        #Updating the Treeview.
        for record in self.av.get_children():
            self.av.delete(record)
        for row in [(t[2], t[3]) for t in self.branch_and_copies_info.branch_and_copies_list if (t[1] == self.book_combo.get()) and (t[0] == author_num)]:
            self.av.insert("", "end", values=[row[0], row[1]])

class HenrySBC(ttk.Frame):
    '''
    This class populates the "Search by Category" tab.
    
    Method:
        __init__ : This method populates the "Search by Category" tab with all of the labels and
        Comboboxes including populating the initial values.
        
        category_selected: This method is binded to the category combobox. When a new category from the combobox is
        selected, this method updates the book combobox and the price and the treeview. Note that this method
        also handles the special cases.
        
        book_selected: This method is binded to the book combobox. When a new book from the combobox is selected,
        this method updates the price and the treeview. Note that this method also handles the special cases.
    
    '''
    def __init__(self, parent):
        super().__init__(parent)
        
        #Creating a HenryDAO object and using it to get all the needed information from the database.
        self.HenryDAO_object = HenryDAO()
        self.category_info = HenryDAO.getCategoryData(self.HenryDAO_object)
        self.category_and_book_info = HenryDAO.getCategoryandBookData(self.HenryDAO_object)
        self.branch_and_copies_info = HenryDAO.getBranchandCopiesData(self.HenryDAO_object)
        self.HenryDAO_object.close()
        
        self.category_lab = ttk.Label(self)
        self.category_lab.grid(row=5,column=3)
        self.category_lab['text'] = "Category Selection:"
        
        self.book_lab = ttk.Label(self)
        self.book_lab.grid(row=5, column=4)
        self.book_lab['text'] = "Book Selection:"
        
        #Creating and populating the category combobox.
        self.category_combo = ttk.Combobox(self, width=20, state="readonly")
        self.category_combo.grid(row=6,column=3)
        self.category_combo['values'] = self.category_info.category_list
        self.category_combo.current(0)
        self.category_combo.bind("<<ComboboxSelected>>", self.category_selected)
        
        #Creating and populating the book combobox.
        self.book_combo = ttk.Combobox(self, width=35, state="readonly")
        self.book_combo.grid(row=6,column=4)
        self.book_combo['values'] = [t[2] for t in self.category_and_book_info.category_and_book_list if t[1] == 'SFI']
        self.book_combo.current(0)
        self.book_combo.bind("<<ComboboxSelected>>", self.book_selected)
        
        #Creating the Price label.
        self.price = ttk.Label(self)
        self.price.grid(row=6,column=5)
        self.price['text'] = "Price: $" + str(self.category_and_book_info.category_and_book_list[4][3])
        
        #Creating and Populating the Treeview.
        self.av = ttk.Treeview(self, columns=('Branch', 'Copies'), show='headings', selectmode='extended')
        self.av_lab = ttk.Label(self)
        self.av_lab.grid(row=1,column=4)
        self.av_lab['text'] = "Available Copies"
        self.av.heading('Branch', text='Branch Name')
        self.av.heading('Copies', text='Copies Available')
        self.av.grid(row=2,column=4)
        for row in [(t[2], t[3]) for t in self.branch_and_copies_info.branch_and_copies_list if t[1] == self.book_combo['values'][0]]:
            self.av.insert("", "end", values=[row[0], row[1]])
            
    def category_selected(self, event=None):
        self.book_combo.set('')
        #Updating the book combobox while handling special cases.
        if (self.category_combo.get() != 'CMP'):
            self.book_combo['values'] = list(set(t[2] for t in self.category_and_book_info.category_and_book_list if t[1] == self.category_combo.get()))
        else:
            self.book_combo['values'] = [t[2] for t in self.category_and_book_info.category_and_book_list if t[1] == self.category_combo.get()]
        title = self.book_combo['values'][0]
        #Updating the price.
        price = [t[3] for t in self.category_and_book_info.category_and_book_list if t[2] == title][0]
        self.price.config(text = "Price: $" + str(price))
        self.book_combo.current(0)
        #Updating the Treeview while handling special cases.
        for record in self.av.get_children():
            self.av.delete(record)
        if (self.category_combo.get() == 'CMP'):
            branch_and_copy = [(t[2], t[3]) for t in self.branch_and_copies_info.branch_and_copies_list if (t[1] == self.book_combo['values'][0])]
            self.av.insert("", "end", values = [branch_and_copy[0][0], branch_and_copy[0][1]])
        elif (self.category_combo.get() == 'ART'):
            branch_and_copy = [(t[2], t[3]) for t in self.branch_and_copies_info.branch_and_copies_list if (t[1] == self.book_combo['values'][0])]
            self.av.insert("", "end", values = [branch_and_copy[0][0], branch_and_copy[0][1]])
        else:
            for row in [(t[2], t[3]) for t in self.branch_and_copies_info.branch_and_copies_list if (t[1] == self.book_combo['values'][0])]:
                self.av.insert("", "end", values = [row[0], row[1]])
        
    def book_selected(self, event=None):
        #Updating the price and Treeview while handling special cases.
        for record in self.av.get_children():
            self.av.delete(record)
        if (self.category_combo.get() == 'CMP') and (self.book_combo.current() == 0):
            price = [t[3] for t in self.category_and_book_info.category_and_book_list if (t[2] == self.book_combo.get())][0]
            branch_and_copy = [(t[2], t[3]) for t in self.branch_and_copies_info.branch_and_copies_list if (t[1] == self.book_combo.get())][0]
            self.av.insert("", "end", values = [branch_and_copy[0], branch_and_copy[1]])
        elif (self.category_combo.get() == 'CMP') and (self.book_combo.current() == 1):
            price = [t[3] for t in self.category_and_book_info.category_and_book_list if (t[2] == self.book_combo.get())][1]
            branch_and_copy = [(t[2], t[3]) for t in self.branch_and_copies_info.branch_and_copies_list if (t[1] == self.book_combo.get())][1]
            self.av.insert("", "end", values = [branch_and_copy[0], branch_and_copy[1]])
        else:
            price = [t[3] for t in self.category_and_book_info.category_and_book_list if (t[2] == self.book_combo.get())][0]
            for row in list(set((t[2], t[3]) for t in self.branch_and_copies_info.branch_and_copies_list if (t[1] == self.book_combo.get()))):
                self.av.insert("", "end", values=[row[0], row[1]])
        self.price.config(text = "Price: $" + str(price))

class HenrySBP(ttk.Frame):
    '''
    This class populates the "Search by Publisher" tab.
    
    Method:
        __init__ : This method populates the "Search by Publisher" tab with all of the labels and
        Comboboxes including populating the initial values.
        
        publisher_selected: This method is binded to the publisher combobox. When a new publisher from the combobox is
        selected, this method updates the book combobox and the price and the treeview. Note that this method
        also handles the special cases.
        
        book_selected: This method is binded to the book combobox. When a new book from the combobox is selected,
        this method updates the price and the treeview. Note that this method also handles the special cases.
        
    '''
    def __init__(self, parent):
        super().__init__(parent)
        
        #Creating a HenryDAO object and using it to get all the needed information from the database.
        self.HenryDAO_object = HenryDAO()
        self.publisher_info = HenryDAO.getPublisherData(self.HenryDAO_object)
        self.publisher_and_book_info = HenryDAO.getPublisherandBookData(self.HenryDAO_object)
        self.branch_and_copies_info = HenryDAO.getBranchandCopiesData(self.HenryDAO_object)
        self.HenryDAO_object.close()
        
        self.publisher_lab = ttk.Label(self)
        self.publisher_lab.grid(row=5,column=3)
        self.publisher_lab['text'] = "Publisher Selection:"
        
        self.book_lab = ttk.Label(self)
        self.book_lab.grid(row=5, column=4)
        self.book_lab['text'] = "Book Selection:"
        
        #Creating and populating the publisher combobox.
        self.publisher_combo = ttk.Combobox(self, width=20, state="readonly")
        self.publisher_combo.grid(row=6,column=3)
        self.publisher_combo['values'] = [t[1] for t in self.publisher_info.publisher_list if t[0] in (v[0] for v in self.publisher_and_book_info.publisher_and_book_list)]
        self.publisher_combo.current(0)
        self.publisher_combo.bind("<<ComboboxSelected>>", self.publisher_selected)
        
        #Creating and populating the book combobox.
        self.book_combo = ttk.Combobox(self, width=35, state="readonly")
        self.book_combo.grid(row=6,column=4)
        self.book_combo['values'] = [t[2] for t in self.publisher_and_book_info.publisher_and_book_list if t[1] == 'Back Bay Books']
        self.book_combo.current(0)
        self.book_combo.bind("<<ComboboxSelected>>", self.book_selected)
        
        #Creating the Price label.
        self.price = ttk.Label(self)
        self.price.grid(row=6,column=5)
        self.price['text'] = "Price: $" + str(self.publisher_and_book_info.publisher_and_book_list[0][3])
        
        #Creating and Populating the Treeview.
        self.av = ttk.Treeview(self, columns=('Branch', 'Copies'), show='headings', selectmode='extended')
        self.av_lab = ttk.Label(self)
        self.av_lab.grid(row=1,column=4)
        self.av_lab['text'] = "Available Copies"
        self.av.heading('Branch', text='Branch Name')
        self.av.heading('Copies', text='Copies Available')
        self.av.grid(row=2,column=4)
        for row in [(t[2], t[3]) for t in self.branch_and_copies_info.branch_and_copies_list if t[1] == self.book_combo['values'][0]]:
            self.av.insert("", "end", values=[row[0], row[1]])
            
    def publisher_selected(self, event=None):
        #Updating the book combobox.
        self.book_combo.set('')
        self.book_combo['values'] = [t[2] for t in self.publisher_and_book_info.publisher_and_book_list if t[1] == self.publisher_combo.get()]
        #Updating the price.
        title = self.book_combo['values'][0]
        price = [t[3] for t in self.publisher_and_book_info.publisher_and_book_list if t[2] == title][0]
        self.price.config(text = "Price: $" + str(price))
        self.book_combo.current(0)
        #Updating the Treeview while handling special cases.
        for record in self.av.get_children():
            self.av.delete(record)
        if (self.publisher_combo.get() == 'Course Technology'):
            branch_and_copy = [(t[2], t[3]) for t in self.branch_and_copies_info.branch_and_copies_list if (t[1] == self.book_combo['values'][0])]
            self.av.insert("", "end", values = [branch_and_copy[0][0], branch_and_copy[0][1]])
        else:
            for row in list(set((t[2], t[3]) for t in self.branch_and_copies_info.branch_and_copies_list if (t[1] == self.book_combo['values'][0]))):
                self.av.insert("", "end", values = [row[0], row[1]])
        
    def book_selected(self, event=None):
        #Updating the price and Treeview while handling the special cases.
        for record in self.av.get_children():
            self.av.delete(record)
        if (self.publisher_combo.get() == 'Course Technology') and (self.book_combo.current() == 0):
            price = [t[3] for t in self.publisher_and_book_info.publisher_and_book_list if (t[2] == self.book_combo.get())][0]
            branch_and_copy = [(t[2], t[3]) for t in self.branch_and_copies_info.branch_and_copies_list if (t[1] == self.book_combo.get())][0]
            self.av.insert("", "end", values = [branch_and_copy[0], branch_and_copy[1]])
        elif (self.publisher_combo.get() == 'Course Technology') and (self.book_combo.current() == 1):
            price = [t[3] for t in self.publisher_and_book_info.publisher_and_book_list if (t[2] == self.book_combo.get())][1]
            branch_and_copy = [(t[2], t[3]) for t in self.branch_and_copies_info.branch_and_copies_list if (t[1] == self.book_combo.get())][1]
            self.av.insert("", "end", values = [branch_and_copy[0], branch_and_copy[1]])
        else:
            price = [t[3] for t in self.publisher_and_book_info.publisher_and_book_list if (t[2] == self.book_combo.get())][0]
            for row in list(set((t[2], t[3]) for t in self.branch_and_copies_info.branch_and_copies_list if (t[1] == self.book_combo.get()))):
                self.av.insert("", "end", values=[row[0], row[1]])
        self.price.config(text = "Price: $" + str(price))


if __name__ == "__main__":
    main()