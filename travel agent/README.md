# Mini Autonomous Travel Agent ✈️

## Overview

The Mini Autonomous Travel Agent is a Python-based application that helps users plan trips by understanding their travel requirements, searching for suitable flights and hotels, calculating the estimated trip cost, and requesting user approval before booking.

The agent uses the Groq API and the `openai/gpt-oss-20b` language model to interpret natural-language travel requests. It also uses stored user preferences, predefined search tools, and a re-planning mechanism to find alternative options when the initial choices are unsuitable.

The application runs in the terminal and demonstrates how an AI agent can understand requests, make decisions, use external tools, and request human approval before taking action.

## Main Features

- **Natural-Language Understanding:** Extracts travel details such as origin, destination, travel date, duration, number of travelers, budget, and preferences.
- **User Memory:** Loads stored preferences from a JSON file to help fill in missing travel requirements.
- **Flight Search:** Searches for flights matching the requested route, date, and preferred flight time.
- **Hotel Search:** Finds hotels based on destination, preferred location, and maximum price per night.
- **Automatic Re-planning:** Attempts alternative flight or hotel options when the initial search fails.
- **Budget Management:** Calculates flight and hotel costs and attempts to find a cheaper hotel if the plan exceeds the budget.
- **Human Approval:** Displays the final travel plan and asks the user to approve or reject it.
- **Mock Booking:** Processes a simulated booking only after the user approves the plan.

## How the Agent Works

The application follows these steps:

1. **User Input:** The user describes the trip they want to plan.
2. **Memory Loading:** The agent loads stored preferences from `memory/user_memory.json`.
3. **Request Understanding:** The Groq language model converts the user's request into structured JSON.
4. **Flight Search:** The agent searches for a suitable flight.
5. **Hotel Search:** The agent searches for a suitable hotel.
6. **Re-planning:** If suitable options are unavailable, the agent relaxes selected preferences and tries again.
7. **Cost Calculation:** The agent calculates the total estimated cost of flights and accommodation.
8. **Budget Check:** If the total exceeds the budget, the agent attempts to find a cheaper hotel.
9. **Human Approval:** The user reviews the final plan and chooses whether to proceed.
10. **Booking:** If approved, the agent calls the booking tool to process a mock booking and displays the result.

## Project Structure

The main Python file depends on several supporting modules and data files.

```text
TravelAgent/
├── main.py
├── tools/
│   ├── flight_tool.py
│   ├── hotel_tool.py
│   └── booking_tool.py
├── memory/
│   └── user_memory.json
├── .env
└── README.md
```

**Note:** `main.py` is a suggested name for the main file. Replace it with the actual filename used in your project. The supporting filenames and folders reflect the imports and file paths in the code.

## Technologies Used

- **Python:** Main programming language.
- **Groq API:** Provides access to the language model.
- **openai/gpt-oss-20b:** Used to understand and structure travel requests.
- **python-dotenv:** Loads environment variables from the `.env` file.
- **JSON:** Stores user preferences and represents structured travel requirements.
- **Custom Python Tools:** Handle flight searches, hotel searches, and mock bookings.

## Requirements

- Python 3.x
- A Groq API key
- An internet connection for API access
- A terminal or command prompt
- The required project modules and memory file

## Installation and Setup

### 1. Install dependencies

Run the following command in your terminal:

```bash
pip install groq python-dotenv
```

### 2. Configure the API key

Create a `.env` file in the project root directory:

```text
GROQ_API_KEY=your_groq_api_key_here
```

Replace the placeholder with your actual API key. Do not share your key or commit the `.env` file to a public repository.

### 3. Check the project files

Ensure that the following components are available:
- The main travel agent Python file.
- The flight search tool.
- The hotel search tool.
- The booking tool.
- The user memory JSON file.

The memory file must be located at `memory/user_memory.json`, relative to the main Python file's directory.

### 4. Run the application

Open a terminal in the project directory and run the main Python file.

For example, if the file is named `main.py`:

```bash
python main.py
```

If your main file has a different name, replace `main.py` with that filename.

## Example Usage

When the application starts, it asks:

```text
What trip would you like to plan?
>
```

A user might enter:

```text
I want to travel from Goa to Mumbai with two people
for three days, with a budget of ₹25,000.
```

The agent then extracts the requirements, searches for flights and hotels, calculates the estimated cost, and presents a travel plan for approval.

The user can approve the plan by entering `yes` or reject it by entering `no`.

## Re-planning Mechanism

The agent attempts to adjust its search when the initial results do not satisfy the requested preferences.

### Flight re-planning
- First, it searches using the requested date and preferred flight time.
- If no suitable flight is found, it relaxes the flight-time preference.
- If that fails, it searches other available dates for the same route.

### Hotel re-planning
- First, it searches using the preferred hotel location and price limit.
- If no suitable hotel is found, it increases the nightly price limit by ₹1,500.
- If necessary, it relaxes the hotel-location preference.

### Budget re-planning
If the estimated total exceeds the user's budget, the agent attempts to find a cheaper hotel. If the plan still exceeds the budget, it reports that it could not create a suitable plan within the specified budget.

## Human Approval and Booking

The agent displays the selected flight, hotel, and total estimated cost before asking for approval.

- If the user enters `yes`, the booking tool is called with user approval enabled.
- If the user enters `no`, the booking is cancelled.
- If a suitable plan cannot be created, the booking process does not proceed.

**Important:** The code describes the booking step as a mock booking. It should not be treated as a real flight or hotel reservation.

## Limitations

- Flight and hotel options depend on the data and search logic implemented in the supporting tools.
- User preferences are loaded from a local JSON file.
- The application does not provide a graphical interface or website.
- The booking operation is simulated rather than a confirmed real-world reservation.
- The initial travel date may be unspecified, in which case the agent can search for alternative available dates.

## Future Improvements

- Integrate live flight and hotel booking APIs.
- Add more advanced travel preferences.
- Improve budget optimization across flights and hotels.
- Add multi-city trip planning.
- Save previous trips and booking history.
- Improve error handling and validation of AI-generated JSON.
- Add a graphical user interface.

## Purpose

This project demonstrates AI-agent development, natural-language processing, API integration, tool usage, memory, decision-making, budget calculation, re-planning, and human approval in a practical travel-planning application.

## License

This project is intended for educational purposes.
