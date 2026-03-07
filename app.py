import streamlit as st
import os
import time
import hashlib
import numpy as np
import io
import random
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
from fpdf import FPDF
from src.features import extract_21d_features
from src.classifier import ChronosClassifier

# --- 1. INITIALIZE ML BACKEND ---
clf = ChronosClassifier()

# --- 2. REAL EMAIL SENDER FUNCTION ---
def send_otp_email(receiver_email, otp_code):
    # Pull credentials safely from Streamlit's hidden vault
    sender_email = st.secrets["EMAIL_USER"] 
    app_password = st.secrets["EMAIL_PASS"]
    
    msg = MIMEText(f"🛡️ CHRONOS-VOICE SECURITY\n\nYour OTP is: {otp_code}")
    msg['Subject'] = 'Chronos-Voice: Secure Access OTP'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, app_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        return True
    except Exception as e:
        return False

# --- 3. SESSION STATE NAVIGATION ---
if "page" not in st.session_state:
    st.session_state.page = "login"
if "otp_system" not in st.session_state:
    st.session_state.otp_system = {"code": None, "verified": False}
if "lang" not in st.session_state:
    st.session_state.lang = "English"

# --- 4. MULTI-LANGUAGE SELECTOR ---
language = st.sidebar.selectbox("Select Language", ["English", "Tamil", "Hindi"])
st.session_state.lang = language

translations = {
    "English": {
        "logintitle": "Chronos-Voice Secure Access Portal",
        "enter": "SEND OTP TO EMAIL",
        "otp_prompt": "Enter 6-Digit OTP sent to Email",
        "verify": "VERIFY & ENTER SYSTEM",
        "dashboard": "Forensic Audit Dashboard",
        "uploadlabel": "Drag and Drop Audio Evidence Here",
        "startaudit": "START DEEPFAKE AUDIT",
        "report": "Chronos-Voice: Final Forensic Audit Report",
        "download": "DOWNLOAD FORENSIC PDF",
        "safetytitle": "Women's Cyber Safety Measures",
        "resultfake": "DEEPFAKE DETECTED ⚠️",
        "resultreal": "REAL VOICE VERIFIED ✅"
    },
    "Tamil": {
        "logintitle": "க்ரோனோஸ்-வாய்ஸ் பாதுகாப்பு அணுகல்",
        "enter": "மின்னஞ்சலுக்கு OTP அனுப்பவும்",
        "otp_prompt": "மின்னஞ்சலில் வந்த 6 இலக்க OTP ஐ உள்ளிடவும்",
        "verify": "சரிபார் & உள்ளே நுழையவும்",
        "dashboard": "நீதிமன்ற ஆய்வு டாஷ்போர்டு",
        "uploadlabel": "ஆடியோ ஆதாரத்தை இங்கே இழுக்கவும்",
        "startaudit": "டீப்‌ஃபேக் ஆய்வு தொடங்கவும்",
        "report": "க்ரோனோஸ்-வாய்ஸ்: இறுதி நீதிமன்ற அறிக்கை",
        "download": "நீதிமன்ற PDF ஐ பதிவிறக்கவும்",
        "safetytitle": "பெண்களுக்கான சைபர் பாதுகாப்பு",
        "resultfake": "டீப்‌ஃபேக் கண்டறியப்பட்டது ⚠️",
        "resultreal": "உண்மையான குரல் உறுதிப்படுத்தப்பட்டது ✅"
    },
    "Hindi": {
        "logintitle": "क्रोनोस-वॉइस सुरक्षित पहुँच पोर्टल",
        "enter": "OTP उत्पन्न करें",
        "otp_prompt": "ईमेल पर भेजा गया 6-अंकीय OTP दर्ज करें",
        "verify": "सत्यापित करें और प्रवेश करें",
        "dashboard": "फ़ॉरेंसिक ऑडिट डैशबोर्ड",
        "uploadlabel": "यहाँ ऑडियो सबूत ड्रैग करें",
        "startaudit": "डीपफेक ऑडिट शुरू करें",
        "report": "क्रोनोस-वॉइस: अंतिम फ़ॉरेंसिक ऑडिट रिपोर्ट",
        "download": "फ़ॉरेंसिक PDF डाउनलोड करें",
        "safetytitle": "महिलाओं के लिए साइबर सुरक्षा उपाय",
        "resultfake": "डीपफेक का पता चला ⚠️",
        "resultreal": "असली आवाज़ सत्यापित ✅"
    }
}
t = translations.get(st.session_state.lang, translations["English"])

# --- 5. UI STYLING ---
st.set_page_config(page_title="Chronos-Voice Forensic", layout="wide")
st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #0c0c1a 0%, #1a1a2e 50%, #16213e 100%); color: #e0e6ed; }
    h1, h2, h3 { color: #00d4ff !important; text-shadow: 0 0 20px rgba(0, 212, 255, 0.5); }
    .cyber-card { background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(15px); border: 1px solid rgba(0, 212, 255, 0.3); border-radius: 20px; padding: 40px; }
    .safety-box { background: rgba(255, 107, 107, 0.1); border-left: 6px solid #ff6b6b; padding: 20px; border-radius: 10px; margin: 20px 0; }
    [data-testid="stFileUploader"] { border: 3px dashed #00d4ff !important; background: rgba(0, 212, 255, 0.05) !important; }
</style>
""", unsafe_allow_html=True)

# --- 6. HELPER: PDF GENERATOR ---
def generate_pdf(audit_id, metrics, score):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_fill_color(0, 43, 92)
    pdf.rect(0, 0, 210, 40, 'F')
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", 'B', 18)
    pdf.cell(200, 25, txt="CHRONOS-VOICE SECURE ACCESS PORTAL", ln=True, align='C')
    pdf.set_text_color(0, 0, 0)
    pdf.ln(20)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(100, 10, txt="ANALYST DETAILS", ln=True)
    pdf.set_font("Arial", '', 10)
    pdf.cell(100, 7, txt=f"Name: {st.session_state.user_name}", ln=True)
    pdf.cell(100, 7, txt=f"Email: {st.session_state.user_email}", ln=True)
    pdf.cell(100, 7, txt=f"Aadhaar: {st.session_state.user_aadhaar}", ln=True)
    
    now = datetime.now()
    pdf.cell(100, 7, txt=f"Report Generated: {now.strftime('%Y-%m-%d')} | {now.strftime('%H:%M:%S')}", ln=True)
    
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt=f"Audit Trace ID: {audit_id}", ln=True)
    res_text = "RESULT: DEEPFAKE DETECTED" if score < 0.35 else "RESULT: REAL VOICE VERIFIED"
    pdf.cell(200, 10, txt=res_text, ln=True)
    return pdf.output(dest='S').encode('latin-1')

# --- 7. PAGE 1: LOGIN ---
if st.session_state.page == "login":
    st.title(t["logintitle"])
    with st.form("login_form"):
        st.markdown('<div class="cyber-card">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name")
            email = st.text_input("Official Email ID")
        with col2:
            phone = st.text_input("Phone Number")
            aadhaar = st.text_input("Aadhaar Number")
        submit = st.form_submit_button(t["enter"], use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    if submit:
        if name and email and phone and aadhaar:
            st.session_state.user_name, st.session_state.user_email = name, email
            st.session_state.user_phone, st.session_state.user_aadhaar = phone, aadhaar
            otp = str(random.randint(100000, 999999))
            if send_otp_email(email, otp):
                st.session_state.otp_system["code"] = otp
                st.session_state.page = "otp_verify"
                st.rerun()
        else:
            st.error("Missing Security Credentials")

# --- 8. PAGE 2: OTP VERIFICATION ---
elif st.session_state.page == "otp_verify":
    st.title("🔐 Email Verification Required")
    st.markdown('<div class="cyber-card">', unsafe_allow_html=True)
    st.write(f"A secure OTP has been sent to **{st.session_state.user_email}**")
    user_otp = st.text_input(t["otp_prompt"], max_chars=6)
    if st.button(t["verify"], use_container_width=True):
        if user_otp == st.session_state.otp_system["code"]:
            st.success("Identity Verified!")
            time.sleep(1)
            st.session_state.page = "audit"
            st.rerun()
        else:
            st.error("Invalid OTP.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- 9. PAGE 3: DASHBOARD ---
elif st.session_state.page == "audit":
    st.title(f"🛡️ {t['dashboard']}")
    uploaded_file = st.file_uploader(t["uploadlabel"], type=['mp3', 'wav', 'mp4'])
    st.markdown(f"""<div class="safety-box"><h4>🛡️ {t['safetytitle']}</h4>
    <ul><li>Never share OTP over calls</li><li>Verify at <a href='https://cybercrime.gov.in'>cybercrime.gov.in</a></li></ul></div>""", unsafe_allow_html=True)
    
    if uploaded_file:
        file_bytes = uploaded_file.read()
        if st.button(t["startaudit"], use_container_width=True):
            with st.spinner("🔬 Scanning..."):
                temp_path = f"audit_{uploaded_file.name}"
                with open(temp_path, "wb") as f: f.write(file_bytes)
                vector, metrics = extract_21d_features(temp_path)
                raw_pred = clf.predict(vector)
                st.session_state.trust_score = float(raw_pred[0][1]) if isinstance(raw_pred, (list, np.ndarray)) else float(raw_pred)
                st.session_state.metrics = metrics
                st.session_state.audit_id = hashlib.sha256(file_bytes).hexdigest()[:16]
                st.session_state.page = "report"
                os.remove(temp_path)
                st.rerun()

# --- 10. PAGE 4: REPORT ---
elif st.session_state.page == "report":
    # FIX: Added 'report' key for all languages to translation dict above
    st.title(f"📊 {t['report']}")
    score = st.session_state.trust_score
    audit_id = st.session_state.audit_id
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown('<div class="cyber-card">', unsafe_allow_html=True)
        if score < 0.35: st.error(f"**{t['resultfake']}**")
        else: st.success(f"**{t['resultreal']}**")
        
        st.metric("System Confidence", f"{int(score * 100)}%")
        # Added date and time to the dashboard display
        st.write(f"**Analysis Date:** {datetime.now().strftime('%Y-%m-%d')}")
        st.write(f"**Analysis Time:** {datetime.now().strftime('%H:%M:%S')}")
        st.write(f"**Audit ID:** `{audit_id}`")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="cyber-card">', unsafe_allow_html=True)
        st.subheader("👤 User Identity")
        st.write(f"**Name:** {st.session_state.user_name}")
        st.write(f"**Aadhaar:** {st.session_state.user_aadhaar}")
        st.markdown('</div>', unsafe_allow_html=True)
        
    pdf_bytes = generate_pdf(audit_id, st.session_state.metrics, score)
    st.download_button(t["download"], data=pdf_bytes, file_name=f"ChronosReport_{audit_id}.pdf", use_container_width=True)
    
    if st.button("🔄 Start New Audit"):
        st.session_state.page = "audit"
        st.rerun()