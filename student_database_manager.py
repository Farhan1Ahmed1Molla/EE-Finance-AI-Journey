import sqlite3
connection = sqlite3.connect("students.db")
cursor = connection.cursor()

cursor.execute(""" CREATE TABLE IF NOT EXISTS students (id INTEGER PRIMARY KEY, name TEXT , age INTEGER, department TEXT)""")

connection.commit()


def add_student():
    name = input("Enter Name:  ")
    age = input("Enter Age:  ")
    department = input("Enter department:  ")

    if not name.isalpha():
        print("Name must contain only letters")
        return

    if not age.isdigit():
        print("Age must only contain digits")
        return
    age = int(age)

    if not department.isalpha():
        print("department must only contain letters")
        return

    cursor.execute("""INSERT INTO students (name, age, department) VALUES(?, ?, ?)""",(name, age, department))

    connection.commit()

    print("student added successfully")

def view_student():

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    for student in students:
        print(f"ID : {student[0]}")
        print(f"Name : {student[1]}")
        print(f"Age : {student[2]}")
        print(f"Department : {student[3]}")
        print("-" * 40)

def search_student():
    name = input("Enter Name:  ")

    cursor.execute("SELECT * FROM students WHERE name =?",(name,))
    student = cursor.fetchone()

    if student is None:
        print(f"Student: '{name}' does not exist in the database")
        return

    print(f"ID : {student[0]}")
    print(f"Name : {student[1]}")
    print(f"Age : {student[2]}")
    print(f"Department : {student[3]}")

def update_student():
    student_id = input("Enter student ID:  ")

    if not student_id.isdigit():
        print("Student ID must contain only digits")
        return

    student_id = int(student_id)

    cursor.execute("SELECT * FROM students WHERE id =?",(student_id,))

    student = cursor.fetchone()

    if student is None:
       print(f"Student ID: '{student_id}' does not exist in the database")
       return

    name = input("Enter new name: ")
    age = input("Enter new age: ")
    department = input("Enter new department: ")

    if not name.isalpha():
        print("Name must contain letters")
        return

    if not age.isdigit():
        print("Age must only contain digits")
        return
    age = int(age)

    if not department.isalpha():
        print("Department must only contain letters")
        return

    cursor.execute("""UPDATE students SET name =?, age = ?, department = ? WHERE id = ?""",(name, age, department,student_id))

    connection.commit()

    print("Student updated successfully")

def delete_student():
    student_id = input("Enter Student ID:  ")

    if not student_id.isdigit():
        print("Student ID must contain only digits")
        return

    student_id = int(student_id)

    cursor.execute("""SELECT * FROM students WHERE id = ?""",(student_id,))

    student = cursor.fetchone()

    if student is None:
        print(" Student ID not found in database")
        return

    cursor.execute("""DELETE FROM students WHERE id = ?""",(student_id,))

    connection.commit()

    print("Student ID successfully deleted")

def welcome_menu():
    print("1.Add student")
    print("2.View student")
    print("3.Search student")
    print("4.Update student")
    print("5.Delete student")
    print("6.Exit")

option = ""

while option != "6":
    welcome_menu()

    option = input("Enter Option:  ")

    if option == "1":
        add_student()

    elif option == "2":
        view_student()

    elif option == "3":
        search_student()

    elif option == "4":
        update_student()

    elif option == "5":
        delete_student()

    elif option == "6":
        print("Goodbye")

    else:
        print("Invalid option")

connection.close()
