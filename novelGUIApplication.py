'''
In the main window, there are 5 options: Enter Novel, Novel Report, Enter Author,
Author Report and Exit. Reports allow you to see the data in the database and
entering allows you to add to the databse. When you enter a novel, you can choose
an author and then fill in the other missing information. When you enter a
author, you fill in all the data. I added the enter author because adding a novel
from an author that's not already in the database is easier. An error message may
pop up while entering data due to incorrect formatting or other erros mentioned
in the message.

By Ben
'''

from tkinter import *
import tkinter as tk
from tkinter import messagebox
import sqlite3 as sq

con = sq.connect("novel.db")
c = con.cursor()

#Query Functions (Model)
def get_authors():
    res = c.execute("SELECT * FROM Author")
    data = c.fetchall()
    return data

def add_author(name, nationality, sex):
    ins_str = "INSERT INTO Author (AuthorName, AuthorNationality, AuthorSex) VALUES ('" + str(name) + "', '" + str(nationality) + "', '" + str(sex) + "');"
    res = c.execute(ins_str)
    con.commit()

def get_novels():
    res = c.execute("SELECT NovelID, ISBN, Title, Price, AuthorName FROM Novel JOIN Author WHERE Novel.AuthorID = Author.AuthorID")
    data = c.fetchall()
    return data

def add_novel(isbn, title, price, authorid):
    ins_str = "INSERT INTO Novel (ISBN, Title, Price, AuthorID) VALUES (" + str(isbn) + ", '" + str(title) + "', " + str(price) + ", " + str(authorid) + ");"
    res = c.execute(ins_str)
    con.commit()

#Database Selections 
def author_lb(w, f, authors):
    lblauthor = Label(f,text = "AuthorID, AuthorName, AuthorNationality, AuthorSex").pack(side = TOP)

    Lb = Listbox(f, height = 8, width = 26,font=("arial", 12), exportselection = False) 
    Lb.pack(side = TOP, fill = Y)
                
    scroll = Scrollbar(w, orient = VERTICAL)
    scroll.config(command = Lb.yview)
    scroll.pack(side = RIGHT, fill = Y)
    Lb.config(yscrollcommand = scroll.set)
    

    i = 0
    for author in authors:
        Lb.insert(i, author)
        i += 1
    Lb.selection_set(first = 0)

    return Lb

#Menu Functions (View)
def render_menu():
    window = Tk()
    window.title("Novel Main Menu")
    window.geometry("200x120")

    novel_res = Button(window, text="Enter Novel", command = render_novel_request)
    novel_res.pack()

    novel_rpt = Button(window, text="Novel Report", command = render_novel_report)
    novel_rpt.pack()

    author_res = Button(window, text="Enter Author", command = render_author_request)
    author_res.pack()

    author_rpt = Button(window, text="Author Report", command = render_author_report)
    author_rpt.pack()

    ext = Button(window, text="Exit", command = lambda:end_program(window))
    ext.pack()
    window.mainloop()

def end_program(w):
    con.close()
    w.destroy()

#Novel Report and Request
def render_novel_report():
    novels = get_novels()
    tbl = "NovelID, ISBN, Title, Price, AuthorName\n \n"
    for row in novels:
        for field in row:
            tbl += str(field)
            tbl += ", "
        tbl += "\n \n"
    tbl += ""

    messagebox.showinfo("Report results\n\n", tbl)

def render_novel_request():
    nov_req_win = Tk()
    nov_req_win.title("Novel Request")
    nov_req_win.geometry("400x400")

    left_frame = Frame(nov_req_win)
    left_frame.pack(side = LEFT)

    i = tk.StringVar(nov_req_win)
    t = tk.StringVar(nov_req_win)
    p = tk.StringVar(nov_req_win)


    lbl = Label(left_frame, text = "Choose an ISBN, Title, Price and Author.").pack()
    isbn_lbl = Label(left_frame, text = "ISBN").pack()
    isbn = Entry(left_frame, text="", textvariable = i).pack()
    title_lbl = Label(left_frame, text = "Title").pack()
    title = Entry(left_frame, text="", textvariable = t).pack()
    price_lbl = Label(left_frame, text = "Price").pack()
    price = Entry(left_frame, text="", textvariable = p).pack()

    option_frame = Frame(nov_req_win)
    option_frame.pack(side = RIGHT)

    authors = get_authors()
    authorlb = author_lb(nov_req_win, option_frame, authors)

    rpt = Button(left_frame, text="Enter Novel", command= lambda: check_and_enter_selection_novel(i.get(), t.get(), p.get(), authors[authorlb.curselection()[0]][0])).pack()

    nov_req_win.mainloop()

#Author Report and Request
def render_author_report():
    authors = get_authors()
    tbl = "AuthorID, AuthorName, AuthorNationality, AuthorSex\n \n"
    for row in authors:
        for field in row:
            tbl += str(field)
            tbl += ", "
        tbl += "\n \n"
    tbl += ""

    messagebox.showinfo("Report results\n\n", tbl)

def render_author_request():
    aut_req_win = Tk()
    aut_req_win.title("Author Request")
    aut_req_win.geometry("400x400")

    left_frame = Frame(aut_req_win)
    left_frame.pack()

    nam = tk.StringVar(aut_req_win)
    nat = tk.StringVar(aut_req_win)
    s = tk.StringVar(aut_req_win)


    lbl = Label(left_frame, text = "Choose a Name, Nationality and Sex.").pack()
    name_lbl = Label(left_frame, text = "Name").pack()
    name = Entry(left_frame, text="", textvariable = nam).pack()
    nationality_lbl = Label(left_frame, text = "Nationality").pack()
    nationality = Entry(left_frame, text="", textvariable = nat).pack()
    sex_lbl = Label(left_frame, text = "Sex").pack()
    sex = Entry(left_frame, text="", textvariable = s).pack()

    rpt = Button(left_frame, text="Enter Author", command= lambda: check_and_enter_selection_author(nam.get(), nat.get(), s.get())).pack()

    aut_req_win.mainloop()

#Final Addition Check (Controller)
def check_and_enter_selection_novel(i, t, p, a):
    try:
        
        add_novel(i, t, p, a)
        messagebox.showinfo("Success!", "Your novel had been added.")

    except:
        messagebox.showinfo("Error- Try again", "\nPossible errors:  \nThere is already a novel with that combination, you chose an invalid author\nThe price, title or isbn is in an invalid format, \nSomeone else is entering a novel at the same time.")
        return
    
def check_and_enter_selection_author(nam, nat, s):
    try:
        add_author(nam, nat, s)
        messagebox.showinfo("Success!", "Your author had been added.")

    except:
        messagebox.showinfo("Error- Try again", "\nPossible errors:  \nThere is already an author with that combination\nThe name, nationality or sex is in an invalid format, \nSomeone else is entering an author at the same time.")
        return

#Main Program
render_menu()


