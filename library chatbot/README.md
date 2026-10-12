# Libra – AI College Library Agent 📚

## Overview

Libra is a Python-based college library assistant designed to help users search for books, check availability, borrow and return books, and access library information.

The project includes a traditional menu-driven library chatbot and an AI-powered library agent. The AI agent uses the Groq API and function calling to understand natural-language requests and execute library operations.

The application runs in the VS Code terminal and does not require student login, a student ID, a database, a website, or a graphical user interface.

## Project Structure

```text
LibraryAgent/
├── lib2.py
├── library_chatbot.py
├── test_library.py
├── .env
└── README.md
```

## Files Description

### 1. `lib2.py`

This file contains the core library management logic used by the AI library agent.

**Main responsibilities:**
- Defines the `Book` data class to represent book information.
- Defines the `Library` class to manage the library collection.
- Stores book information using a dictionary.
- Searches books by title, author, or category.
- Retrieves detailed information about individual books.
- Checks book availability.
- Handles borrowing and returning books.
- Tracks borrowed books, borrowing dates, and due dates.
- Calculates library statistics.
- Provides library opening hours and borrowing rules.

The library contains 10 predefined book titles.

**Borrowing rules:**
- A maximum of 3 books can be borrowed at one time.
- The borrowing period is 14 days.
- A book must be available before it can be borrowed.
- A book cannot be checked out again while it is already checked out.

### 2. `library_chatbot.py`

This file implements a menu-driven college library chatbot.

It provides a text-based interface that allows users to interact with the library system through numbered options.

**Main features:**
- View all library books.
- Search for books by title, author, or category.
- View book details.
- Check book availability.
- Borrow or check out books.
- Return borrowed books.
- View currently borrowed books.
- View library statistics.
- Access library opening hours and borrowing rules.
- Exit the application.

The program uses Python dictionaries to store book details and track borrowing records. It also uses the `datetime` module to calculate borrowing and due dates.

### 3. `test_library.py`

This file contains automated unit tests for the `Library` class defined in `lib2.py`.

It uses Python's built-in `unittest` framework to verify important library operations.

**Tests included:**

- **Book search:** Checks whether searching for "python" returns matching books, with "Python Crash Course" as the first result.
- **Borrowing a book:** Verifies that borrowing book ID `1` updates the available and borrowed copy counts correctly.
- **Returning a book:** Checks whether returning book ID `2` restores its available copies and resets its borrowed count.
- **Borrowing limit:** Verifies that the system prevents a user from borrowing more than three books at a time.

The tests use the `setUp()` method to create a fresh `Library` instance before each test.

## Technologies Used

- **Python 3:** Main programming language.
- **Groq API:** Provides access to the AI model used by the library agent.
- **openai/gpt-oss-20b:** Language model used by the AI agent.
- **Function/Tool Calling:** Allows the AI to select and execute library operations.
- **Python Dataclasses:** Represents individual books in `lib2.py`.
- **Dictionaries:** Store book details and borrowing records.
- **python-dotenv:** Loads the API key from a `.env` file.
- **unittest:** Tests library management functionality.
- **datetime:** Calculates borrowing dates and due dates.

## Requirements

- Python 3.x
- A terminal or command prompt
- Visual Studio Code or another Python IDE
- A Groq API key for the AI-powered agent

## Installation and Setup

### 1. Install the required packages

Open a terminal in the project directory and run:

```bash
pip install groq python-dotenv
```

### 2. Configure the API key

Create a file named `.env` in the project directory and add your Groq API key:

```text
GROQ_API_KEY=your_groq_api_key_here
```

Replace `your_groq_api_key_here` with your actual API key. Do not share or commit your API key to a public repository.

### 3. Run the library chatbot

To start the menu-driven chatbot, run:

```bash
python library_chatbot.py
```

Follow the numbered menu options to perform library operations.

### 4. Run the AI library agent

To start the AI-powered assistant, run:

```bash
python lib2.py
```

You can ask questions in natural language, such as:

- "What programming books do you have?"
- "Is Clean Code available?"
- "Tell me about Python Crash Course."
- "Borrow Clean Code."
- "Return Clean Code."
- "What books am I currently borrowing?"
- "How many books are available?"
- "What are the library timings?"

Type `quit`, `exit`, or `bye` to leave the AI agent.

### 5. Run the unit tests

Execute the following command to run the tests:

```bash
python -m unittest test_library.py
```

The test results indicate whether the library search, borrowing, returning, and borrowing-limit functionality works as expected.

## How the AI Agent Works

1. The user enters a request in natural language.
2. The AI model interprets the request and decides which library tool is needed.
3. The selected tool calls the appropriate library function.
4. The function processes the request using the library's stored data.
5. The tool result is sent back to the AI model.
6. The AI generates a conversational response based on the result.

This process allows users to interact with the library without navigating a numbered menu.

## Library Rules and Opening Hours

| Day | Opening Hours |
|---|---|
| Monday–Friday | 9:00 AM – 5:00 PM |
| Saturday | 9:00 AM – 1:00 PM |
| Sunday | Closed |

- Maximum borrowing limit: 3 books.
- Borrowing period: 14 days.
- Book availability updates automatically when books are borrowed or returned.
- No student login or student ID is required.

## Limitations

- The library contains only 10 predefined book titles.
- Library data is stored in memory using dictionaries and is not connected to a database.
- Borrowing records are not permanently saved between program restarts.
- The AI-powered agent requires a valid Groq API key and an available API service.
- The application runs in the terminal and does not provide a graphical interface or website.

## Future Improvements

- Add more books and categories.
- Integrate a database for persistent storage.
- Save borrowing records between sessions.
- Add overdue-book tracking and reminders.
- Expand the automated test suite.
- Add support for multiple users and individual borrowing records.
- Improve error handling and input validation.

## Purpose

This project demonstrates Python programming, object-oriented design, dictionary-based data management, automated testing, API integration, and AI function calling through a practical college library management application.

## License

This project is intended for educational purposes.
