import streamlit as st
import pandas as pd

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# App Title

st.set_page_config(page_title="Spam SMS Detector", page_icon="📩")
st.title("📩 Spam SMS Detection App")
st.write("Detect whether an SMS massage is **Spam** or **Legitimate** using Machine Learning.")

@st.cache_data
def load_data():
    df = pd.read_csv("spam_sms.csv")
    df.columns = ["label", "message"]
    df["label"] = df["label"].map({"ham": 0, "spam": 1})
    return df
df = load_data()

@st.cache_resource
def train_model():
    X_train, X_test, y_train, y_test = train_test_split(
        df["message"],
        df["label"],
        test_size=0.2,
        random_state=42,
        stratify=df["label"]
    )

    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(
            stop_words="english",
            ngram_range=(1,2),
            max_features=5000
        )),
        ("model", MultinomialNB())
    ])

    pipeline.fit(X_train, y_train)
    accuracy = accuracy_score(y_test, pipeline.predict(X_test))
    return pipeline, accuracy

model, acc = train_model()

# Slidebar

st.sidebar.header("Model Info")
st.sidebar.write("Model: Navie Bayes + TF-IDF")
st.sidebar.write(f"Accuracy: {acc:.2%}")

# User Input

user_input = st.text_area("Enter SMS message:")

if st.button("Predict"):
    if user_input.strip() == "":
        st.warning("Please enter a message.")
    else:
        prediction = model.predict([user_input])[0]

        if prediction == 1:
            st.error("This message is **SPAM**")
        else:
            st.success("This message is **NOT SPAM**")

# Footer

st.markdown("---")
st.markdown("Built with ❤️ using Streamlit & Machine Learning")

