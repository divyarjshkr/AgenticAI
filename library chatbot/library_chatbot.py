from datetime import date, timedelta

# ============================================================
# COLLEGE LIBRARY CHATBOT
# ============================================================

# -------------------- LIBRARY DATA ---------------------------

library = {
    1: {
        "title": "Python Crash Course",
        "author": "Eric Matthes",
        "category": "Programming",
        "total": 5,
        "available": 5,
        "borrowed": 0
    },
    2: {
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "category": "Programming",
        "total": 4,
        "available": 4,
        "borrowed": 0
    },
    3: {
        "title": "Computer Networks",
        "author": "Andrew S. Tanenbaum",
        "category": "Networking",
        "total": 4,
        "available": 4,
        "borrowed": 0
    },
    4: {
        "title": "Database System Concepts",
        "author": "Abraham Silberschatz",
        "category": "Database",
        "total": 3,
        "available": 3,
        "borrowed": 0
    },
    5: {
        "title": "Operating System Concepts",
        "author": "Abraham Silberschatz",
        "category": "Operating Systems",
        "total": 4,
        "available": 4,
        "borrowed": 0
    },
    6: {
        "title": "Introduction to Algorithms",
        "author": "Thomas H. Cormen",
        "category": "Algorithms",
        "total": 3,
        "available": 3,
        "borrowed": 0
    },
    7: {
        "title": "Java: The Complete Reference",
        "author": "Herbert Schildt",
        "category": "Programming",
        "total": 5,
        "available": 5,
        "borrowed": 0
    },
    8: {
        "title": "Artificial Intelligence: A Modern Approach",
        "author": "Stuart Russell",
        "category": "AI",
        "total": 3,
        "available": 3,
        "borrowed": 0
    },
    9: {
        "title": "Computer Organization and Design",
        "author": "David A. Patterson",
        "category": "Computer Science",
        "total": 3,
        "available": 3,
        "borrowed": 0
    },
    10: {
        "title": "The Pragmatic Programmer",
        "author": "Andrew Hunt",
        "category": "Software",
        "total": 4,
        "available": 4,
        "borrowed": 0
    }
}


# Stores books that are currently checked out
borrowed_books = {}


# -------------------- DISPLAY FUNCTIONS ----------------------

def header(title):
    print("\n" + "=" * 65)
    print(f"{title:^65}")
    print("=" * 65)


def show_books():
    header("AVAILABLE LIBRARY BOOKS")

    print(f"{'ID':<5}{'TITLE':<38}{'AVAILABLE':<12}")
    print("-" * 65)

    for book_id, book in library.items():
        availability = f"{book['available']}/{book['total']}"
        print(f"{book_id:<5}{book['title']:<38}{availability:<12}")

    print("-" * 65)
    print("Available = currently available / total copies")


def search_book():
    header("SEARCH FOR A BOOK")

    search = input("Enter title, author, or category: ").strip().lower()

    found = False

    for book_id, book in library.items():
        if (
            search in book["title"].lower()
            or search in book["author"].lower()
            or search in book["category"].lower()
        ):
            print("\nBook ID :", book_id)
            print("Title   :", book["title"])
            print("Author  :", book["author"])
            print("Category:", book["category"])
            print(
                "Copies  :",
                f"{book['available']} available out of {book['total']}"
            )

            found = True

    if not found:
        print("\n❌ No matching books found.")


def book_details():
    header("BOOK DETAILS")

    show_books()

    try:
        book_id = int(input("\nEnter Book ID: "))

        if book_id not in library:
            print("❌ Invalid Book ID.")
            return

        book = library[book_id]

        print("\n" + "-" * 50)
        print("BOOK DETAILS")
        print("-" * 50)
        print("Book ID       :", book_id)
        print("Title         :", book["title"])
        print("Author        :", book["author"])
        print("Category      :", book["category"])
        print("Total Copies  :", book["total"])
        print("Available     :", book["available"])
        print("Borrowed      :", book["borrowed"])
        print("-" * 50)

    except ValueError:
        print("❌ Please enter a valid number.")


def check_availability():
    header("CHECK BOOK AVAILABILITY")

    show_books()

    try:
        book_id = int(input("\nEnter Book ID: "))

        if book_id not in library:
            print("❌ Invalid Book ID.")
            return

        book = library[book_id]

        print("\nBook:", book["title"])
        print("Total copies:", book["total"])
        print("Available copies:", book["available"])

        if book["available"] > 0:
            print("Status: ✅ AVAILABLE")
        else:
            print("Status: ❌ NOT AVAILABLE")

    except ValueError:
        print("❌ Please enter a valid number.")


# -------------------- BORROW FUNCTION ------------------------

def borrow_book():
    header("BORROW / CHECK OUT A BOOK")

    show_books()

    try:
        book_id = int(input("\nEnter Book ID to borrow: "))

        if book_id not in library:
            print("❌ Invalid Book ID.")
            return

        book = library[book_id]

        if book["available"] <= 0:
            print("\n❌ Sorry, this book is currently unavailable.")
            return

        # Check if this book is already borrowed
        if book_id in borrowed_books:
            print("\n❌ This book is already checked out.")
            print("Please return it before borrowing another copy.")
            return

        # Borrowing limit
        if len(borrowed_books) >= 3:
            print("\n❌ Borrowing limit reached.")
            print("Maximum 3 books can be checked out at one time.")
            return

        # Update library information
        book["available"] -= 1
        book["borrowed"] += 1

        borrow_date = date.today()
        due_date = borrow_date + timedelta(days=14)

        borrowed_books[book_id] = {
            "borrow_date": borrow_date,
            "due_date": due_date
        }

        print("\n✅ Book checked out successfully!")
        print("Book       :", book["title"])
        print("Borrowed on:", borrow_date)
        print("Due date   :", due_date)

    except ValueError:
        print("❌ Please enter a valid Book ID.")


# -------------------- RETURN FUNCTION ------------------------

def return_book():
    header("RETURN A BOOK")

    if not borrowed_books:
        print("No books are currently checked out.")
        return

    print("Currently checked-out books:\n")

    for book_id in borrowed_books:
        book = library[book_id]
        print(f"{book_id}. {book['title']}")

    try:
        book_id = int(input("\nEnter Book ID to return: "))

        if book_id not in borrowed_books:
            print("❌ This book is not currently checked out.")
            return

        book = library[book_id]

        # Update library information
        book["available"] += 1
        book["borrowed"] -= 1

        del borrowed_books[book_id]

        print("\n✅ Book returned successfully!")
        print("Book:", book["title"])
        print("Thank you for returning the book.")

    except ValueError:
        print("❌ Please enter a valid Book ID.")


# -------------------- BORROWED BOOKS -------------------------

def borrowed_book_list():
    header("CURRENTLY BORROWED BOOKS")

    if not borrowed_books:
        print("📚 No books are currently checked out.")
        return

    for book_id, record in borrowed_books.items():
        book = library[book_id]

        print("\nBook ID    :", book_id)
        print("Title      :", book["title"])
        print("Author     :", book["author"])
        print("Borrowed on:", record["borrow_date"])
        print("Due date   :", record["due_date"])
        print("-" * 50)


# -------------------- STATISTICS ------------------------------

def statistics():
    header("LIBRARY STATISTICS")

    total_titles = len(library)

    total_copies = sum(
        book["total"] for book in library.values()
    )

    available_copies = sum(
        book["available"] for book in library.values()
    )

    borrowed_copies = sum(
        book["borrowed"] for book in library.values()
    )

    print("Total book titles      :", total_titles)
    print("Total physical copies  :", total_copies)
    print("Available copies       :", available_copies)
    print("Currently borrowed     :", borrowed_copies)


# -------------------- LIBRARY INFORMATION --------------------

def library_information():
    header("LIBRARY INFORMATION")

    print("📚 College Library")
    print("\nOpening Hours:")
    print("Monday - Friday : 9:00 AM - 5:00 PM")
    print("Saturday        : 9:00 AM - 1:00 PM")
    print("Sunday          : Closed")

    print("\nBorrowing Rules:")
    print("• Maximum 3 books can be checked out.")
    print("• Borrowing period is 14 days.")
    print("• Books must be returned before the due date.")
    print("• Availability is updated automatically.")


# -------------------- MAIN MENU ------------------------------

def show_menu():

    print("\n")
    print("=" * 65)
    print("              📚 COLLEGE LIBRARY CHATBOT")
    print("=" * 65)

    print("1. 📚 View all books")
    print("2. 🔍 Search for a book")
    print("3. 📖 View book details")
    print("4. 📦 Check availability")
    print("5. 📥 Borrow / Check out a book")
    print("6. 📤 Return a book")
    print("7. 📋 View currently borrowed books")
    print("8. 📊 Library statistics")
    print("9. ℹ️  Library information")
    print("0. 🚪 Exit")

    print("=" * 65)


# -------------------- CHATBOT -------------------------------

def chatbot():

    header("WELCOME TO THE COLLEGE LIBRARY CHATBOT")

    print("Hello! 👋")
    print("I can help you find and manage library books.")
    print("No login or student ID is required.")

    while True:

        show_menu()

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            show_books()

        elif choice == "2":
            search_book()

        elif choice == "3":
            book_details()

        elif choice == "4":
            check_availability()

        elif choice == "5":
            borrow_book()

        elif choice == "6":
            return_book()

        elif choice == "7":
            borrowed_book_list()

        elif choice == "8":
            statistics()

        elif choice == "9":
            library_information()

        elif choice == "0":
            print("\n" + "=" * 65)
            print("Thank you for using the College Library Chatbot! 📚")
            print("Goodbye! 👋")
            print("=" * 65)
            break

        else:
            print("\n❌ Invalid option.")
            print("Please choose a number from 0 to 9.")


# -------------------- START PROGRAM --------------------------

if __name__ == "__main__":
    chatbot()