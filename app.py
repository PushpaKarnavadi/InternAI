import streamlit as st
import sqlite3
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

st.set_page_config(page_title="Intern AI", layout="wide")

# ---------------- DATABASE CONNECTION ----------------
conn = sqlite3.connect("inter AI.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    name TEXT,
    email TEXT PRIMARY KEY,
    password TEXT,
    skills TEXT,
    education TEXT,
    location TEXT
)
""")
conn.commit()

# ---------------- SESSION STATE ----------------
if "current_user" not in st.session_state:
    st.session_state.current_user = None

# ---------------- CSS ----------------
st.markdown("""
<style>

/* Main background */
.stApp {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    color: white;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #111827;
    border-right: 1px solid #374151;
}

/* Title */
.main-title {
    text-align: center;
    padding: 25px;
    border-radius: 20px;
    background: linear-gradient(90deg, #2563eb, #7c3aed);
    color: white;
    box-shadow: 0 8px 25px rgba(0,0,0,0.3);
}

/* Cards */
.card {
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(10px);
    padding: 20px;
    border-radius: 18px;
    border: 1px solid rgba(255,255,255,0.1);
    margin-bottom: 20px;
    transition: 0.3s;
}

.card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 25px rgba(0,0,0,0.3);
}

/* Buttons */
.stButton > button {
    width: 100%;
    border-radius: 12px;
    height: 3em;
    background: linear-gradient(90deg, #2563eb, #7c3aed);
    color: white;
    border: none;
    font-weight: bold;
}

.stButton > button:hover {
    background: linear-gradient(90deg, #1d4ed8, #6d28d9);
    color: white;
}

/* Input boxes */
.stTextInput > div > div > input {
    border-radius: 10px;
}

/* Footer */
.footer {
    text-align: center;
    padding: 20px;
    color: #cbd5e1;
}
            .login-box {
    background: rgba(255,255,255,0.08);
    padding: 35px;
    border-radius: 20px;
    width: 400px;
    margin: auto;
    margin-top: 40px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.3);
}

/* Fix invisible text */
label, .stTextInput label, .stSelectbox label {
    color: white !important;
    font-weight: 500;
}

p, h1, h2, h3, h4, h5, h6, span {
    color: white !important;
}

/* Input text color */
.stTextInput input {
    color: black !important;
    background-color: white !important;
}

</style>
            
            
""", unsafe_allow_html=True)
# ---------------- ML MODEL ----------------
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

data = {
    "skills": [
        "python sql excel",
        "html css javascript",
        "python machine learning pandas",
        "java kotlin android",
        "aws cloud devops",
        "python data analysis numpy",
        "react js html css",
        "deep learning python tensorflow",
        "android java firebase",
        "cloud aws kubernetes"
    ],
    "role": [
        "Data Analyst",
        "Web Developer",
        "ML Intern",
        "App Developer",
        "Cloud Intern",
        "Data Analyst",
        "Web Developer",
        "ML Intern",
        "App Developer",
        "Cloud Intern"
    ]
}

df = pd.DataFrame(data)

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df["skills"])
y = df["role"]

# Train-test split (for accuracy)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LogisticRegression(max_iter=200)
model.fit(X_train, y_train)

# Accuracy
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

# 🔮 Predict Top Roles
def predict_top_roles(skills):
    skills_text = " ".join(skills)
    vector = vectorizer.transform([skills_text])

    probs = model.predict_proba(vector)[0]
    roles = model.classes_

    results = list(zip(roles, probs))
    results.sort(key=lambda x: x[1], reverse=True)

    return results[:3]

# ---------------- AI MATCH FUNCTION ----------------
def match_score(student_skills, job_role):
    role_skills = {
        "Data Analyst": ["python", "excel", "sql"],
        "Web Developer": ["html", "css", "javascript"],
        "ML Intern": ["python", "machine learning", "pandas"],
        "App Developer": ["java", "kotlin", "android"],
        "Cloud Intern": ["aws", "cloud", "devops"]
    }

    required = role_skills.get(job_role, [])
    match = len(set(student_skills) & set(required))
    return int((match / len(required)) * 100) if required else 0

# ---------------- SIDEBAR ----------------
menu = st.sidebar.radio(
    "📌 Navigation",
    ["🏠 Home", "📝 Student Registration", "🔐 Login", "💼 Internships"]
)

if st.session_state.current_user:
    if st.sidebar.button("Logout"):
        st.session_state.current_user = None
        st.success("Logged out successfully")


# ---------------- HOME ----------------
if menu == "🏠 Home":

    st.markdown("""
    <div class="main-title">
        <h1>🚀 Internsync AI</h1>
        <h4>AI-Powered Internship Matching Platform</h4>
        <p>Smartly connecting students with the right opportunities</p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    c1, c2, c3 = st.columns(3)

    c1.markdown("""
    <div class="card">
        <h2>👨‍🎓</h2>
        <h3>Students</h3>
        <h1>500+</h1>
    </div>
    """, unsafe_allow_html=True)

    c2.markdown("""
    <div class="card">
        <h2>🏢</h2>
        <h3>Companies</h3>
        <h1>120+</h1>
    </div>
    """, unsafe_allow_html=True)

    c3.markdown("""
    <div class="card">
        <h2>💼</h2>
        <h3>Internships</h3>
        <h1>540+</h1>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="footer">
    © 2026 Intern AI | MCA  Project
    </div>
    """, unsafe_allow_html=True)

# ---------------- REGISTRATION ----------------


elif menu == "📝 Student Registration":

    st.info("Example Skills: python, html, css, sql, machine learning")

    with st.form("register_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        skills = st.text_input("Skills (comma separated)")
        education = st.text_input("Education")
        location = st.text_input("Preferred Location")

        submitted = st.form_submit_button("Register")

        if submitted:
            if not name or not email or not skills or not password:
                st.error("Please fill all required fields")
            else:
                try:
                    cursor.execute(
                        "INSERT INTO students VALUES (?, ?, ?, ?, ?, ?)",
                        (
                            name,
                            email,
                            password,
                            skills.lower(),
                            education,
                            location
                        )
                    )
                    conn.commit()
                    st.success("Registration Successful ✅")
                except:
                    st.error("User already exists!")


# ---------------- LOGIN ----------------
elif menu == "🔐 Login":

    col1, col2, col3 = st.columns([1,2,1])

    with col2:

        st.markdown("""
        <div class="login-box">
            <h2 style='text-align:center; color:white; margin-bottom:30px;'>
                🔐 Login
            </h2>
        """, unsafe_allow_html=True)

        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            cursor.execute(
                "SELECT * FROM students WHERE email=? AND password=?",
                (email, password)
            )

            user = cursor.fetchone()

            if user:
                st.session_state.current_user = {
                    "name": user[0],
                    "email": user[1],
                    "skills": [s.strip().lower() for s in user[3].split(",")]
                }

                st.success(f"Welcome {user[0]} 🎉")

            else:
                st.error("Invalid email or password")

        st.markdown("</div>", unsafe_allow_html=True)
# ---------------- INTERNSHIPS ----------------
elif menu == "💼 Internships":
    st.header("Recommended Internships")

    if not st.session_state.current_user:
        st.warning("Please login first ⚠️")
    else:
        student = st.session_state.current_user

        st.success(f"Logged in as {student['name']}")

        # 🔮 Predict roles
        top_roles = predict_top_roles(student["skills"])

        st.subheader("🎯 Recommended Roles")

        for role, score in top_roles:
            st.write(f"👉 {role} ({round(score*100, 2)}%)")

        best_role = top_roles[0][0]

        internships = [
            {"company": "ABC Tech", "role": "Data Analyst"},
            {"company": "XYZ Pvt Ltd", "role": "Web Developer"},
            {"company": "AI Solutions", "role": "ML Intern"},
            {"company": "TechNova", "role": "App Developer"},
            {"company": "CloudNet", "role": "Cloud Intern"}
        ]

        for job in internships:
            if job["role"] == best_role:
                score = match_score(student["skills"], job["role"])

        st.markdown(f"""
        <div class="card">
            <h2>💼 {job['role']}</h2>
            <h4>🏢 {job['company']}</h4>
            <p>🎯 Match Score: <b>{score}%</b></p>
            <p style="color:#22c55e;"><b>Best Match Found ✅</b></p>
        </div>
        """, unsafe_allow_html=True)

        # Progress bar
        st.progress(score / 100)