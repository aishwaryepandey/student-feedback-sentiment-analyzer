import streamlit as st
from textblob import TextBlob
import pandas as pd
import os
from datetime import datetime
import base64

# ---------- Basic Page Config ----------
st.set_page_config(
    page_title="Student Feedback Sentiment Analyzer",
    page_icon="📊",
    layout="centered"
)

DATA_FILE = "feedback_data.csv"

# ---------- Convert Image to Base64 ----------
def get_base64_of_image(image_path):
    with open(image_path, "rb") as file:
        data = file.read()
    return base64.b64encode(data).decode()

# ---------- Set Global Background Image ----------
def set_background(image_file):
    encoded_image = get_base64_of_image(image_file)
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded_image}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Apply the background
set_background("background.png")


# ---------- Data Handling Functions ----------
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=["Timestamp", "Name", "Course", "Feedback", "Polarity", "Sentiment"])

def save_data(df):
    df.to_csv(DATA_FILE, index=False)


# ---------- Sentiment Analysis Function ----------
def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity

    if polarity > 0.13:
        sentiment = "Positive"
    elif polarity < -0.15:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    return polarity, sentiment


# ---------- Main App ----------
def main():

    if "page" not in st.session_state:
        st.session_state["page"] = "Home"

    st.title("🎓 Student Feedback Sentiment Analyzer")
    st.write("**Mini Project - Sentiment Analysis of Student Feedback Using NLP**")
    st.write("**Name** - Aishwarye Pandey")
    st.write("**Roll Number** - 2301920100028")
    st.write("**Class** - CSE-3F")

    # ---------- Sidebar ----------
    with st.sidebar:
        st.markdown(
            """
            <h2 style="font-size: 26px; font-weight: 800; margin-bottom: 10px;">
                Navigation
            </h2>
            """,
            unsafe_allow_html=True
        )

        if st.button("🏠 Home"):
            st.session_state["page"] = "Home"

        if st.button("📝 Analyze Feedback"):
            st.session_state["page"] = "Analyze Feedback"

        if st.button("📊 View All Feedback"):
            st.session_state["page"] = "View All Feedback"

    page = st.session_state["page"]
    df = load_data()


    # ==================================================================
    #                       HOME PAGE
    # ==================================================================
    if page == "Home":
        st.markdown("---")
        st.subheader("📌 Project Overview")

        st.markdown("""
        The **Student Feedback Sentiment Analyzer** is a web-based mini-project developed using Python and NLP.  
        It reads **text feedback** given by students about a subject, course or teacher and automatically
        classifies it as **Positive**, **Neutral** or **Negative** based on the sentiment expressed in the text.
        """)

        st.markdown("### 🎯 Main Idea of the Project")
        st.markdown("""
        - Students usually give feedback in the form of **sentences or paragraphs** like  
          _"The teacher explains very well"_ or _"The workload is too high"_.  
        - Manually reading each feedback is **time-consuming** and **difficult** when there are many students.  
        - This project uses **Natural Language Processing (NLP)** to:
          - Read the feedback text  
          - Calculate a **polarity score** (between -1 and +1)  
          - Convert that score into **Positive, Neutral or Negative sentiment**  
        - This helps teachers and administrators quickly understand the **overall mood** of students.
        """)

        st.markdown("### 🤖 What is Sentiment Analysis?")
        st.markdown("""
        - **Sentiment Analysis** is a subfield of NLP that focuses on identifying the **emotion or opinion** behind text.  
        - It is commonly used in:
          - ⭐ Product reviews (Amazon, Flipkart)  
          - 💬 Social media comments (Twitter, Instagram)  
          - 🎥 Movie and app reviews  
        - In this project, sentiment analysis is applied on **student feedback** instead of product or movie reviews.
        """)

        st.markdown("### 📌 Why Use Sentiment Analysis for Student Feedback?")
        st.markdown("""
        - Manually checking each feedback form is **slow and inefficient**.  
        - Important comments might be **missed** if there are too many responses.  
        - With sentiment analysis:
          - ⏱️ Faculty can quickly get a **summary of student opinions**.  
          - 🎯 It becomes easy to identify **problem areas** like workload, clarity of teaching, pace, etc.  
          - 📈 It supports **data-driven decision-making** for improving teaching and curriculum.  
          - 🤝 Overall, it makes the feedback process more **objective, consistent and meaningful**.
        """)

        st.markdown("### 🧩 Features of the Application")
        st.markdown("""
        - 🌐 **Web Interface using Streamlit** – simple and easy to use.  
        - 📝 Input form to collect:
          - Student Name  
          - Course / Subject  
          - Textual Feedback  
        - 🤖 **Automatic Sentiment Detection** using TextBlob (NLP).  
        - 📈 Calculation of **polarity score** between -1 and +1.  
        - 🏷️ Classification of each feedback as **Positive**, **Neutral** or **Negative** based on polarity.  
        - 💾 Storage of all feedback in a **CSV file** (`feedback_data.csv`) using Pandas.  
        - 📊 Separate page to **view all feedback entries** and **sentiment summary**.  
        - 📥 Option to **download all data as CSV** for further analysis or reporting.
        """)

        st.markdown("### 📖 How to Use the Application (Step-by-Step)")
        st.markdown("""
        1️⃣ Open the **Analyze Feedback** page from the navigation sidebar.  
        2️⃣ Enter the following details:  
           - Student Name (optional)  
           - Course / Subject  
           - Feedback text in English  
        3️⃣ Click on the **Analyze Sentiment** button.  
        4️⃣ The system will:
           - Compute the **polarity score** using TextBlob  
           - Display the **detected sentiment** (Positive / Neutral / Negative) with a colored box  
           - Save the feedback into the CSV file along with timestamp and sentiment  
        5️⃣ To view all feedback, open the **View All Feedback** page:
           - See the complete **table of feedback**  
           - Check **sentiment counts** (how many positive, neutral, negative)  
           - Download the data as a CSV file.
        """)

        st.markdown("### ⚙️ Technologies Used")
        st.markdown("""
        - 💻 **Programming Language:** Python  
        - 🌐 **Framework:** Streamlit (for building the web-based user interface)  
        - 🧠 **NLP Library:** TextBlob (for sentiment analysis and polarity calculation)  
        - 📊 **Data Handling:** Pandas  
        - 💾 **Storage:** CSV file (`feedback_data.csv`)  
        - 🖼️ **UI Enhancement:** Custom background image using Base64 and CSS
        """)

        st.markdown("---")
        st.markdown("## 📌 Example: How It Works")

        example_feedbacks = [
            ("The teacher explains everything extremely well and I love this class!", "Expected: Positive"),
            ("The lectures are extremely confusing and badly structured.", "Expected: Negative"),
            ("The teaching style is acceptable. It meets expectations but doesn’t exceed them.", "Expected: Neutral"),
        ]

        st.markdown("Below are some example feedbacks and how the system classifies them:")

        for fb, expected in example_feedbacks:
            polarity, sentiment = analyze_sentiment(fb)
            emoji = "🟢" if sentiment == "Positive" else "🔴" if sentiment == "Negative" else "🟡"

            st.markdown(f"""
            ### 💬 Feedback:
            > _{fb}_  

            **{expected}**

            **Polarity:** `{polarity:.3f}`  
            **Detected Sentiment:** {emoji} **{sentiment}**

            ---
            """)

        st.markdown("These examples show how the application converts normal sentences into **numeric polarity** and then into **sentiment labels**.")

        st.markdown("---")
        if st.button("Start Analyzing Feedback →"):
            st.session_state["page"] = "Analyze Feedback"
            st.rerun()


    # ==================================================================
    #                    ANALYZE FEEDBACK PAGE
    # ==================================================================
    elif page == "Analyze Feedback":
        st.header("📝 Analyze New Feedback")

        name = st.text_input("Student Name")
        course = st.text_input("Course / Subject")
        feedback = st.text_area("Enter Feedback")

        if st.button("Analyze Sentiment"):
            if feedback.strip() == "":
                st.warning("Please enter feedback text.")
            else:
                polarity, sentiment = analyze_sentiment(feedback)

                # Color-coded sentiment box
                color = "#0f9d58" if sentiment == "Positive" else "#d93025" if sentiment == "Negative" else "#f2c744"

                st.markdown(
                    f"""
                    <div style="
                        background-color:{color};
                        padding:15px;
                        border-radius:10px;
                        font-size:18px;
                        color:white;
                        font-weight:bold;
                        text-align:center;">
                        Sentiment: {sentiment}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                # Polarity
                st.info(f"Polarity Score: {polarity:.3f}")

                # Save
                new_row = {
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Name": name if name else "NA",
                    "Course": course if course else "NA",
                    "Feedback": feedback,
                    "Polarity": polarity,
                    "Sentiment": sentiment
                }

                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                save_data(df)

                st.success("Feedback saved successfully!")


    # ==================================================================
    #                    VIEW ALL FEEDBACK PAGE
    # ==================================================================
    elif page == "View All Feedback":
        st.header("📊 Stored Feedback")

        if df.empty:
            st.info("No feedback available yet.")
        else:
            st.dataframe(df)

            st.subheader("📈 Sentiment Summary")
            st.write(df["Sentiment"].value_counts())

            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "Download CSV",
                csv,
                "feedback_data.csv",
                "text/csv"
            )


# ---------- Run App ----------
if __name__ == "__main__":
    main()
