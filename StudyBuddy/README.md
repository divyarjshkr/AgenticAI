# StudyBuddy 🌱

## Overview

StudyBuddy is a simple Python application that helps students learn about photosynthesis and test their knowledge through a multiple-choice quiz.

The application provides two main features: a study mode that displays key points about photosynthesis and a quiz mode that asks five questions and calculates the user's score.

## Projects

### Project 1
The first version of StudyBuddy allows users to:
- Review important facts about photosynthesis.
- Take a five-question multiple-choice quiz.
- Receive feedback on their answers.
- View their final quiz score.
- Exit the application.

### Project 2
Project 2 contains the same core StudyBuddy features, including study notes, an interactive quiz, score tracking, and an option to quit the program.

## Features

- **Study Mode:** Displays key points about photosynthesis.
- **Quiz Mode:** Presents five multiple-choice questions.
- **Score Tracking:** Awards one point for every correct answer, with a maximum score of 5.
- **Instant Feedback:** Informs users whether their answers are correct and reveals the correct answer when they make a mistake.
- **Interactive Menu:** Allows users to select study mode, quiz mode, or quit.
- **Input Validation:** Displays an error message when an invalid menu option is entered.

## Topics Covered

- The purpose of photosynthesis.
- The role of sunlight and chlorophyll.
- Where photosynthesis mainly takes place.
- The inputs required for photosynthesis.
- Oxygen production during photosynthesis.
- The importance of photosynthesis for plant growth and food chains.

## Requirements

- Python 3.x
- A terminal or command prompt
- A text editor or Python IDE

## Project Structure

```text
StudyBuddy/
├── project1.py
├── project2.py
├── studymaterials.txt
└── README.md
```

**Note:** Both Python files attempt to open `studymaterials.txt` when the program starts. Ensure that this file exists in the same directory as the Python scripts.

## How to Run

1. Install Python 3 if it is not already installed.
2. Place `project1.py`, `project2.py`, and `studymaterials.txt` in the same folder.
3. Open a terminal or command prompt in the project folder.
4. Run either project.

To run Project 1:

```bash
python project1.py
```

To run Project 2:

```bash
python project2.py
```

## How to Use

When the application starts, the following menu appears:

```text
StudyBuddy
1. Study
2. Quiz
3. Quit
```

- Enter `1` to view the photosynthesis study notes.
- Enter `2` to start the five-question quiz.
- Enter `3` to exit the application.

During the quiz, enter the letter corresponding to your chosen answer. At the end, your score will be displayed out of 5.

## Technologies Used

- **Python:** Programming language used to develop the application.
- **File Handling:** Opens and reads the `studymaterials.txt` file.
- **Conditional Statements:** Checks menu choices and quiz answers.
- **Loops:** Keeps the program running until the user chooses to quit.
- **Input and Output:** Uses `input()` and `print()` to interact with users.

## Future Improvements

- Load study notes directly from `studymaterials.txt`.
- Add more study topics and quiz questions.
- Randomize quiz questions.
- Allow users to retry incorrect questions.
- Save quiz scores for future reference.
- Improve the user interface.

## Author

Created as a Python learning project to support studying and self-assessment.

## License

This project is intended for educational purposes.
