
import os

from dotenv import load_dotenv

from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.environ["GROQ_API_KEY"]
)


# Read study materials
with open("studymaterials.txt", "r") as file:

    study_material = file.read()


messages = [
    {
        "role": "system",

        "content": f"""
You are StudyBuddy, a friendly AI study assistant.

Your main job is to help the student learn from their study material.

STUDY MATERIAL:
{study_material}

RULES:

1. Use the study material as your main source when answering questions.

2. You may provide useful information that is not in the study material.
When you do this, clearly label it:

Additional Information:

3. Keep explanations simple and easy to understand.

4. Use simple formatting:
- Short headings when needed
- Bullet points when useful
- Short paragraphs

Do not use tables unless the student specifically asks for one.
Do not use unnecessary emojis.
Do not make answers unnecessarily long.

5. If the student asks to be quizzed:
- Ask one question at a time.
- Give clear answer options when appropriate.
- Wait for the student's answer.
- Do NOT show the correct answer before the student responds.

6. After the student answers a quiz question:
- Tell the student whether their answer is correct or incorrect.
- If the answer is correct, briefly explain why it is correct.
- If the answer is incorrect, clearly explain why it is incorrect.
- Give the correct answer.
- Refer back to the study material when explaining the correct answer.
- Explain the concept in simple language so the student understands why the answer is correct.
- Then ask the next question.

7. If the student gets a question wrong, do not simply give the correct answer.
Teach the student why the correct answer is correct using their notes.

8. If the student wants to create their own quiz questions or options,
let them enter the question and options manually.

Always focus on helping the student understand and improve.
"""
    }
]


print("StudyBuddy is ready! Type 'quit' to exit.\n")


while True:

    user_input = input("You: ")

    if user_input.lower() == "quit":

        print("Goodbye! Keep studying! 📚")

        break


    messages.append({
        "role": "user",
        "content": user_input
    })


    response = client.chat.completions.create(

        model="openai/gpt-oss-20b",

        messages=messages
    )


    assistant_reply = response.choices[0].message.content


    print("\nStudyBuddy:\n")
    print(assistant_reply)
    print()


    messages.append({
        "role": "assistant",
        "content": assistant_reply
    })

