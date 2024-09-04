import firebase_admin
from firebase_admin import credentials, firestore
import numpy as np
import tkinter as tk
from tkinter import messagebox

# Initialize Firebase Admin SDK
cred = credentials.Certificate('Your_json')
firebase_admin.initialize_app(cred)

# Function to calculate results and update the GUI
def calculate_results():
    global user_data, user_sums, result  # Declare global to modify these variables

    # Initialize Firestore client
    db = firestore.client()

    # Fetch all user documents
    users_ref = db.collection('users')
    users_docs = users_ref.stream()

    # Dictionary to store user data
    user_data = {}

    # Dictionary to store the count, sum, div, and ratio for each question from q1 to q42
    result = {f'q{i}': {'count': 0, 'sum': 0, 'div': 0, 'ratio': 0} for i in range(1, 43)}

    def sig(x):
        return 2 * (1 + np.exp(5 * x)) / np.exp(5.7 * x)

    # Iterate through each user document
    for user_doc in users_docs:
        user_name = user_doc.id  # Get the document ID (user name)
        user_dict = {}  # Dictionary to store user's quiz data

        # Fetch subcollections (q1, q2, etc.) for each user
        subcollections = user_doc.reference.collections()
        for subcollection in subcollections:
            question_id = subcollection.id  # Get subcollection ID (e.g., 'q1', 'q2')

            # Check if the subcollection ID is within the range q1 to q42
            if question_id in result:
                for doc in subcollection.stream():
                    answer = doc.to_dict()  # Fetch the answer document

                    # Assuming the document contains a single field with the answer
                    answer_value = list(answer.values())[0]  # Extract the answer value
                    user_dict[question_id] = answer_value

                    # Update the count and sum for the current question
                    result[question_id]['count'] += 1
                    result[question_id]['sum'] += answer_value

                if result[question_id]['count'] > 0:
                    result[question_id]['div'] = result[question_id]['sum'] / result[question_id]['count']
                if result[question_id]['div'] > 0:
                    result[question_id]['ratio'] = sig(result[question_id]['div'])

        # Add user's data to the main dictionary
        user_data[user_name] = user_dict

    # Multiply each user's answer by the calculated ratio
    for user, quizzes in user_data.items():
        for question_id, answer_value in quizzes.items():
            if question_id in result:
                quizzes[question_id] *= result[question_id]['ratio']  # Multiply answer by ratio

    # Create a new dictionary to store the sum of all modified question values for each user
    user_sums = {}

    # Calculate the sum for each user
    for user, quizzes in user_data.items():
        total_sum = sum(quizzes.values())  # Sum all values in the user's quiz data
        user_sums[user] = total_sum

    # Sort the users by their total score in descending order and get the top 10
    sorted_users = sorted(user_sums.items(), key=lambda x: x[1], reverse=True)[:10]

    # Update the GUI with the top 10 users
    update_gui(sorted_users)

def update_gui(sorted_users):
    # Clear the text widget
    text_widget.delete(1.0, tk.END)

    # Display the top 10 users in the text widget
    text_widget.insert(tk.END, "Top 10\n", "center")  # Center align
    for i, (user, score) in enumerate(sorted_users, start=1):
        text_widget.insert(tk.END, f"{i}. {user}: {score:.2f}\n", "center")  # Center align

# Set up the main GUI window
root = tk.Tk()
root.title("Top 10")

# Create a button to regenerate results with a sky blue color
generate_button = tk.Button(
    root, text="결산~!", command=calculate_results,
    bg="sky blue", font=("Helvetica", 14, "bold")
)
generate_button.pack(pady=10)  # Add padding around the button

# Create a text widget to display the top 10 users with centered text
text_widget = tk.Text(root, height=15, width=50, font=("Helvetica", 14))
text_widget.tag_configure("center", justify='center')  # Configure tag for center alignment
text_widget.pack()

# Run the initial calculation and display the results
calculate_results()

# Start the GUI event loop
root.mainloop()
