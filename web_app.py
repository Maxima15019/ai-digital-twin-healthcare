import streamlit as st
import pandas as pd
import pickle, joblib, os, sqlite3, random
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

st.set_page_config(page_title="AI Digital Twin Healthcare", layout="wide")

# ================= OTP LOGIN SYSTEM =================
users = {"admin":"admin123", "doctor":"healthcare"}

if "logged" not in st.session_state:
    st.session_state.logged = False
if "otp_sent" not in st.session_state:
    st.session_state.otp_sent = False
if "otp" not in st.session_state:
    st.session_state.otp = None

def login():
    st.title("🔐 Secure Doctor Login")

    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Send OTP"):
        if u in users and users[u] == p:
            st.session_state.otp = str(random.randint(100000,999999))
            st.session_state.otp_sent = True
            st.success(f"OTP Generated (Demo): {st.session_state.otp}")
        else:
            st.error("Invalid Credentials")

    if st.session_state.otp_sent:
        user_otp = st.text_input("Enter OTP")
        if st.button("Verify OTP"):
            if user_otp == st.session_state.otp:
                st.session_state.logged = True
                st.success("Login Successful ✅")
            else:
                st.error("Wrong OTP")

if not st.session_state.logged:
    login()
    st.stop()

# ================= MODEL LOADING =================
def load_model(path):
    if not os.path.exists(path):
        st.error(f"Missing file: {path}")
        st.stop()
    try:
        return pickle.load(open(path, "rb"))
    except:
        return joblib.load(path)

heart_model = load_model("heart_model.pkl")
heart_scaler = load_model("heart_scaler.pkl")
diabetes_model = load_model("diabetes_model.pkl")
diabetes_scaler = load_model("diabetes_scaler.pkl")
hypertension_model = load_model("hypertension_model.pkl")
hypertension_scaler = load_model("hypertension_scaler.pkl")

# ================= DATABASE =================
conn = sqlite3.connect("health_history.db", check_same_thread=False)
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS reports (
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT, age INTEGER, gender TEXT,
heart REAL, diabetes REAL, hyper REAL,
score REAL, date TEXT)""")
conn.commit()

def save_report(name, age, gender, h, d, hy, score):
    c.execute("INSERT INTO reports VALUES (NULL,?,?,?,?,?,?,?,?)",
              (name, age, gender, h, d, hy, score,
               datetime.now().strftime("%d-%m-%Y %H:%M")))
    conn.commit()

def get_all_patients():
    return pd.read_sql("SELECT DISTINCT name FROM reports", conn)

def get_history(name):
    return pd.read_sql("SELECT * FROM reports WHERE name=?", conn, params=(name,))

def delete_patient(name):
    c.execute("DELETE FROM reports WHERE name=?", (name,))
    conn.commit()

def delete_all():
    c.execute("DELETE FROM reports")
    conn.commit()

# ================= FUNCTIONS =================
def predict(model, scaler, data):
    df = pd.DataFrame([data])
    df = df.reindex(columns=scaler.feature_names_in_, fill_value=0)
    df_scaled = scaler.transform(df)
    return model.predict_proba(df_scaled)[0][1]

def risk(p):
    if p < 0.35: return "Low Risk"
    elif p < 0.65: return "Moderate Risk"
    return "High Risk"

def score(h,d,hy):
    return 100 - ((h+d+hy)/3)*100

def advice(h,d,hy):
    tips=[]
    if h>0.5: tips.append("Do daily cardio and avoid oily food.")
    if d>0.5: tips.append("Reduce sugar and refined carbs.")
    if hy>0.5: tips.append("Reduce salt and manage stress and have enough sleep.")
    if not tips: tips.append("Maintain your healthy lifestyle!")
    return tips

def pdf_report(name,age,gender,h,d,hy,s):
    file=f"{name}_report.pdf"
    doc=SimpleDocTemplate(file)
    styles=getSampleStyleSheet()
    story=[]
    story.append(Paragraph("AI Digital Twin Health Report", styles['Title']))
    story.append(Spacer(1,12))
    story.append(Paragraph(f"Patient: {name}", styles['Normal']))
    story.append(Paragraph(f"Age: {age} | Gender: {gender}", styles['Normal']))
    story.append(Spacer(1,12))
    story.append(Paragraph(f"Heart Risk: {h*100:.1f}% ({risk(h)})", styles['Normal']))
    story.append(Paragraph(f"Diabetes Risk: {d*100:.1f}% ({risk(d)})", styles['Normal']))
    story.append(Paragraph(f"Hypertension Risk: {hy*100:.1f}% ({risk(hy)})", styles['Normal']))
    story.append(Spacer(1,12))
    story.append(Paragraph(f"Health Score: {s:.1f}/100", styles['Normal']))
    story.append(Spacer(1,12))
    for t in advice(h,d,hy):
        story.append(Paragraph(t, styles['Normal']))
    doc.build(story)
    return file

# ================= UI =================
tab1, tab2 = st.tabs(["🧬 Patient Prediction", "🏥 Doctor Dashboard"])

with tab1:
    st.title("AI Healthcare Digital Twin")

    name = st.text_input("Patient Name")
    age = st.number_input("Age",1,120)
    gender = st.selectbox("Gender",["Male","Female"])

    st.subheader("Heart")
    cp = st.slider("Chest Pain",0,3)
    trestbps = st.number_input("Resting BP")
    chol = st.number_input("Cholesterol")
    thalach = st.number_input("Max Heart Rate")
    oldpeak = st.number_input("ST Depression")

    st.subheader("Diabetes")
    preg = st.number_input("Pregnancies",0,20) if gender=="Female" else 0
    glucose = st.number_input("Glucose")
    bmi = st.number_input("BMI")

    st.subheader("Hypertension")
    salt = st.number_input("Salt Intake")
    stress = st.slider("Stress Level",1,10)
    sleep = st.number_input("Sleep Hours")

    if st.button("Generate Report"):
        h=predict(heart_model,heart_scaler,{"age":age,"cp":cp,"trestbps":trestbps,"chol":chol,"thalach":thalach,"oldpeak":oldpeak})
        d=predict(diabetes_model,diabetes_scaler,{"Pregnancies":preg,"Glucose":glucose,"BMI":bmi,"Age":age})
        hy=predict(hypertension_model,hypertension_scaler,{"Age":age,"Salt_Intake":salt,"Stress_Score":stress,"Sleep_Duration":sleep,"BMI":bmi})
        s=score(h,d,hy)

        st.success("Health Report")
        st.write(f"Heart: {h*100:.1f}% ({risk(h)})")
        st.write(f"Diabetes: {d*100:.1f}% ({risk(d)})")
        st.write(f"Hypertension: {hy*100:.1f}% ({risk(hy)})")
        st.write(f"Health Score: {s:.1f}/100")

        for t in advice(h,d,hy):
            st.write("•",t)

        save_report(name,age,gender,h,d,hy,s)
        pdf=pdf_report(name,age,gender,h,d,hy,s)
        st.download_button("Download PDF",open(pdf,"rb"),file_name=pdf)

with tab2:
    st.title("Doctor Dashboard")

    patients=get_all_patients()
    if len(patients)==0:
        st.info("No records yet.")
    else:
        sel=st.selectbox("Select Patient",patients["name"])
        hist=get_history(sel)
        st.dataframe(hist)
        st.line_chart(hist.set_index("date")[["heart","diabetes","hyper"]])

        if st.button("❌ Delete This Patient"):
            delete_patient(sel)
            st.success("Patient deleted.")

        if st.button("⚠ Delete ALL Records"):
            delete_all()
            st.warning("All data deleted.")
