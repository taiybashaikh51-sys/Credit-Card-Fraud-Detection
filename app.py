<<<<<<< HEAD
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, roc_curve, auc, precision_score, recall_score
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="Credit Card Fraud Detection",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .stApp { background-color: #0B1220; color: #ffffff; }
    .main-header {
        background: linear-gradient(135deg, #1A2333, #0B1220);
        border: 1px solid rgba(239,68,68,0.3);
        border-radius: 16px;
        padding: 2rem;
        margin-bottom: 2rem;
        text-align: center;
    }
    .section-title {
        color: #EF4444;
        font-size: 1.3rem;
        font-weight: 700;
        margin: 1.5rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid rgba(239,68,68,0.3);
    }
    div[data-testid="stSidebar"] {
        background-color: #111827;
        border-right: 1px solid rgba(239,68,68,0.2);
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv('creditcard.csv')
    return df

@st.cache_data
def get_sample(df, n=10000):
    fraud = df[df['Class'] == 1]
    normal = df[df['Class'] == 0].sample(n=min(n, len(df[df['Class']==0])), random_state=42)
    return pd.concat([fraud, normal]).sample(frac=1, random_state=42)

with st.spinner("Loading dataset..."):
    df = load_data()
    sample_df = get_sample(df)

# Sidebar
with st.sidebar:
    st.markdown("### 💳 Fraud Detection")
    st.markdown("---")
    page = st.radio(
        "📊 Select Page",
        ["🏠 Overview", "📈 EDA Analysis", "🤖 ML Models", "🎯 Live Detection", "📋 Data Explorer"]
    )
    st.markdown("---")
    fraud_count = df['Class'].sum()
    fraud_rate = df['Class'].mean() * 100
    st.metric("🚨 Fraud Rate", f"{fraud_rate:.3f}%")
    st.metric("💳 Total Transactions", f"{len(df):,}")

# Header
st.markdown("""
<div class="main-header">
    <h1 style="color:#EF4444; margin:0; font-size:2rem;">💳 Credit Card Fraud Detection</h1>
    <p style="color:#94A3B8; margin:0.5rem 0 0 0;">ML-Powered Real-time Fraud Detection System | Logistic Regression, Decision Tree & Random Forest</p>
</div>
""", unsafe_allow_html=True)

# KPIs
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("💳 Total Transactions", f"{len(df):,}")
with col2:
    st.metric("🚨 Fraud Cases", f"{fraud_count:,}")
with col3:
    normal_count = len(df) - fraud_count
    st.metric("✅ Normal Cases", f"{normal_count:,}")
with col4:
    st.metric("📊 Fraud Rate", f"{fraud_rate:.3f}%")
with col5:
    avg_amount = df['Amount'].mean()
    st.metric("💰 Avg Amount", f"${avg_amount:.2f}")

st.markdown("---")

# OVERVIEW
if page == "🏠 Overview":
    st.markdown('<p class="section-title">📊 Transaction Distribution</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        class_counts = df['Class'].value_counts().reset_index()
        class_counts['Type'] = class_counts['Class'].map({0: 'Normal', 1: 'Fraud'})
        fig = px.pie(class_counts, values='count', names='Type',
            color_discrete_map={'Normal': '#22C55E', 'Fraud': '#EF4444'},
            title='Transaction Class Distribution')
        fig.update_layout(paper_bgcolor='#1A2333', font=dict(color='#94A3B8'))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig2 = px.histogram(df, x='Amount', nbins=50,
            color='Class',
            color_discrete_map={0: '#22C55E', 1: '#EF4444'},
            title='Transaction Amount Distribution',
            barmode='overlay', opacity=0.7)
        fig2.update_layout(paper_bgcolor='#1A2333', plot_bgcolor='#1A2333',
            font=dict(color='#94A3B8'),
            xaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.05)'))
        st.plotly_chart(fig2, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        fraud_df = df[df['Class'] == 1]
        normal_df = df[df['Class'] == 0]
        fig3 = go.Figure()
        fig3.add_trace(go.Box(y=fraud_df['Amount'], name='Fraud',
            marker_color='#EF4444'))
        fig3.add_trace(go.Box(y=normal_df['Amount'].sample(1000), name='Normal',
            marker_color='#22C55E'))
        fig3.update_layout(paper_bgcolor='#1A2333', plot_bgcolor='#1A2333',
            font=dict(color='#94A3B8'), title='Amount by Transaction Type',
            xaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.05)'))
        st.plotly_chart(fig3, use_container_width=True)

    with col2:
        time_fraud = df[df['Class']==1]['Time'].values
        time_normal = df[df['Class']==0]['Time'].sample(500).values
        fig4 = go.Figure()
        fig4.add_trace(go.Histogram(x=time_fraud, name='Fraud',
            marker_color='#EF4444', opacity=0.7))
        fig4.add_trace(go.Histogram(x=time_normal, name='Normal Sample',
            marker_color='#22C55E', opacity=0.7))
        fig4.update_layout(paper_bgcolor='#1A2333', plot_bgcolor='#1A2333',
            font=dict(color='#94A3B8'), title='Fraud vs Normal Over Time',
            barmode='overlay',
            xaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.05)'))
        st.plotly_chart(fig4, use_container_width=True)

# EDA
elif page == "📈 EDA Analysis":
    st.markdown('<p class="section-title">🔬 Feature Analysis</p>', unsafe_allow_html=True)

    feature = st.selectbox("Select Feature", [f'V{i}' for i in range(1, 29)] + ['Amount', 'Time'])

    col1, col2 = st.columns(2)
    with col1:
        fig = go.Figure()
        fig.add_trace(go.Histogram(
            x=df[df['Class']==1][feature],
            name='Fraud', marker_color='#EF4444', opacity=0.7))
        fig.add_trace(go.Histogram(
            x=df[df['Class']==0][feature].sample(2000),
            name='Normal', marker_color='#22C55E', opacity=0.7))
        fig.update_layout(paper_bgcolor='#1A2333', plot_bgcolor='#1A2333',
            font=dict(color='#94A3B8'), barmode='overlay',
            title=f'{feature} Distribution by Class',
            xaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.05)'))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        stats = pd.DataFrame({
            'Fraud': df[df['Class']==1][feature].describe(),
            'Normal': df[df['Class']==0][feature].describe()
        }).round(4)
        st.markdown(f"#### 📊 {feature} Statistics")
        st.dataframe(stats, use_container_width=True)

    st.markdown('<p class="section-title">🔥 Correlation with Fraud</p>', unsafe_allow_html=True)
    corr = df[[f'V{i}' for i in range(1, 15)] + ['Amount', 'Class']].corr()['Class'].drop('Class').sort_values()
    fig2 = px.bar(x=corr.index, y=corr.values,
        color=corr.values, color_continuous_scale='RdYlGn',
        title='Feature Correlation with Fraud')
    fig2.update_layout(paper_bgcolor='#1A2333', plot_bgcolor='#1A2333',
        font=dict(color='#94A3B8'),
        xaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.05)'))
    st.plotly_chart(fig2, use_container_width=True)

# ML MODELS
elif page == "🤖 ML Models":
    st.markdown('<p class="section-title">🤖 Model Training & Evaluation</p>', unsafe_allow_html=True)

    features = [f'V{i}' for i in range(1, 29)] + ['Amount', 'Time']
    X = sample_df[features]
    y = sample_df['Class']

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    model_choice = st.selectbox("🤖 Select Model",
        ["Logistic Regression", "Decision Tree", "Random Forest"])

    with st.spinner(f"Training {model_choice}..."):
        if model_choice == "Logistic Regression":
            model = LogisticRegression(random_state=42, max_iter=1000)
        elif model_choice == "Decision Tree":
            model = DecisionTreeClassifier(random_state=42, max_depth=10)
        else:
            model = RandomForestClassifier(n_estimators=50, random_state=42)

        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        y_prob = model.predict_proba(X_test)[:, 1]

    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("✅ Accuracy", f"{acc*100:.1f}%")
    with col2:
        st.metric("🎯 Precision", f"{prec*100:.1f}%")
    with col3:
        st.metric("📊 Recall", f"{rec*100:.1f}%")
    with col4:
        from sklearn.metrics import f1_score
        f1 = f1_score(y_test, y_pred)
        st.metric("⚡ F1 Score", f"{f1*100:.1f}%")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<p class="section-title">📊 Confusion Matrix</p>', unsafe_allow_html=True)
        cm = confusion_matrix(y_test, y_pred)
        fig = px.imshow(cm, text_auto=True,
            labels=dict(x="Predicted", y="Actual"),
            x=['Normal', 'Fraud'], y=['Normal', 'Fraud'],
            color_continuous_scale='Reds')
        fig.update_layout(paper_bgcolor='#1A2333', font=dict(color='#94A3B8'))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<p class="section-title">📈 ROC Curve</p>', unsafe_allow_html=True)
        fpr, tpr, _ = roc_curve(y_test, y_prob)
        roc_auc = auc(fpr, tpr)
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=fpr, y=tpr,
            name=f'ROC (AUC = {roc_auc:.3f})',
            line=dict(color='#EF4444', width=2)))
        fig2.add_trace(go.Scatter(x=[0,1], y=[0,1],
            line=dict(dash='dash', color='#94A3B8'), name='Random'))
        fig2.update_layout(paper_bgcolor='#1A2333', plot_bgcolor='#1A2333',
            font=dict(color='#94A3B8'),
            xaxis=dict(title='FPR', gridcolor='rgba(255,255,255,0.05)'),
            yaxis=dict(title='TPR', gridcolor='rgba(255,255,255,0.05)'))
        st.plotly_chart(fig2, use_container_width=True)

# LIVE DETECTION
elif page == "🎯 Live Detection":
    st.markdown('<p class="section-title">🎯 Real-time Fraud Detection</p>', unsafe_allow_html=True)

    st.info("💡 Adjust the transaction features below to predict if it's fraudulent!")

    features = [f'V{i}' for i in range(1, 29)] + ['Amount', 'Time']
    X = sample_df[features]
    y = sample_df['Class']
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=50, random_state=42)
    model.fit(X_train, y_train)

    col1, col2 = st.columns(2)
    with col1:
        amount = st.number_input("💰 Transaction Amount ($)", 0.0, 30000.0, 100.0)
        time = st.number_input("⏰ Time (seconds)", 0.0, 200000.0, 50000.0)
        v1 = st.slider("V1", -5.0, 5.0, 0.0)
        v2 = st.slider("V2", -5.0, 5.0, 0.0)
        v3 = st.slider("V3", -5.0, 5.0, 0.0)
        v4 = st.slider("V4", -5.0, 5.0, 0.0)
    with col2:
        v5 = st.slider("V5", -5.0, 5.0, 0.0)
        v6 = st.slider("V6", -5.0, 5.0, 0.0)
        v7 = st.slider("V7", -5.0, 5.0, 0.0)
        v8 = st.slider("V8", -5.0, 5.0, 0.0)
        v9 = st.slider("V9", -5.0, 5.0, 0.0)
        v10 = st.slider("V10", -5.0, 5.0, 0.0)

    input_vals = [v1,v2,v3,v4,v5,v6,v7,v8,v9,v10] + [0.0]*18 + [amount, time]
    input_scaled = scaler.transform([input_vals])
    pred = model.predict(input_scaled)[0]
    prob = model.predict_proba(input_scaled)[0]

    if pred == 1:
        st.markdown(f"""
        <div style="background:#1A2333; border:2px solid #EF4444; border-radius:16px; padding:2rem; text-align:center; margin-top:1rem;">
            <h2 style="color:#EF4444; margin:0;">🚨 FRAUD DETECTED!</h2>
            <p style="color:#94A3B8; margin:0.5rem 0 0 0;">Fraud Probability: <strong style="color:#EF4444">{prob[1]*100:.1f}%</strong></p>
            <p style="color:#94A3B8;">This transaction is flagged as FRAUDULENT!</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="background:#1A2333; border:2px solid #22C55E; border-radius:16px; padding:2rem; text-align:center; margin-top:1rem;">
            <h2 style="color:#22C55E; margin:0;">✅ TRANSACTION SAFE</h2>
            <p style="color:#94A3B8; margin:0.5rem 0 0 0;">Safe Probability: <strong style="color:#22C55E">{prob[0]*100:.1f}%</strong></p>
            <p style="color:#94A3B8;">This transaction appears to be legitimate!</p>
        </div>
        """, unsafe_allow_html=True)

# DATA EXPLORER
elif page == "📋 Data Explorer":
    st.markdown('<p class="section-title">📋 Data Explorer</p>', unsafe_allow_html=True)

    filter_class = st.selectbox("Filter", ['All', 'Fraud Only', 'Normal Only'])
    show_df = df.copy()
    if filter_class == 'Fraud Only':
        show_df = df[df['Class'] == 1]
    elif filter_class == 'Normal Only':
        show_df = df[df['Class'] == 0].head(1000)

    st.dataframe(show_df.head(500), use_container_width=True, height=400)
    csv = show_df.head(1000).to_csv(index=False)
    st.download_button("📥 Download Sample", csv, "fraud_data.csv", "text/csv")

st.markdown("---")
st.markdown("""
<div style="text-align:center; color:#94A3B8; font-size:0.8rem; padding:1rem;">
    💳 Credit Card Fraud Detection | Built by <strong style="color:#EF4444">Taiyba Shaikh</strong> | ML Project
</div>
=======
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, roc_curve, auc, precision_score, recall_score
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="Credit Card Fraud Detection",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .stApp { background-color: #0B1220; color: #ffffff; }
    .main-header {
        background: linear-gradient(135deg, #1A2333, #0B1220);
        border: 1px solid rgba(239,68,68,0.3);
        border-radius: 16px;
        padding: 2rem;
        margin-bottom: 2rem;
        text-align: center;
    }
    .section-title {
        color: #EF4444;
        font-size: 1.3rem;
        font-weight: 700;
        margin: 1.5rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid rgba(239,68,68,0.3);
    }
    div[data-testid="stSidebar"] {
        background-color: #111827;
        border-right: 1px solid rgba(239,68,68,0.2);
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv('creditcard.csv')
    return df

@st.cache_data
def get_sample(df, n=10000):
    fraud = df[df['Class'] == 1]
    normal = df[df['Class'] == 0].sample(n=min(n, len(df[df['Class']==0])), random_state=42)
    return pd.concat([fraud, normal]).sample(frac=1, random_state=42)

with st.spinner("Loading dataset..."):
    df = load_data()
    sample_df = get_sample(df)

# Sidebar
with st.sidebar:
    st.markdown("### 💳 Fraud Detection")
    st.markdown("---")
    page = st.radio(
        "📊 Select Page",
        ["🏠 Overview", "📈 EDA Analysis", "🤖 ML Models", "🎯 Live Detection", "📋 Data Explorer"]
    )
    st.markdown("---")
    fraud_count = df['Class'].sum()
    fraud_rate = df['Class'].mean() * 100
    st.metric("🚨 Fraud Rate", f"{fraud_rate:.3f}%")
    st.metric("💳 Total Transactions", f"{len(df):,}")

# Header
st.markdown("""
<div class="main-header">
    <h1 style="color:#EF4444; margin:0; font-size:2rem;">💳 Credit Card Fraud Detection</h1>
    <p style="color:#94A3B8; margin:0.5rem 0 0 0;">ML-Powered Real-time Fraud Detection System | Logistic Regression, Decision Tree & Random Forest</p>
</div>
""", unsafe_allow_html=True)

# KPIs
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("💳 Total Transactions", f"{len(df):,}")
with col2:
    st.metric("🚨 Fraud Cases", f"{fraud_count:,}")
with col3:
    normal_count = len(df) - fraud_count
    st.metric("✅ Normal Cases", f"{normal_count:,}")
with col4:
    st.metric("📊 Fraud Rate", f"{fraud_rate:.3f}%")
with col5:
    avg_amount = df['Amount'].mean()
    st.metric("💰 Avg Amount", f"${avg_amount:.2f}")

st.markdown("---")

# OVERVIEW
if page == "🏠 Overview":
    st.markdown('<p class="section-title">📊 Transaction Distribution</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        class_counts = df['Class'].value_counts().reset_index()
        class_counts['Type'] = class_counts['Class'].map({0: 'Normal', 1: 'Fraud'})
        fig = px.pie(class_counts, values='count', names='Type',
            color_discrete_map={'Normal': '#22C55E', 'Fraud': '#EF4444'},
            title='Transaction Class Distribution')
        fig.update_layout(paper_bgcolor='#1A2333', font=dict(color='#94A3B8'))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig2 = px.histogram(df, x='Amount', nbins=50,
            color='Class',
            color_discrete_map={0: '#22C55E', 1: '#EF4444'},
            title='Transaction Amount Distribution',
            barmode='overlay', opacity=0.7)
        fig2.update_layout(paper_bgcolor='#1A2333', plot_bgcolor='#1A2333',
            font=dict(color='#94A3B8'),
            xaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.05)'))
        st.plotly_chart(fig2, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        fraud_df = df[df['Class'] == 1]
        normal_df = df[df['Class'] == 0]
        fig3 = go.Figure()
        fig3.add_trace(go.Box(y=fraud_df['Amount'], name='Fraud',
            marker_color='#EF4444'))
        fig3.add_trace(go.Box(y=normal_df['Amount'].sample(1000), name='Normal',
            marker_color='#22C55E'))
        fig3.update_layout(paper_bgcolor='#1A2333', plot_bgcolor='#1A2333',
            font=dict(color='#94A3B8'), title='Amount by Transaction Type',
            xaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.05)'))
        st.plotly_chart(fig3, use_container_width=True)

    with col2:
        time_fraud = df[df['Class']==1]['Time'].values
        time_normal = df[df['Class']==0]['Time'].sample(500).values
        fig4 = go.Figure()
        fig4.add_trace(go.Histogram(x=time_fraud, name='Fraud',
            marker_color='#EF4444', opacity=0.7))
        fig4.add_trace(go.Histogram(x=time_normal, name='Normal Sample',
            marker_color='#22C55E', opacity=0.7))
        fig4.update_layout(paper_bgcolor='#1A2333', plot_bgcolor='#1A2333',
            font=dict(color='#94A3B8'), title='Fraud vs Normal Over Time',
            barmode='overlay',
            xaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.05)'))
        st.plotly_chart(fig4, use_container_width=True)

# EDA
elif page == "📈 EDA Analysis":
    st.markdown('<p class="section-title">🔬 Feature Analysis</p>', unsafe_allow_html=True)

    feature = st.selectbox("Select Feature", [f'V{i}' for i in range(1, 29)] + ['Amount', 'Time'])

    col1, col2 = st.columns(2)
    with col1:
        fig = go.Figure()
        fig.add_trace(go.Histogram(
            x=df[df['Class']==1][feature],
            name='Fraud', marker_color='#EF4444', opacity=0.7))
        fig.add_trace(go.Histogram(
            x=df[df['Class']==0][feature].sample(2000),
            name='Normal', marker_color='#22C55E', opacity=0.7))
        fig.update_layout(paper_bgcolor='#1A2333', plot_bgcolor='#1A2333',
            font=dict(color='#94A3B8'), barmode='overlay',
            title=f'{feature} Distribution by Class',
            xaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.05)'))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        stats = pd.DataFrame({
            'Fraud': df[df['Class']==1][feature].describe(),
            'Normal': df[df['Class']==0][feature].describe()
        }).round(4)
        st.markdown(f"#### 📊 {feature} Statistics")
        st.dataframe(stats, use_container_width=True)

    st.markdown('<p class="section-title">🔥 Correlation with Fraud</p>', unsafe_allow_html=True)
    corr = df[[f'V{i}' for i in range(1, 15)] + ['Amount', 'Class']].corr()['Class'].drop('Class').sort_values()
    fig2 = px.bar(x=corr.index, y=corr.values,
        color=corr.values, color_continuous_scale='RdYlGn',
        title='Feature Correlation with Fraud')
    fig2.update_layout(paper_bgcolor='#1A2333', plot_bgcolor='#1A2333',
        font=dict(color='#94A3B8'),
        xaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.05)'))
    st.plotly_chart(fig2, use_container_width=True)

# ML MODELS
elif page == "🤖 ML Models":
    st.markdown('<p class="section-title">🤖 Model Training & Evaluation</p>', unsafe_allow_html=True)

    features = [f'V{i}' for i in range(1, 29)] + ['Amount', 'Time']
    X = sample_df[features]
    y = sample_df['Class']

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    model_choice = st.selectbox("🤖 Select Model",
        ["Logistic Regression", "Decision Tree", "Random Forest"])

    with st.spinner(f"Training {model_choice}..."):
        if model_choice == "Logistic Regression":
            model = LogisticRegression(random_state=42, max_iter=1000)
        elif model_choice == "Decision Tree":
            model = DecisionTreeClassifier(random_state=42, max_depth=10)
        else:
            model = RandomForestClassifier(n_estimators=50, random_state=42)

        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        y_prob = model.predict_proba(X_test)[:, 1]

    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("✅ Accuracy", f"{acc*100:.1f}%")
    with col2:
        st.metric("🎯 Precision", f"{prec*100:.1f}%")
    with col3:
        st.metric("📊 Recall", f"{rec*100:.1f}%")
    with col4:
        from sklearn.metrics import f1_score
        f1 = f1_score(y_test, y_pred)
        st.metric("⚡ F1 Score", f"{f1*100:.1f}%")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<p class="section-title">📊 Confusion Matrix</p>', unsafe_allow_html=True)
        cm = confusion_matrix(y_test, y_pred)
        fig = px.imshow(cm, text_auto=True,
            labels=dict(x="Predicted", y="Actual"),
            x=['Normal', 'Fraud'], y=['Normal', 'Fraud'],
            color_continuous_scale='Reds')
        fig.update_layout(paper_bgcolor='#1A2333', font=dict(color='#94A3B8'))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<p class="section-title">📈 ROC Curve</p>', unsafe_allow_html=True)
        fpr, tpr, _ = roc_curve(y_test, y_prob)
        roc_auc = auc(fpr, tpr)
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=fpr, y=tpr,
            name=f'ROC (AUC = {roc_auc:.3f})',
            line=dict(color='#EF4444', width=2)))
        fig2.add_trace(go.Scatter(x=[0,1], y=[0,1],
            line=dict(dash='dash', color='#94A3B8'), name='Random'))
        fig2.update_layout(paper_bgcolor='#1A2333', plot_bgcolor='#1A2333',
            font=dict(color='#94A3B8'),
            xaxis=dict(title='FPR', gridcolor='rgba(255,255,255,0.05)'),
            yaxis=dict(title='TPR', gridcolor='rgba(255,255,255,0.05)'))
        st.plotly_chart(fig2, use_container_width=True)

# LIVE DETECTION
elif page == "🎯 Live Detection":
    st.markdown('<p class="section-title">🎯 Real-time Fraud Detection</p>', unsafe_allow_html=True)

    st.info("💡 Adjust the transaction features below to predict if it's fraudulent!")

    features = [f'V{i}' for i in range(1, 29)] + ['Amount', 'Time']
    X = sample_df[features]
    y = sample_df['Class']
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=50, random_state=42)
    model.fit(X_train, y_train)

    col1, col2 = st.columns(2)
    with col1:
        amount = st.number_input("💰 Transaction Amount ($)", 0.0, 30000.0, 100.0)
        time = st.number_input("⏰ Time (seconds)", 0.0, 200000.0, 50000.0)
        v1 = st.slider("V1", -5.0, 5.0, 0.0)
        v2 = st.slider("V2", -5.0, 5.0, 0.0)
        v3 = st.slider("V3", -5.0, 5.0, 0.0)
        v4 = st.slider("V4", -5.0, 5.0, 0.0)
    with col2:
        v5 = st.slider("V5", -5.0, 5.0, 0.0)
        v6 = st.slider("V6", -5.0, 5.0, 0.0)
        v7 = st.slider("V7", -5.0, 5.0, 0.0)
        v8 = st.slider("V8", -5.0, 5.0, 0.0)
        v9 = st.slider("V9", -5.0, 5.0, 0.0)
        v10 = st.slider("V10", -5.0, 5.0, 0.0)

    input_vals = [v1,v2,v3,v4,v5,v6,v7,v8,v9,v10] + [0.0]*18 + [amount, time]
    input_scaled = scaler.transform([input_vals])
    pred = model.predict(input_scaled)[0]
    prob = model.predict_proba(input_scaled)[0]

    if pred == 1:
        st.markdown(f"""
        <div style="background:#1A2333; border:2px solid #EF4444; border-radius:16px; padding:2rem; text-align:center; margin-top:1rem;">
            <h2 style="color:#EF4444; margin:0;">🚨 FRAUD DETECTED!</h2>
            <p style="color:#94A3B8; margin:0.5rem 0 0 0;">Fraud Probability: <strong style="color:#EF4444">{prob[1]*100:.1f}%</strong></p>
            <p style="color:#94A3B8;">This transaction is flagged as FRAUDULENT!</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="background:#1A2333; border:2px solid #22C55E; border-radius:16px; padding:2rem; text-align:center; margin-top:1rem;">
            <h2 style="color:#22C55E; margin:0;">✅ TRANSACTION SAFE</h2>
            <p style="color:#94A3B8; margin:0.5rem 0 0 0;">Safe Probability: <strong style="color:#22C55E">{prob[0]*100:.1f}%</strong></p>
            <p style="color:#94A3B8;">This transaction appears to be legitimate!</p>
        </div>
        """, unsafe_allow_html=True)

# DATA EXPLORER
elif page == "📋 Data Explorer":
    st.markdown('<p class="section-title">📋 Data Explorer</p>', unsafe_allow_html=True)

    filter_class = st.selectbox("Filter", ['All', 'Fraud Only', 'Normal Only'])
    show_df = df.copy()
    if filter_class == 'Fraud Only':
        show_df = df[df['Class'] == 1]
    elif filter_class == 'Normal Only':
        show_df = df[df['Class'] == 0].head(1000)

    st.dataframe(show_df.head(500), use_container_width=True, height=400)
    csv = show_df.head(1000).to_csv(index=False)
    st.download_button("📥 Download Sample", csv, "fraud_data.csv", "text/csv")

st.markdown("---")
st.markdown("""
<div style="text-align:center; color:#94A3B8; font-size:0.8rem; padding:1rem;">
    💳 Credit Card Fraud Detection | Built by <strong style="color:#EF4444">Taiyba Shaikh</strong> | ML Project
</div>
>>>>>>> 7fada881d00b51976fb97b6d32993d735666b598
""", unsafe_allow_html=True)