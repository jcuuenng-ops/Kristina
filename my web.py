import streamlit as st
import json
from datetime import datetime
import sys
import os

# ---------------- DATA ----------------
version_float = 1.1

questions = [
    {"q": "When you start your day, how heavy does it feel to begin tasks?",
     "opts": [("Light and easy to start",0),("A little slow to start",1),("Hard to push myself",2),("Very hard, I avoid tasks",3)]},

    {"q": "How often do you make small mistakes in your mind?",
     "opts": [("Almost never",0),("Sometimes",1),("Often",2),("Very often",3)]},

    {"q": "How calm do you feel when unexpected changes happen?",
     "opts": [("Calm and flexible",0),("Mostly okay",1),("I get tense",2),("I panic or shut down",3)]},

    {"q": "How steady is your appetite recently?",
     "opts": [("Normal and steady",0),("Slight changes",1),("Big changes",2),("Very irregular or no appetite",3)]},

    {"q": "How often do you feel mentally tired even after rest?",
     "opts": [("Rarely",0),("Sometimes",1),("Often",2),("Almost always",3)]},

    {"q": "When you think about the future, what is your usual feeling?",
     "opts": [("Hopeful",0),("Mixed feelings",1),("Mostly worried",2),("Mostly hopeless",3)]},

    {"q": "How easy is it for you to enjoy hobbies or entertainment?",
     "opts": [("Very easy",0),("Somewhat easy",1),("Hard lately",2),("I cannot enjoy them",3)]},

    {"q": "How often do you feel rushed even without strict deadlines?",
     "opts": [("Almost never",0),("Sometimes",1),("Often",2),("Very often",3)]},

    {"q": "How do you react to normal daily noise?",
     "opts": [("It doesn’t bother me",0),("A little annoying",1),("Very annoying",2),("It overwhelms me",3)]},

    {"q": "How comfortable are you in social situations these days?",
     "opts": [("Comfortable",0),("A bit shy",1),("Uncomfortable",2),("I avoid them",3)]},

    {"q": "How often do you feel your thoughts are too fast?",
     "opts": [("Rarely",0),("Sometimes",1),("Often",2),("Very often",3)]},

    {"q": "How confident do you feel about handling your responsibilities?",
     "opts": [("Very confident",0),("Quite confident",1),("Not very confident",2),("Not confident at all",3)]},

    {"q": "How often do you feel guilty without a clear reason?",
     "opts": [("Almost never",0),("Sometimes",1),("Often",2),("Very often",3)]},

    {"q": "How stable is your mood across the week?",
     "opts": [("Mostly stable",0),("Small ups and downs",1),("Many mood changes",2),("Very unstable",3)]},

    {"q": "When problems happen, how quickly do you recover emotionally?",
     "opts": [("Quickly",0),("In some time",1),("Slowly",2),("I stay stuck for a long time",3)]},

    {"q": "How often do you delay tasks because you feel pressure?",
     "opts": [("Rarely",0),("Sometimes",1),("Often",2),("Almost always",3)]},

    {"q": "How often do you need reassurance from others to feel okay?",
     "opts": [("Rarely",0),("Sometimes",1),("Often",2),("Very often",3)]},

    {"q": "How often do you feel physically restless?",
     "opts": [("Rarely",0),("Sometimes",1),("Often",2),("Always",3)]},

    {"q": "How easy is it to focus on reading or study for 20–30 minutes?",
     "opts": [("Easy",0),("Mostly okay",1),("Hard",2),("Almost impossible",3)]},

    {"q": "How often do you feel emotionally empty or numb?",
     "opts": [("Almost never",0),("Sometimes",1),("Often",2),("Always",3)]}
]

psych_states = {
    "Very Balanced": (0, 8),
    "Balanced": (9, 16),
    "Mild Strain": (17, 25),
    "Moderate Strain": (26, 34),
    "High Strain": (35, 43),
    "Very High Strain": (44, 52),
    "Critical Strain": (53, 60)
}

# ---------------- HELPERS ----------------
def validate_name(name: str) -> bool:
    return len(name.strip()) > 0 and not any(c.isdigit() for c in name)

def validate_dob(dob: str) -> bool:
    try:
        datetime.strptime(dob, "%Y-%m-%d")
        return True
    except:
        return False

def interpret_score(score: int) -> str:
    for state, (low, high) in psych_states.items():
        if low <= score <= high:
            return state
    return "Unknown"

def save_json(filename: str, data: dict):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

# ---------------- STREAMLIT APP ----------------
st.set_page_config(page_title="Student Psychological Survey")
st.title("📝 Student Psychological Survey")

st.info("Please fill out your details and answer all questions honestly.")

# --- User Info ---
name = st.text_input("Given Name")
surname = st.text_input("Surname")
dob = st.text_input("Date of Birth (YYYY-MM-DD)")
sid = st.text_input("Student ID (digits only)")

# --- Start Survey ---
if st.button("Start Survey"):

    # Validate inputs
    errors = []
    if not validate_name(name):
        errors.append("Invalid given name.")
    if not validate_name(surname):
        errors.append("Invalid surname.")
    if not validate_dob(dob):
        errors.append("Invalid date of birth format. Use YYYY-MM-DD.")
    if not sid.isdigit():
        errors.append("Student ID must be digits only.")

    if errors:
        for e in errors:
            st.error(e)
    else:
        st.success("All inputs are valid. Proceed to answer the questions below.")

        total_score = 0
        answers = []

        for idx, q in enumerate(questions):
            opt_labels = [opt[0] for opt in q["opts"]]
            choice = st.selectbox(f"Q{idx+1}. {q['q']}", opt_labels, key=f"q{idx}")
            score = next(score for label, score in q["opts"] if label == choice)
            total_score += score
            answers.append({
                "question": q["q"],
                "selected_option": choice,
                "score": score
            })

        status = interpret_score(total_score)

        st.markdown(f"## ✅ Your Result: {status}")
        st.markdown(f"**Total Score:** {total_score}")

        # Save results to JSON
        record = {
            "name": name,
            "surname": surname,
            "dob": dob,
            "student_id": sid,
            "total_score": total_score,
            "result": status,
            "answers": answers,
            "version": version_float
        }

        json_filename = f"{sid}_result.json"
        save_json(json_filename, record)

        st.success(f"Your results are saved as {json_filename}")
        st.download_button("Download your result JSON", json.dumps(record, indent=2), file_name=json_filename)
