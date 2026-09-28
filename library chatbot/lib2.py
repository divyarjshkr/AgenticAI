
"""
============================================================
        LIBRA - AI COLLEGE LIBRARY AGENT
============================================================

AI-powered college library agent using:
- Python
- Groq API
- openai/gpt-oss-20b
- Function/Tool Calling
- Dictionary-based library data
- .env for API key

Runs completely in the VS Code terminal.

No:
- Student login
- Student ID
- Database
- Website
- GUI
============================================================
"""

import os
import json
from dataclasses import dataclass
from datetime import date, timedelta

from dotenv import load_dotenv

try:
    from groq import Groq
except ImportError:  # pragma: no cover - optional dependency
    Groq = None


# ============================================================
# GROQ SETUP
# ============================================================

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key) if api_key and Groq else None
MODEL = "openai/gpt-oss-20b"


# ============================================================
# LIBRARY DATA
# ============================================================

@dataclass
class Book:
    book_id: int
    title: str
    author: str
    category: str
    total: int
    available: int
    borrowed: int = 0

    def to_summary(self):
        return {
            "book_id": self.book_id,
            "title": self.title,
            "author": self.author,
            "category": self.category,
            "available": self.available,
            "total": self.total,
        }

    def to_detail(self):
        return {
            "book_id": self.book_id,
            "title": self.title,
            "author": self.author,
            "category": self.category,
            "total_copies": self.total,
            "available_copies": self.available,
            "borrowed_copies": self.borrowed,
        }


class Library:
    def __init__(self):
        self.books = {
            1: Book(1, "Python Crash Course", "Eric Matthes", "Programming", 5, 5),
            2: Book(2, "Clean Code", "Robert C. Martin", "Programming", 4, 4),
            3: Book(3, "Computer Networks", "Andrew S. Tanenbaum", "Networking", 4, 4),
            4: Book(4, "Database System Concepts", "Abraham Silberschatz", "Database", 3, 3),
            5: Book(5, "Operating System Concepts", "Abraham Silberschatz", "Operating Systems", 4, 4),
            6: Book(6, "Introduction to Algorithms", "Thomas H. Cormen", "Algorithms", 3, 3),
            7: Book(7, "Java: The Complete Reference", "Herbert Schildt", "Programming", 5, 5),
            8: Book(8, "Artificial Intelligence: A Modern Approach", "Stuart Russell", "AI", 3, 3),
            9: Book(9, "Computer Organization and Design", "David A. Patterson", "Computer Science", 3, 3),
            10: Book(10, "The Pragmatic Programmer", "Andrew Hunt", "Software", 4, 4),
        }
        self.borrowed_books = {}

    def list_all_books(self):
        return [book.to_summary() for book in self.books.values()]

    def search_books(self, query):
        query = query.lower().strip()
        if not query:
            return []

        results = []
        for book in self.books.values():
            haystack = " ".join([
                book.title,
                book.author,
                book.category,
            ]).lower()
            if query in haystack:
                results.append(book.to_summary())
        return results

    def get_book_details(self, book_id):
        if book_id not in self.books:
            return {"success": False, "message": "Book ID does not exist."}

        return {"success": True, **self.books[book_id].to_detail()}

    def check_availability(self, book_id):
        if book_id not in self.books:
            return {"success": False, "message": "Book ID does not exist."}

        book = self.books[book_id]
        return {
            "success": True,
            "title": book.title,
            "available_copies": book.available,
            "total_copies": book.total,
            "status": "Available" if book.available > 0 else "Not Available",
        }

    def borrow_book(self, book_id):
        if book_id not in self.books:
            return {"success": False, "message": "Book ID does not exist."}

        book = self.books[book_id]

        if book.available <= 0:
            return {"success": False, "message": f'"{book.title}" is currently unavailable.'}

        if book_id in self.borrowed_books:
            return {"success": False, "message": f'"{book.title}" is already checked out.'}

        if len(self.borrowed_books) >= 3:
            return {"success": False, "message": "The maximum borrowing limit of 3 books has been reached."}

        borrow_date = date.today()
        due_date = borrow_date + timedelta(days=14)

        book.available -= 1
        book.borrowed += 1
        self.borrowed_books[book_id] = {
            "borrow_date": str(borrow_date),
            "due_date": str(due_date),
        }

        return {
            "success": True,
            "title": book.title,
            "borrow_date": str(borrow_date),
            "due_date": str(due_date),
            "message": f'"{book.title}" has been checked out successfully.',
        }

    def return_book(self, book_id):
        if book_id not in self.borrowed_books:
            return {"success": False, "message": "This book is not currently checked out."}

        book = self.books[book_id]
        book.available += 1
        book.borrowed -= 1
        del self.borrowed_books[book_id]

        return {"success": True, "title": book.title, "message": f'"{book.title}" has been returned successfully.'}

    def get_borrowed_books(self):
        if not self.borrowed_books:
            return {"message": "No books are currently checked out."}

        books = []
        for book_id, record in self.borrowed_books.items():
            book = self.books[book_id]
            books.append({
                "book_id": book_id,
                "title": book.title,
                "author": book.author,
                "borrow_date": record["borrow_date"],
                "due_date": record["due_date"],
            })
        return books

    def get_library_statistics(self):
        total_titles = len(self.books)
        total_copies = sum(book.total for book in self.books.values())
        available_copies = sum(book.available for book in self.books.values())
        borrowed_copies = sum(book.borrowed for book in self.books.values())

        return {
            "total_book_titles": total_titles,
            "total_physical_copies": total_copies,
            "available_copies": available_copies,
            "currently_borrowed": borrowed_copies,
        }

    def get_library_information(self):
        return {
            "opening_hours": {
                "Monday-Friday": "9:00 AM - 5:00 PM",
                "Saturday": "9:00 AM - 1:00 PM",
                "Sunday": "Closed",
            },
            "rules": [
                "Maximum 3 books can be checked out.",
                "Borrowing period is 14 days.",
                "Book availability updates automatically.",
                "No student login is required.",
            ],
        }


library = Library()


# ============================================================
# LIBRARY FUNCTIONS / TOOLS
# ============================================================

def list_all_books():
    """Return all books in the library."""
    return library.list_all_books()


def search_books(query):
    """Search books by title, author, category, or topic."""
    return library.search_books(query)


def get_book_details(book_id):
    """Get complete information about a book."""
    return library.get_book_details(book_id)


def check_availability(book_id):
    """Check availability of a book."""
    return library.check_availability(book_id)


def borrow_book(book_id):
    """Borrow a book."""
    return library.borrow_book(book_id)


def return_book(book_id):
    """Return a borrowed book."""
    return library.return_book(book_id)


def get_borrowed_books():
    """Show currently borrowed books."""
    return library.get_borrowed_books()


def get_library_statistics():
    """Return library statistics."""
    return library.get_library_statistics()


def get_library_information():
    """Return library rules and opening hours."""
    return library.get_library_information()


# ============================================================
# GROQ TOOL DEFINITIONS
# ============================================================

tools = [

    {
        "type": "function",
        "function": {
            "name": "list_all_books",

            "description": (
                "List all books in the college library "
                "with their availability."
            ),

            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "search_books",

            "description": (
                "Search the library by title, author, "
                "category, subject, or topic."
            ),

            "parameters": {
                "type": "object",

                "properties": {
                    "query": {
                        "type": "string",
                        "description": (
                            "The title, author, category, "
                            "subject, or topic to search for."
                        )
                    }
                },

                "required": ["query"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "get_book_details",

            "description": (
                "Get detailed information about a specific "
                "book using its book ID."
            ),

            "parameters": {
                "type": "object",

                "properties": {
                    "book_id": {
                        "type": "integer",
                        "description": "The ID of the book."
                    }
                },

                "required": ["book_id"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "check_availability",

            "description": (
                "Check the number of available copies "
                "of a specific book."
            ),

            "parameters": {
                "type": "object",

                "properties": {
                    "book_id": {
                        "type": "integer",
                        "description": "The ID of the book."
                    }
                },

                "required": ["book_id"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "borrow_book",

            "description": (
                "Borrow or check out a library book. "
                "The book must be available and the user "
                "cannot have more than 3 books checked out."
            ),

            "parameters": {
                "type": "object",

                "properties": {
                    "book_id": {
                        "type": "integer",
                        "description": "The ID of the book."
                    }
                },

                "required": ["book_id"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "return_book",

            "description": (
                "Return a book that is currently checked out."
            ),

            "parameters": {
                "type": "object",

                "properties": {
                    "book_id": {
                        "type": "integer",
                        "description": "The ID of the book."
                    }
                },

                "required": ["book_id"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "get_borrowed_books",

            "description": (
                "Show all books that are currently checked out."
            ),

            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "get_library_statistics",

            "description": (
                "Get library statistics including total titles, "
                "total copies, available copies, and borrowed copies."
            ),

            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "get_library_information",

            "description": (
                "Get library opening hours and borrowing rules."
            ),

            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }
]


# ============================================================
# TOOL EXECUTION
# ============================================================

def execute_tool(tool_name, arguments):

    if tool_name == "list_all_books":
        return list_all_books()

    elif tool_name == "search_books":
        return search_books(arguments["query"])

    elif tool_name == "get_book_details":
        return get_book_details(arguments["book_id"])

    elif tool_name == "check_availability":
        return check_availability(arguments["book_id"])

    elif tool_name == "borrow_book":
        return borrow_book(arguments["book_id"])

    elif tool_name == "return_book":
        return return_book(arguments["book_id"])

    elif tool_name == "get_borrowed_books":
        return get_borrowed_books()

    elif tool_name == "get_library_statistics":
        return get_library_statistics()

    elif tool_name == "get_library_information":
        return get_library_information()

    else:
        return {
            "success": False,
            "message": "Unknown tool requested."
        }


# ============================================================
# AI AGENT INSTRUCTIONS
# ============================================================

SYSTEM_PROMPT = """
You are Libra, a friendly AI college library assistant.

Your main job is to help users interact with the college library.

The library contains exactly 10 books.

You have access to library tools that contain the real
library data. Always use the tools for library information.

RULES:

1. Use library tools when the user asks about:
   - books
   - authors
   - categories
   - availability
   - borrowing
   - returning
   - borrowed books
   - library statistics
   - library opening hours
   - library rules

2. Never invent a book.

3. Never invent availability numbers.

4. If the user gives a book title instead of a book ID,
   use search_books first to find the correct book.

5. Search can be performed using:
   - title
   - author
   - category
   - subject
   - topic

6. If the user asks to borrow a book, use the borrow_book
   tool after identifying the correct book.

7. If the user asks to return a book, use the return_book tool.

8. There is no student login.

9. There is no student ID.

10. A maximum of 3 books can be borrowed at one time.

11. The borrowing period is 14 days.

12. Be conversational and friendly.

13. Do not force the user to choose numbered menu options.

14. The user should be able to communicate naturally.

15. If a request is unclear, ask a short clarification question.

16. You can perform multiple tool calls when necessary.

17. When showing book information, keep the response simple
    and easy to understand.

18. When a tool returns an error or unavailable result,
    clearly explain the actual result to the user.

EXAMPLE:

User:
"Do you have any programming books?"

Use the search_books tool with:
"programming"

Then explain the matching books.

EXAMPLE:

User:
"Borrow Clean Code."

First search for "Clean Code" if the book ID is not already known.

Then use borrow_book with the correct book ID.

Then tell the user whether the borrowing was successful.

You are an AI agent because you decide which tools
are needed to accomplish the user's request.
"""


# ============================================================
# MAIN AI AGENT
# ============================================================

def run_agent():

    print("\n" + "=" * 70)
    print("              📚 LIBRA - AI COLLEGE LIBRARY")
    print("=" * 70)

    print("\nHello! 👋")
    print("I'm Libra, your AI college library assistant.")
    print("You can talk to me naturally.")

    print("\nTry asking things like:")
    print('  "What programming books do you have?"')
    print('  "Is Clean Code available?"')
    print('  "Tell me about Python Crash Course."')
    print('  "Borrow Clean Code."')
    print('  "Return Clean Code."')
    print('  "What books am I currently borrowing?"')
    print('  "How many books are available?"')
    print('  "What are the library timings?"')

    print("\nType 'quit' or 'exit' to leave.")

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    while True:

        try:

            user_input = input("\nYou: ").strip()

        except (KeyboardInterrupt, EOFError):

            print("\n\nLibra: Goodbye! 📚")
            break

        if not user_input:
            continue

        if user_input.lower() in ["quit", "exit", "bye"]:

            print("\nLibra: Goodbye! Keep reading! 📚")
            break

        messages.append({
            "role": "user",
            "content": user_input
        })

        try:

            while True:

                response = client.chat.completions.create(

                    model=MODEL,

                    messages=messages,

                    tools=tools,

                    tool_choice="auto",

                    temperature=0.2
                )

                assistant_message = response.choices[0].message

                # ------------------------------------------------
                # AI WANTS TO USE A TOOL
                # ------------------------------------------------

                if assistant_message.tool_calls:

                    messages.append(assistant_message)

                    for tool_call in assistant_message.tool_calls:

                        tool_name = tool_call.function.name

                        try:

                            arguments = json.loads(
                                tool_call.function.arguments
                            )

                        except json.JSONDecodeError:

                            arguments = {}

                        result = execute_tool(
                            tool_name,
                            arguments
                        )

                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": json.dumps(result)
                        })

                    # Send tool results back to the AI
                    continue

                # ------------------------------------------------
                # AI FINAL RESPONSE
                # ------------------------------------------------

                assistant_reply = assistant_message.content

                messages.append({
                    "role": "assistant",
                    "content": assistant_reply
                })

                print("\nLibra:\n")
                print(assistant_reply)

                break

        except Exception as error:

            print("\n❌ Something went wrong.")
            print("Error:", error)

            # Remove failed user message
            if messages and messages[-1]["role"] == "user":
                messages.pop()


# ============================================================
# START PROGRAM
# ============================================================

if __name__ == "__main__":
    run_agent()

