import streamlit as st
import requests

def get_lesson(subject, question, user_type="learner"):
    """Fetches the generated lesson and exercises from the Django backend."""
    url = "http://127.0.0.1:8000/tutor/"  # backend url
    data = {"subject": subject, "question": question, "user_type": user_type}

    response = requests.post(url, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        return f"Error: {response.text}"

def display_exercise(exercise):
    """Displays an exercise and handles user input."""
    if "choices" in exercise:
        # Multiple-choice exercise
        st.write(exercise["question"])
        selected_option = st.radio("Select your answer:", exercise["choices"])
        # Add logic to check if selected_option is correct (requires backend support)
        st.write("Your answer:", selected_option)
        # Add logic to send user answer to backend for evaluation
    else:
        # Other exercise types (e.g., fill-in-the-blank, short answer)
        st.write(exercise["question"])
        user_answer = st.text_input("Your answer:")
        # Add logic to check user_answer against correct answer (requires backend support)
        # Send user answer to backend for evaluation

st.title("SmartFriend Tutor")

# Streamlit UI elements to get subject and question
subject = st.text_input("Enter Subject:")
question = st.text_input("Enter Question:")

user_type = st.radio("User Type:", ("Learner", "Teacher"))

if st.button("Generate Lesson"):
    lesson_data = get_lesson(subject, question, user_type)
    if isinstance(lesson_data, str) and lesson_data.startswith("Error"):
        st.error(lesson_data)
    else:
        with st.spinner("Generating Lesson..."):
            lesson = lesson_data['lesson']
            st.write(lesson)#generate the otput stream


