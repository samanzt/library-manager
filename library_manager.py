# ================================================== imports ================================================
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import backend
from datetime import date

# ================================================== setting ==================================================
window = Tk()
window.geometry("870x400")
window.resizable(False, False)
window.title("Library Manager")


# ================================================== functions ===============================================
def show_all_books():
    tree.delete(*tree.get_children())
    books = backend.viewAll()
    for book in books:
        tree.insert('', 'end', iid=book[0], values=book[1:])


def add():
    if len(titleText.get()) > 0 and len(authorText.get()) > 0 and len(yearText.get()) > 0 and len(
            categoryText.get()) > 0:
        if not yearText.get().isdigit():
            messagebox.showwarning("Invalid Year","Year must be numbers only.")
            return


        backend.insert(titleText.get(), authorText.get(), yearText.get(), categoryText.get(), "Available")
        titleText.set("")
        authorText.set("")
        yearText.set("")
        categoryText.set("")
        show_all_books()


selectedRow = None
selectedBookValues = None


def get_selected_row(event):
    global selectedRow
    global selectedBookValues
    selected = tree.focus()
    if selected:
        selectedRow = int(selected)

    if not selected:
        return
    values = tree.item(selected)["values"]
    selectedBookValues = values
    if not values:
        return
    titleText.set(values[0])
    authorText.set(values[1])
    yearText.set(values[2])
    categoryText.set(values[3])

def delete_selected_book():
    global selectedRow
    if not selectedRow:
        messagebox.showwarning(title="Delete Error", message="Please select a book.")
        return
    if selectedBookValues[4]=="Borrowed":
        messagebox.showwarning("Delete Error","This book is currently borrowed and cannot be deleted.")
        return
    confirm = messagebox.askyesno("Confirm Delete","Are you sure you want to delete this book?")

    if not confirm:
        return

    backend.delete(selectedRow)
    show_all_books()
    selectedRow = None



def update_selected_book():
    global selectedRow
    if not selectedRow:
        messagebox.showwarning(title="Update Error", message="Please select a book.")
        return
    if not yearText.get().isdigit():
        messagebox.showwarning("Invalid Year", "Year must be numbers only.")
        return
    backend.update(selectedRow, titleText.get(), authorText.get(), yearText.get(), categoryText.get(), selectedBookValues[4])

    show_all_books()
    titleText.set("")
    authorText.set("")
    yearText.set("")
    categoryText.set("")
    selectedRow = None



def search_book():
    if not searchText.get():
        show_all_books()
        return
    if not searchByText.get():
        messagebox.showwarning(title="Search Error", message="Please select a search category")
        return
    column_map = {
        "Title": "title",
        "Author": "author",
        "Year": "year",
        "Category": "category",
        "Status": "status"
    }

    column = column_map[searchByText.get()]
    value = searchText.get()
    searched_books = backend.search(column, value)
    tree.delete(*tree.get_children())
    for books in searched_books:
        tree.insert('', 'end', iid=books[0], values=books[1:])


loan_window = None


def open_loan_window():
    global loan_window


    if selectedRow is None:
        messagebox.showwarning(
            "No Book Selected",
            "Please select a book first.")
        return

    if loan_window is not None and loan_window.winfo_exists():
        loan_window.lift()
        return
    #========================== setting ===============================
    loan_window = Toplevel(window)
    loan_window.geometry("650x400")
    loan_window.resizable(False, False)
    loan_window.title("Loan Manager")
    #========================= functions =============================
    selectedLoan=None
    def get_selected_loan(event):
        nonlocal selectedLoan
        selected=loanTree.focus()
        if selected:
            selectedLoan = int(selected)
        if not selected:
            return

    def borrow_book():
        global selectedRow
        global selectedBookValues
        if selectedBookValues[4] == "Borrowed":
            messagebox.showwarning("Borrow Error","This book is already borrowed.")
            return
        if not  borrowedNameText.get():
            messagebox.showwarning("Borrow Error", "Please enter the Borrower's name")
            return
        today=str(date.today())
        backend.borrow_book(selectedRow,selectedBookValues[0],borrowedNameText.get(),today)
        show_all_loans()
        show_all_books()
        selectedRow = None
        selectedBookValues = None

    def return_book():
        nonlocal selectedLoan
        if not selectedLoan:
            messagebox.showwarning("Return Error", "Please select a book.")
            return
        backend.return_loan_book(selectedLoan)
        show_all_loans()
        show_all_books()
        selectedLoan=None


    #========================= frames =================================
    loanTreeFrame=Frame(loan_window)
    loanTreeFrame.grid(row=3, column=0,columnspan=10, sticky="nsew")
    # ========================= labels ================================
    selectedBookLabel = Label(loan_window, text=f"Selected Book : {selectedBookValues[0]} ")
    selectedBookLabel.grid(column=0, row=0, pady=10, columnspan=2, sticky="W")

    borrowedNameLabel = Label(loan_window, text="Borrowed Name:")
    borrowedNameLabel.grid(column=0, row=1, sticky="w")
    # ========================= entries ================================
    borrowedNameText = StringVar()
    borrowedNameEntry = Entry(loan_window, textvariable=borrowedNameText, width=35)
    borrowedNameEntry.grid(column=1, row=1, sticky="w")
    # ========================= buttons ================================
    borrowedBooksButton = Button(loan_window, text="Borrow Book", width=12,command=borrow_book)
    borrowedBooksButton.grid(column=0, row=2, pady=30)

    returnBooksButton = Button(loan_window, text="Return Book", width=12,command=return_book)
    returnBooksButton.grid(column=1, row=2,sticky="w")

    # ========================== treeview ===============================
    columns=("Book Title","Borrower","Loan Date")
    loanTree=ttk.Treeview(loanTreeFrame, columns=columns, show="headings",selectmode="browse")
    loanTree.grid(column=0, row=3,padx=20,pady=10, sticky="w")
    for colm in columns:
        loanTree.heading(colm, text=colm)
    loanTree.bind("<<TreeviewSelect>>",get_selected_loan)
    #========================================================
    def show_all_loans():
        loanTree.delete(*loanTree.get_children())
        borrowedBooks=backend.view_all_loans()
        for books in borrowedBooks:
            loanTree.insert('', 'end',iid=books[1], values=books[2:])
    show_all_loans()


# ================================================== frames ==================================================
buttonsFrame = Frame(window)
buttonsFrame.grid(column=0, row=3, columnspan=4, padx=5)

treeFrame = Frame(window)
treeFrame.grid(row=4, column=0, columnspan=6, padx=10, pady=10, sticky="nsew")
# ================================================== labels ==================================================
titleLabel = Label(window, text="Title")
titleLabel.grid(column=0, row=0, padx=10, pady=10, sticky="ew")

authorLabel = Label(window, text="Author")
authorLabel.grid(column=0, row=1)

YearLabel = Label(window, text="Year")
YearLabel.grid(column=2, row=0, padx=10, pady=10, sticky="ew")

categoryLabel = Label(window, text="Category")
categoryLabel.grid(column=2, row=1, padx=10, pady=10, sticky="ew")

searchByLabel = Label(window, text="Search By:")
searchByLabel.grid(column=0, row=2, padx=10, pady=10, sticky="ew")

searchLabel = Label(window, text="Search")
searchLabel.grid(column=2, row=2, padx=10, pady=10, sticky="ew")

# #================================================== entries ==================================================
titleText = StringVar()
titleEntry = Entry(window, textvariable=titleText, width=35)
titleEntry.grid(column=1, row=0, padx=10, pady=10, sticky="ew")

authorText = StringVar()
authorEntry = Entry(window, textvariable=authorText, width=35)
authorEntry.grid(column=1, row=1, padx=10, pady=10, sticky="ew")

yearText = StringVar()
yearEntry = Entry(window, textvariable=yearText, width=35)
yearEntry.grid(column=3, row=0, sticky="ew")

searchText = StringVar()
searchEntry = Entry(window, textvariable=searchText, width=35)
searchEntry.grid(column=3, row=2, sticky="ew")

# ==================================================== comboBoxes ================================================
categoryText = StringVar()
categoryCombobox = ttk.Combobox(window, textvariable=categoryText)
categoryCombobox['values'] = ("Fantasy", "Sci-Fi", "History", "Programming", "Psychology", "Romance")
categoryCombobox.grid(column=3, row=1, sticky="ew")

searchByText = StringVar()
searchCombobox = ttk.Combobox(window, textvariable=searchByText)
searchCombobox["values"] = ("Title", "Author", "Year", "Category", "Status")
searchCombobox.grid(column=1, row=2, sticky="ew")

# ================================================== treeview =================================================
columns = ("Title", "Author", "Year", "Category", "Status")
tree = ttk.Treeview(treeFrame, columns=columns, show="headings", selectmode="browse")
for colm in columns:
    tree.heading(colm, text=colm)
tree.pack(side=LEFT, fill="both", expand=True)
tree.column("Title", width=200)

tree.column("Author", width=150)
tree.column("Year", width=80)
tree.column("Category", width=120)
tree.column("Status", width=100)

tree.bind("<<TreeviewSelect>>", get_selected_row)

scrollbar = ttk.Scrollbar(treeFrame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")

# ================================================== buttons ==================================================
searchButton = Button(window, text="Search", width=12, command=search_book)
searchButton.grid(column=4, row=2, padx=5, sticky="w")

addButton = Button(buttonsFrame, text="Add", width=12, command=add)
addButton.grid(column=0, row=0, padx=25)

updateButton = Button(buttonsFrame, text="Update", width=12, command=update_selected_book)
updateButton.grid(column=1, row=0, padx=25)

showAllButton = Button(buttonsFrame, text="Refresh", width=12, command=show_all_books)
showAllButton.grid(column=2, row=0, padx=25)

deleteButton = Button(buttonsFrame, text="Delete", width=12, command=delete_selected_book)
deleteButton.grid(column=3, row=0, padx=25)

loanManagementButton = Button(buttonsFrame, text="Loan Management", width=15, command=open_loan_window)
loanManagementButton.grid(column=4, row=0, padx=25)

show_all_books()


window.mainloop()
