import mysql.connector
import easygui
asdfsdf

con = mysql.connector.connect(host="localhost", user="root", passwd="", autocommit=True)
c = con.cursor(buffered=True)  # without a buffered cursor, the results are lazily loaded
c.execute("create database if not exists library_db")
c.execute("use library_db")
c.execute("create table if not exists books (b_id varchar(5) primary key,b_name varchar(50),genre varchar(50), author varchar(50), available varchar(5) Default 'yes')")
c.execute(
    "create table if not exists issue_details(b_id varchar(5), student_id varchar(10), student_Name varchar(50) Not null,foreign key(b_id) references books(b_id))")


def add_book():
    # Define the field names
    add_book_names = ["Book ID", "Book name", "Genre","Author"]

   # Display the form
    add_book_values = easygui.multenterbox("Enter Book information", "New book entry", add_book_names)

    sql = 'insert into books(b_id,b_name,genre,author) values(%s,%s,%s,%s)'
    c.execute(sql, add_book_values)


def delete_book():
    delete_book_names = ["Book ID"]
    delete_book_values = easygui.multenterbox("Enter Book information", "Delete Book", delete_book_names)
    c.execute(f"delete from books where b_id= {delete_book_values[0]}")
    display_books()


def issue_book():
    # s_name = input("Enter your Name : ")
    # s_id = input("Enter Reg No : ")
    # book = input("Enter Book name : ")
    # c.execute("select b_id from books where b_name = '" + book + "' and available='YES'")

    issue_book_names = ["Name","Reg no","Book name"]
    issue_book_values = easygui.multenterbox("Enter Book information", "Issue Book", issue_book_names)
    c.execute("select b_id from books where b_name = '" + issue_book_values[2] + "' and available='YES'")
    book_id = c.fetchone()
    bid = book_id[0]
    print(bid)
    a = "insert into issue_details values(%s,%s,%s)"
    data = (bid, issue_book_values[1], issue_book_values[0])
    c.execute(a, data)
    c.execute("update books set available='no' where b_id='"+bid+" '")
    print(issue_book_values[2], " book issued to ", issue_book_values[0])


def return_book():
    name = input("Enter your Name : ")
    bid = input("Enter book id : ")
    c.execute("update books set available='yes' where b_id='" + bid + "'")
    c.execute("delete from issue_details where b_id = %s", (bid,))
    print("book id ", bid, "book returned by ", name)


def display_books():
    sql = "select * from books"
    c.execute(sql)
    my_result = c.fetchall()
    print("Book ID\t Book title\t\tAuthor\tAvailable")
    for i in my_result:
        print(i[0], "\t", i[1], "  \t", i[2], "\t", i[3])


def select_book():
    book = input('enter the name of book')
    sql = "select * from books where b_name= '" + book + "'"
    c.execute(sql)
    my_result = c.fetchall()
    print("Book ID\t Book title\t\tAuthor\tAvailable")
    for i in my_result:
        print(i[0], "\t", i[1], "\t", i[2], "\t", i[3])


def display_issued_books():
    c.execute("select issue_details. *, books.b_name from issue_details, books where issue_details.b_id = books.b_id")
    my_result = c.fetchall()
    print("list of issued books:")
    print("Book_id  book_name  Reg_no  Student_Name")
    for i in my_result:
        print(i[0], "  ", i[3], "  ", i[1], "  ", i[2])


def modify_info():
    bid = input("Enter BOOK ID : ")
    c.execute(f"select * from books where b_id={bid}")
    print("1. Modify name")
    print("2. Modify Author")
    print("3. Modify Genre")
    print("\n\n")
    opt = input("Enter your choice: ")
    if opt == '1':
        title = input("Enter book Name : ")
        c.execute(f'UPDATE books SET books.b_name = "{title}" WHERE books.b_id = "{bid}"')
    elif opt == '2':
        author = input("Enter author name : ")
        c.execute(f'UPDATE books SET books.author = "{author}" WHERE books.b_id = "{bid}"')
    elif opt == '3':
        genre = input("Enter genre name : ")
        c.execute(f'UPDATE books SET books.genre = "{genre}" WHERE books.b_id = "{bid}"')
    else:
        print("Invalid choice")


# Display a box with choices
user_type = easygui.buttonbox("Select User typer.", choices=['Librarian', 'Student'])



# if user_type == "Librarian":
#     # Define the field names
#     field_names = ["User Name", "Password"]

#     # Display the form
#     field_values = easygui.multenterbox("Enter your information", "Personal Information", field_names)



# if field_values[0] == 'admin' and field_values[1] == '123':
if True:
    print('Welcome Admin')
    while True:
        ch = easygui.buttonbox(""" Select an option """, choices=['Add book', 'Issue book','Display books','Return book','Delete book','Modify info' ,'Exit'])
        if ch == 'Add book':
            add_book()
        elif ch == 'Issue book':
            issue_book()
        elif ch == 'Return book':
            return_book()
        elif ch == 'Display books':
            choice = easygui.buttonbox("Select a choice", choices=['All books', 'Issued books', 'Particular book'])
            if choice == 'All books':
                display_books()
            elif choice == 'Issued books':
                display_issued_books()
            elif choice == 'Particular book':
                select_book()
            else:
                print('wrong choice')
        elif ch == 'Delete book':
            delete_book()
        elif ch == 'Modify info':
                modify_info()
        else:
            break
else:
    print("Wrong username or Password,try again")
