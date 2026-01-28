import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns 

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Load Data

@st.cache_data
def load_data():
    data = pd.read_csv("creditcard.csv")
    return data

df = load_data()

# Dataset Overview

st.subheader("Dataset Overview")
st.write(df.head())
st.write("Shape:", df.shape)

# Class Distribution

st.subheader("Class Distribution")
fig, ax = plt.subplots()
sns.countplot(x="Class", data=df, ax=ax)
ax.set_xticklabels(["Legit", "Fraud"])
st.pyplot(fig)

# Preprocessing

X = df.drop("Class", axis=1)
y = df["Class"]

scaler = StandardScaler()
X[["Amount", "Time"]] = scaler.fit_transform(X[["Amount", "Time"]])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Model Selection

st.sidebar.header("Model Settings")

model_choice = st.sidebar.selectbox(
    "Choose Model",
    ("Logistic Regression", "Decision Tree", "Random Forest")
)

# Train Model

if model_choice == "Logistic Regression":
    model = LogisticRegression(
        class_weight = "balanced", 
        max_iter = 1000
    )

elif model_choice == "Decision Tree":
    model = DecisionTreeClassifier(
        class_weight="balanced",
        max_depth=6,
        random_state=42
    )

else:
    model = RandomForestClassifier(
        n_estimators=100,
        class_weight="balanced",
        random_state=42
    )

model.fit(X_train, y_train)
y_pred = model.predict(X_test)

# Result

st.subheader("Model Performance")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Accuracy", f"{accuracy_score(y_test, y_pred):.4f}")

with col2:
    st.metric("Fraud Recall", f"{classification_report(y_test, y_pred, output_dict=True)["1"]["recall"]:.4f}")

with col3:
    st.metric("Fraud Precision", f"{classification_report(y_test, y_pred, output_dict=True)["1"]["precision"]:.4f}")

# Classification Report

st.subheader("Classification Report")
st.text(classification_report(y_test, y_pred))

# Confusion Matrix

st.subheader("Confusion Matrix")
cm = confusion_matrix(y_test, y_pred)

fig2, ax2 = plt.subplots()
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax2)
ax2.set_xlabel("Predicted")
ax2.set_ylabel("Actual")
st.pyplot(fig2)

# Footer

st.success("Model trained and evaluated successfully!")
