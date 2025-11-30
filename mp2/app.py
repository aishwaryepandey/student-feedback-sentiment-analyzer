import streamlit as st
from textblob import TextBlob
import pandas as pd
import os
from datetime import datetime
import base64
import pathlib   # IMPORTANT for background image path


# ---------- Basic Page Config ----------
st.set_page_config(
    page_title="Student Feedback Sentiment Analyzer",
    page_icon="📊",
    layout="centered"
)

DATA_FILE = "feedback_data.csv"

# Base directory where app.py is located
BASE_DIR = pathlib.Path(__file__).parent


# ---------- Convert Image to Base64 ----------
def get_base64_of_image(image_name: str) -> str:
    image_path = BASE_DIR / image_name  # always next to app.py

    if not image_path.exists():
        st.warning(f"Background image not found: {image_path}")
        return ""

    with open(image_path, "rb") as file:
        data = file.read()

    return base64.b64encode(data).decode()


# ---------- Set Global Background Image ----------
def set_background(image_file: str):
    encoded_image = get_base64_of_image(image_file)

    if not encoded_image:
        return  # avoid errors if file missing

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


# Apply background image
set_background("background.png")


# ---------- Data Handling ----------
def load_data():
    file_path = BASE_DIR / DATA_FILE

    if file_path.exists():
        return pd.read_csv(file_path)
    else:
        return pd.DataFrame(columns=["Timestamp", "Name", "Course", "Feedback", "Polarity", "Sentiment"])


def save_data(df):
    file_path = BASE_DIR / DATA_FILE
    df.to_csv(file_path, index=False)


# ---------- Sentiment Analysis ----------
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

    # ---------- Sidebar Navigation ----------
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

    # --------------------------------------------------------------
    #                          HOME PAGE
    # --------------------------------------------------------------
    if page == "Home":
        st.markdown("---")
        st.subheader("📌 Project Overview")
        st.markdown("""
        The **Student Feedback Sentiment Analyzer** is a web-based mini-project developed using Python and NLP.  
        It reads **text feedback** given by students about a subject, course, or teacher and automatically
        classifies it as **Positive**, **Neutral**, or **Negative** based on the sentiment expressed in the text.
        """)

        st.markdown("### 🎯 Main Idea of the Project")
        st.markdown("""
        - Students give feedback like _"The teaching is great"_ or _"The load is too much"_.  
        - Manually reading each feedback is slow and difficult.  
        - This project uses **NLP** to compute:
          - A **polarity score** (-1 to +1)
          - A **sentiment label** (Positive / Neutral / Negative)
        """)

        st.markdown("### 🤖 What is Sentiment Analysis?")
        st.markdown("""
        Sentiment analysis is an NLP technique used to detect the **emotion** behind a text.  
        It is used in:
        - Product reviews  
        - Social media  
        - Movie reviews  
        Here, it is used for **student feedback**.
        """)

        st.markdown("### 📌 Why Use It?")
        st.markdown("""
        - Manual checking is slow  
        - Important comments may be missed  
        - Helps teachers get **quick insights**  
        - Provides **data-driven decisions**  
        """)

        st.markdown("### 🧩 Features")
        st.markdown("""
        - Web interface using Streamlit  
        - NLP-based sentiment detection  
        - Polarity score calculation  
        - CSV storage  
        - View All Feedback page  
        - Download data option  
        """)

        st.markdown("---")
        st.markdown("## 📌 Example Outputs")

        example_feedbacks = [
            ("The teacher explains very well!", "Expected: Positive"),
            ("The lectures are confusing.", "Expected: Negative"),
            ("The teaching style is acceptable.", "Expected: Neutral"),
        ]

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

        if st.button("Start Analyzing Feedback →"):
            st.session_state["page"] = "Analyze Feedback"
            st.rerun()


    # --------------------------------------------------------------
    #                ANALYZE FEEDBACK PAGE
    # --------------------------------------------------------------
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

                st.info(f"Polarity Score: {polarity:.3f}")

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


    # --------------------------------------------------------------
    #                   VIEW ALL FEEDBACK PAGE
    # --------------------------------------------------------------
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
