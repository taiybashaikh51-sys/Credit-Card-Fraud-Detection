import streamlit as st
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score

# Page Config
st.set_page_config(page_title="Customer Churn Prediction", layout="wide")
st.title("Customer Churn Prediction App")

# Load Dataset
@st.cache_data
def load_data():
    return pd.read_csv("Churn_Modelling.csv")

df = load_data()

st.subheader("Dataset Preview")
st.dataframe(df.head())

# Data Preprocessing

df_model = df.drop(columns=["RowNumber", "CustomerId", "Surname"])

# Encode categorical column
le_geo = LabelEncoder()
le_gender = LabelEncoder()

df_model["Geography"] = le_geo.fit_transform(df_model["Geography"])
df_model["Gender"] = le_gender.fit_transform(df_model["Gender"])

X = df_model.drop("Exited", axis=1)
y = df_model["Exited"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scaling
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Train Models

models = {
    "Logistic Regression": LogisticRegression(),
    "Random Forest": RandomForestClassifier(n_estimators=150, random_state=42),
    "Gradient Boosting": GradientBoostingClassifier(random_state=42)
}   

results = {}

for name, model in models.items():
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    results[name] = accuracy_score(y_test, preds)

# Model Performance

st.subheader("Model Accuracy Comparison")
for model, acc in results.items():
    st.write(f"**{model}** : {acc:.4f}")

best_model_name = max(results, key=results.get)
best_model = models[best_model_name]

st.success(f"Best Model: **{best_model_name}**")

# User Input for Prediction

st.subheader("Predict Churn for New Customer")

col1, col2, col3 = st.columns(3)

with col1:
    credit_score = st.number_input("Credit Score", 300, 900, 600)
    geography = st.selectbox("Geography", le_geo.classes_)
    gender = st.selectbox("Gender", le_gender.classes_)
    age = st.number_input("Age", 18, 100, 35)

with col2:
    tenure = st.slider("Tenure (Years)", 0, 10, 3)
    balance = st.number_input("Balance", 0.0, 300000.0, 50000.0)
    products = st.slider("Number of Products", 1, 4, 1)

with col3:
    credit_card = st.selectbox("Has Credit Card", [0,1])
    active_member = st.selectbox("Is Active Member", [0,1])
    salary = st.number_input("Estimated Salary", 10000.0, 200000.0, 50000.0)

# Encode input

geo_encoded = le_geo.transform([geography])[0]
gender_encoded = le_gender.transform([gender])[0]

input_data = np.array([[credit_score, gender_encoded, gender_encoded, age, tenure, balance, products, credit_card, active_member, salary]])

input_scaled = scaler.transform(input_data)

# Prediction Button

if st.button("Predic Churn"):
    prediction = best_model.predict(input_scaled)[0]
    prob = best_model.predict_proba(input_scaled)[0][1]

    if prediction == 1:
        st.error(f" Customer is likely to churn (Probability: {prob:.2f})")
    else:
        st.success(f"Customer is likely to stay (Probability: {1 - prob:.2f})")
