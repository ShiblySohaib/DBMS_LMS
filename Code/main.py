import mysql.connector
import easygui as eg
from datetime import date

con = mysql.connector.connect(host="localhost", user="root", passwd="", autocommit=True)
c = con.cursor(buffered=True)  # without a buffered cursor, the results are lazily loaded
c.execute("create database if not exists library_db")
c.execute("use library_db")
c.execute("create table if not exists books (b_id varchar(5) primary key,b_name varchar(50),genre varchar(50), author varchar(50), available varchar(5) Default 'yes')")
c.execute("create table if not exists issue_details(b_id varchar(5), student_id varchar(10), student_Name varchar(50) Not null,issue_date date, foreign key(b_id) references books(b_id))")
c.execute("create table if not exists librarian(user_name varchar(50) Not null,user_pass varchar(50) Not null)")


def add_book():
    try:
        add_book_names = ["Book ID", "Book name", "Genre","Author"]
        add_book_values = eg.multenterbox("Enter Book information", "New book entry", add_book_names)
        sql = 'insert into books(b_id,b_name,genre,author) values(%s,%s,%s,%s)'
        c.execute(sql, add_book_values)
    except:
        return

def delete_book():
    try:
        delete_book_names = ["Book ID"]
        delete_book_values = eg.multenterbox("Enter Book information", "Delete Book", delete_book_names)
        c.execute(f"delete from books where b_id= {delete_book_values[0]}")
        display_books()
    except:
        return

def issue_book():
    sql = "SELECT * FROM `books` ORDER BY cast(b_id as int)"
    c.execute(sql)
    issue_book_names = ["Book id","Student Name","Student ID"]
    issue_book_values = eg.multenterbox("Enter Book information", "Issue Book", issue_book_names)
    c.execute(f"select b_id from books where b_id = '{issue_book_values[0]}' and available='YES'")
    res = c.fetchall()
    if len(res)==0:
        eg.msgbox("Book is not available")
        return
    today = str(date.today())
    c.execute(f"insert into issue_details values('{issue_book_values[0]}','{issue_book_values[2]}','{issue_book_values[1]}','{today}')")
    c.execute("update books set available='no' where b_id='"+issue_book_values[0]+"'")

def print_librarian(data):
    result = "===============================================================================\n"
    result += "|"+"%39s"%"User Name|"+"%39s"%"Password |"+"\n"
    result += "===============================================================================\n"
    for i in data:
        result+="|"+"%37s"%i[0]+' |'+"%37s"%i[1]+' |'+"\n"
    result += "===============================================================================\n"
    eg.msgbox(result)
    admin()

def show_librarian():
    sql = "SELECT * FROM librarian ORDER BY user_name desc;"
    c.execute(sql)
    my_result = c.fetchall()
    print_librarian(my_result)

def add_librarian():
    try:
           librarian_names = ["User name", "Password"]
           librarian_values = eg.multenterbox("Enter information", "Admin",  librarian_names)
           sql = 'insert into librarian(user_name,user_pass) values(%s,%s)'
           c.execute(sql, librarian_values)
    except:
        return   

def delete_librarian():
    try:
        delete_librarian_names = ["User name"]
        delete_librarian_values = eg.multenterbox("Enter librarian name", "Delete librarian", delete_librarian_names)
        c.execute(f"delete from librarian where user_name = '{delete_librarian_values[0]}'")
    except:
        admin()

def admin():
    admin_ch = eg.buttonbox(""" Select an option """, choices=['Show all librarian','Add librarian', 'Delete librarian','Exit'])
    if admin_ch == 'Show all librarian':
        show_librarian()
    elif admin_ch == 'Add librarian':
        add_librarian()
    elif admin_ch == 'Delete librarian':
        delete_librarian()
    else:
        home()

def return_book():
    return_book_names = ["Book ID"]
    return_book_values = eg.multenterbox("Enter information", "Return book", return_book_names)
    c.execute(f"select issue_details. *, books.b_name FROM issue_details INNER JOIN books on issue_details.b_id = books.b_id HAVING issue_details.b_id = '{return_book_values[0]}'")
    res = c.fetchall()
    if len(res)==0:
        eg.msgbox('Book is not issued')
        return
    res = res[0]
    days = (date.today()-res[3]).days
    print(days)
    if days>14:
        fine = (days-14)*20
        payment = eg.ynbox(f'{fine} BDT fine is due. Payment complete?')
        if payment == False:
            eg.msgbox("Payment incomplete. Book was not returned.")
            return
    c.execute("update books set available='yes' where b_id='" + return_book_values[0] + "'")
    c.execute("delete from issue_details where b_id = %s", (return_book_values[0],))
    eg.msgbox(f"'{res[4]}' book has been successfully returned by {res[1]}")


def print_books(data):
    result = "===============================================================================\n"
    result += "|"+"%15s"%"Book ID |"+"%16s"%"Book Title |"+"%15s"%"Genre |"+"%17s"%"Author |"+"%15s"%"Availability |"+"\n"
    result += "===============================================================================\n"
    for i in data:
        result+="|"+"%13s"%i[0]+' |'+"%14s"%i[1]+' |'+"%13s"%i[2]+' |'+"%15s"%i[3]+' |'+"%13s"%i[4]+" |"+"\n"
    result += "===============================================================================\n"
    eg.msgbox(result)



def print_issuedbooks(data):
    result = "===============================================================================\n"
    result += "|"+"%12s"%"Book ID |"+"%17s"%"Book Title |"+"%17s"%"Student ID |"+"%17s"%"Student Name |"+"%15s"%"Issue date |"+"\n"
    result += "===============================================================================\n"
    for i in data:
        result+="|"+"%10s"%i[0]+' |'+"%15s"%i[4]+' |'+"%15s"%i[1]+' |'+"%15s"%i[2]+" |"+"%13s"%i[3]+" |"+"\n"
    result += "===============================================================================\n"
    eg.msgbox(result)


def display_books():
    sql = "SELECT * FROM `books` ORDER BY cast(b_id as int);"
    c.execute(sql)
    my_result = c.fetchall()
    print_books(my_result)



def search_book():
    try:
        value = eg.buttonbox("Search by:", choices=['Title','Author','Genre'])
        if value == 'Title':
            title = eg.enterbox("Enter title")
            c.execute(f"SELECT * FROM `books` where b_name like '%{title}%' and available = 'YES' ORDER BY cast(b_id as int)")
            res = c.fetchall()
            if len(res)==0:
                eg.msgbox("No books found")
                exit()
            else:
                print_books(res)
                exit()
        elif value == 'Author':
            author = eg.enterbox("Enter title")
            c.execute(f"SELECT * FROM `books` where author like '%{author}%' and available = 'YES' ORDER BY cast(b_id as int)")
            res = c.fetchall()
            if len(res)==0:
                eg.msgbox("No books found")
                exit()
            else:
                print_books(res)
                exit()
        else:
            genre = eg.enterbox("Enter title")
            c.execute(f"SELECT * FROM `books` where genre like '%{genre}%' and available = 'YES' ORDER BY cast(b_id as int)")
            res = c.fetchall()
            if len(res)==0:
                eg.msgbox("No books found")
                exit()
            else:
                print_books(res)
                exit()
    except:
        return


def display_menu():
    choice = eg.buttonbox("Select a choice", choices=['All books', 'Issued books', 'Particular book'])
    if choice == 'All books':
        display_books()
    elif choice == 'Issued books':
        display_issued_books()
    elif choice == 'Particular book':
        search_book()
    else:
        print('wrong choice')



def display_issued_books():
    c.execute("select issue_details. *, books.b_name from issue_details INNER JOIN books on issue_details.b_id = books.b_id ORDER BY issue_details.issue_date desc")
    my_result = c.fetchall()
    print_issuedbooks(my_result)



def a_menu():
    try:
        Admin_names = ["User Name", "Password"]
        Admin_values = eg.multenterbox("Enter your information", "Personal Information", Admin_names)
        if Admin_values[0] == 'a' and Admin_values[1] == '123':
            admin()
        else:
            eg.msgbox('Wrong username or Password,try again')
            home()
    except:
        return


def l_menu():
    while True:
        ch = eg.buttonbox(""" Select an option """, choices=['Add book', 'Issue book','Display books','Return book','Delete book' ,'Exit'])
        if ch == 'Add book':
            add_book()
        elif ch == 'Issue book':
            issue_book()
        elif ch == 'Return book':
            return_book()
        elif ch == 'Display books':
            display_menu()
        elif ch == 'Delete book':
            delete_book()
        else:
            return
def s_menu():
    try:
        print("sdf")
    except:
        home()

def home():
    while True:
        user_type = eg.buttonbox("Select User type", choices=['Admin','Librarian', 'Student','Exit'])

        if user_type == "Admin":
            try:
                a_menu()
                continue
            except:
                continue

        elif user_type == "Librarian":
            try:
                field_names = ["User Name", "Password"]
                field_values = eg.multenterbox("Enter your information", "Personal Information", field_names)
                sql = f"Select user_name,user_pass from librarian where user_name='{field_values[0]}' and user_pass='{field_values[1]}'"
                c.execute(sql)
                librarian_res = c.fetchall()
                if len(librarian_res)!=0:
                    l_menu()
                    continue
                else:
                    eg.msgbox('Wrong username or Password,try again')
                    home()
            except:
                continue       

        elif user_type == "Student":
            try:
                s_menu()
                continue
            except:
                continue
        else:
            return
home()