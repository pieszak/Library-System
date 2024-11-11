import sqlite3 #this imports sql module that will allow us to 
import os #used so we can clear the terminal and improve UI
import hashlib #imports hashing module for the login module

 #hashlib.sha256("pass123".encode()).hexdigest()


def LoginSystem(): #this function is the log-in gateway that controls access to the library system.
    valid_username = "user123" #this is the username for the system
    hashed_password = "9b8769a4a742959a2d0298c36fb70623f2dfacda8436237df08d8dfd5b37374c" #this is the hashed password - never store password in plain text

    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest() #encodes the entered password for comparison of saved hash (see above)

    def login(): #this function manages the login process
        print("Welcome to the Login Page")
        username = input("Enter your username: ") #user input of username
        password = input("Enter your password: ") #user input of password
        if username == valid_username and hash_password(password) == hashed_password: #cleartext password gets hashed using hash_password(password)
            print("Login successful! Welcome, " + username + "!") #more personalised to increase user experience
            return 0 #the function has now completed it's task and returns 0, closing the function.
        else:
            print("Invalid username or password. Please try again.")
            LoginSystem() #resets the function, so we can have another go at crackin' the password.
    login() #loopback to prevent user bypass. Only way to exit the LoginSystem() function is to enter correct credentials

class LibraryManagementSystemSQLite: #Put it in a class so we can reuse on another system, especially if we wanna put it on backend.
    def __init__(self, db_filename='library1.db'):
        self.conn = sqlite3.connect(db_filename) #connecting to sql database = 'library.db'
        self.cursor = self.conn.cursor()
        self.create_table() #sets off create_table function.

    def create_table(self): #creates table for us! the CAPITALS are the data types we use.
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                isbn TEXT PRIMARY KEY, 
                name TEXT,
                author TEXT,
                date TEXT,
                description TEXT,
                quantity INTEGER
            )
        ''')
        self.conn.commit() #commit allows us to edit database files

    def add_book(self, isbn, name, author, date, description, quantity): #add new books to the data base
        try:
            self.cursor.execute('''
                INSERT INTO books (isbn, name, author, date, description, quantity)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (isbn, name, author, date, description, quantity))
            self.conn.commit()
            print(f"Book '{name}' with ISBN {isbn} added successfully.")
        except sqlite3.IntegrityError:
            print(f"Book with ISBN {isbn} already exists. Use the update function to modify details.")

    def update_quantity(self, isbn, new_quantity): #update the quantity of books
        try:
            self.cursor.execute('''
                UPDATE books SET quantity = ? WHERE isbn = ?
            ''', (new_quantity, isbn))
            self.conn.commit()
            print(f"Quantity for book with ISBN {isbn} updated to {new_quantity}.")
        except sqlite3.Error:
            print(f"Book with ISBN {isbn} not found.")

    def delete_book(self, isbn): # delete books
        try:
            self.cursor.execute('DELETE FROM books WHERE isbn = ?', (isbn,))
            self.conn.commit()
            print(f"Book with ISBN {isbn} deleted successfully.")
        except sqlite3.Error:
            print(f"Book with ISBN {isbn} not found.")

    def update_description(self, isbn, new_name, new_author, new_date, new_description): # update the description of the books
        try:
            self.cursor.execute('''
                UPDATE books
                SET name = ?, author = ?, date = ?, description = ?
                WHERE isbn = ?
            ''', (new_name, new_author, new_date, new_description, isbn))
            self.conn.commit()
            print(f"Details for book with ISBN {isbn} updated successfully.")
        except sqlite3.Error:
            print(f"Book with ISBN {isbn} not found.")

    def check_status(self, isbn): #check the status of books
        try:
            result = self.cursor.execute('SELECT quantity FROM books WHERE isbn = ?', (isbn,))
            row = result.fetchone()
            if row is not None:
                quantity = row[0]
                if quantity > 0:
                    print(f"Book with ISBN {isbn} is in stock.")
                else:
                    print(f"Book with ISBN {isbn} is out of stock.")
            else:
                print(f"Book with ISBN {isbn} not found.")
        except sqlite3.Error:
            print(f"Book with ISBN {isbn} not found.")

    def export_books_to_txt(self, filename):
        try:
            with open(filename, 'w') as file:
                result = self.cursor.execute('SELECT * FROM books')
                for row in result.fetchall():
                    file.write(f"ISBN: {row[0]}\n")
                    file.write(f"Name: {row[1]}\n")
                    file.write(f"Author: {row[2]}\n")
                    file.write(f"Date: {row[3]}\n")
                    file.write(f"Description: {row[4]}\n")
                    file.write(f"Quantity: {row[5]}\n")
                    file.write("\n")
            print(f"Books exported to {filename} successfully.")
        except sqlite3.Error:
            print("Error exporting books to file.")

    def print_all_books(self):
        try:
            result = self.cursor.execute('SELECT * FROM books')
            for row in result.fetchall():
                print(f"ISBN: {row[0]}")
                print(f"Name: {row[1]}")
                print(f"Author: {row[2]}")
                print(f"Date: {row[3]}")
                print(f"Description: {row[4]}")
                print(f"Quantity: {row[5]}")
                print("\n")
        except sqlite3.Error:
            print("Error retrieving books from the database.")


def main(): #def main=
    os.system('cls||clear') # clears the terminal. Makes it more clean
    #Selection for the system
    foo =   int(input("Hello welcome to the USW Library!\nPlease select one of the following options:\n1. Add Book\n2. Update Quantity\n3. Check Book Status\n4. Update Description\n5. Delete Book\n6. Print all inventory\n7. Save and Quit\n"))
    if foo == 1:
        checker = str(input("You have selected ADD BOOK\nIs this the correct selection [y/n]: "))
        if checker == 'n':
              main()
        if checker == 'y':
            print("Please input the following information:")
            temp1 = str(input("ISBN Number: "))
            temp2 = str(input("Book Name: "))
            temp3 = str(input("Author: "))
            temp4 = str(input("Date of publication: "))
            temp5 = str(input("Book Description: "))
            temp6 = int(input("Quantity of books: "))
            library_system.add_book(temp1, temp2, temp3, temp4, temp5, temp6)
            print("The above information has been processed by the system!\nThank you!")
            input("Press any KEY to continue")
            main()

    if foo == 2:
        checker = str(input("You have selected UPDATE QUANTITY\nIs this the correct selection [y/n]: "))
        if checker == 'n':
              main()
        if checker == 'y':
            print("\n Please input the following information:")
            temp1 = str(input("ISBN Number: "))
            temp2 = int(input("Quantity of books: "))
            library_system.update_quantity(temp1, temp2)
            input("The above information has been processed by the system!\nPress any KEY to continue")
            main() #Allows for loop

    if foo == 3:#CHECK IF BOOK EXISTS
      checker = str(input("You have selected CHECK STATUS\nIs this the correct selection [y/n]: "))
      if checker == 'n':
          main()
      if checker == 'y':
          print("\n Please input the following information:")
          temp1 = str(input("ISBN Number: "))
          library_system.check_status(temp1)
          input("Press any KEY to continue")
          main()
          
    if foo == 4: #UPDATE DESCRIPTION
      checker = str(input("You have selected UPDATE DESCRIPTION\nIs this the correct selection [y/n]: "))
      if checker == 'n':
          main()
      if checker == 'y':
          print("\n Please input the following information:")
          temp1 = str(input("ISBN Number: "))
          temp2 = str(input("Book Name: "))
          temp3 = str(input("Author: "))
          temp4 = str(input("Date of publication: "))
          temp5 = str(input("Book Description: "))
          library_system.update_description(temp1, temp2, temp3, temp4, temp5)
          input("The above information has been processed by the system!\nPress any KEY to continue")
          main()

    if foo == 5:#DELETE THE BOOK
      checker = str(input("You have selected DELETE BOOK\nIs this the correct selection [y/n]: "))
      if checker == 'n':
          main()
      if checker == 'y':
          print("\n Please input the following information:")
          temp1 = str(input("ISBN Number: "))
          library_system.delete_book(temp1)
          input("Press any KEY to continue")
          main()

    if foo == 6: #PRINTS ALL BOOKS
      checker = str(input("You have selected PRINT ALL BOOKS\nIs this the correct selection [y/n]: "))
      if checker == 'n':
          main()
      if checker == 'y':
          library_system.print_all_books()
          input("Press any KEY to continue")
          main()

    if foo == 7:
      checker = str(input("You have selected SAVE AND QUIT\nIs this the correct selection [y/n]: "))
      if checker == 'n':
          main()
      if checker == 'y':
          library_system.conn.close() #closes our database connection.
          input("Library saved!\nPress any KEY to continue")
          print("Quiting the programme...")
          exit()
    
    else:
        input("Incorrect input. Please try again!\nPress any KEY to continue")
          
library_system = LibraryManagementSystemSQLite() #assign library_system variable to the class so it can call on itself when doing operations.
LoginSystem() #login system is triggered 
main() # after final complete