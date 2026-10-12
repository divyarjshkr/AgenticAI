with open("studymaterials.txt", "r") as file:

    study_material = file.read()


while True:

    print("\nStudyBuddy")
    print("1. Study")
    print("2. Quiz")
    print("3. Quit")

    choice = input("Choose an option: ")

    if choice == "1":

        print("\nPhotosynthesis - Key Points")

        print("• Plants use sunlight to make their own food.")
        print("• The main inputs are sunlight, carbon dioxide, and water.")
        print("• Chlorophyll absorbs light energy.")
        print("• Photosynthesis mainly takes place in the leaves.")
        print("• Glucose is produced and stores chemical energy.")
        print("• Oxygen is produced as a byproduct.")
        print("• Plants release oxygen into the atmosphere.")
        print("• Photosynthesis supports plant growth and food chains.")


    elif choice == "2":

        score = 0

        print("\nStarting Photosynthesis Quiz!\n")


        # Question 1
        print("1. What is the main purpose of photosynthesis?")
        print("A. To produce oxygen only")
        print("B. To make food using light energy")
        print("C. To absorb water from the soil")
        print("D. To release carbon dioxide")

        answer = input("Your answer: ").lower()

        if answer == "b":

            print("Correct!")
            score += 1

        else:

            print("Good try! The correct answer is B.")


        # Question 2
        print("\n2. Which pigment is important for photosynthesis?")
        print("A. Chlorophyll")
        print("B. Glucose")
        print("C. Carbon dioxide")
        print("D. Oxygen")

        answer = input("Your answer: ").lower()

        if answer == "a":

            print("Correct!")
            score += 1

        else:

            print("Good try! The correct answer is A.")


        # Question 3
        print("\n3. Where does most photosynthesis take place?")
        print("A. Roots")
        print("B. Flowers")
        print("C. Leaves")
        print("D. Seeds")

        answer = input("Your answer: ").lower()

        if answer == "c":

            print("Correct!")
            score += 1

        else:

            print("Good try! The correct answer is C.")


        # Question 4
        print("\n4. Which of these is an input needed for photosynthesis?")
        print("A. Oxygen")
        print("B. Glucose")
        print("C. Carbon dioxide")
        print("D. Sugar")

        answer = input("Your answer: ").lower()

        if answer == "c":

            print("Correct!")
            score += 1

        else:

            print("Good try! The correct answer is C.")


        # Question 5
        print("\n5. What gas is produced as a byproduct of photosynthesis?")
        print("A. Carbon dioxide")
        print("B. Oxygen")
        print("C. Nitrogen")
        print("D. Hydrogen")

        answer = input("Your answer: ").lower()

        if answer == "b":

            print("Correct!")
            score += 1

        else:
            print("Good try! The correct answer is B.")


        print("\nQuiz complete!")
        print(f"Your score: {score}/5")

    elif choice == "3":

        print("Goodbye!")

        break


    else:

        print("Invalid choice. Please choose 1, 2, or 3.")