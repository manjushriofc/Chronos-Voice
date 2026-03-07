import streamlit as st
import os
import time
import hashlib
import numpy as np
import io
import zipfile
from fpdf import FPDF 
from src.features import extract_21d_features
from src.classifier import ChronosClassifier

# --- 1. INITIALIZE ML BACKEND ---
clf = ChronosClassifier()

# --- 2. MULTI-LANGUAGE TRANSLATION DICTIONARY ---
translations = {
    "English": {
        "title": "🛡️ Chronos-Voice: Forensic Audit",
        "analyst": "Current Analyst: Ravi (SBI Chennai Branch)",
        "offline": "🔒 BANK-GRADE OFFLINE MODE",
        "sidebar_title": "🔍 FORENSIC EVIDENCE",
        "phonetic": "Phonetic Optimization",
        "stability": "MFCC Stability",
        "pitch": "Pitch Variance (F0)",
        "bio": "Biological Signals",
        "breath_ok": "🫁 NATURAL BREATH DETECTED",
        "breath_no": "🫁 NO NATURAL BREATH PATTERN",
        "heatmap": "🧬 ANOMALY HEATMAP",
        "input_header": "Audio Evidence Input",
        "report_portal": "📊 Access National Cyber Crime Reporting Portal ↗️",
        "start_audit": "START DEEPFAKE AUDIT",
        "confidence": "System Confidence",
        "detected": "🚩 DEEPFAKE DETECTED",
        "verified": "✅ REAL VOICE VERIFIED",
        "export": "📄 Export Report (PDF)"
    },
    "Hindi": {
        "title": "🛡️ क्रोनोस-वॉइस: फॉरेंसिक ऑडिट",
        "analyst": "वर्तमान विश्लेषक: रवि (SBI चेन्नई शाखा)",
        "offline": "🔒 बैंक-ग्रेड ऑफलाइन मोड",
        "sidebar_title": "🔍 फॉरेंसिक साक्ष्य",
        "phonetic": "ध्वन्यात्मक अनुकूलन",
        "stability": "MFCC स्थिरता",
        "pitch": "पिच भिन्नता (F0)",
        "bio": "जैविक संकेत",
        "breath_ok": "🫁 प्राकृतिक सांस का पता चला",
        "breath_no": "🫁 कोई प्राकृतिक सांस पैटर्न नहीं",
        "heatmap": "🧬 विसंगति हीटमैप",
        "input_header": "ऑडियो साक्ष्य इनपुट",
        "report_portal": "📊 राष्ट्रीय साइबर अपराध रिपोर्टिंग पोर्टल ↗️",
        "start_audit": "डीपफेक ऑडिट शुरू करें",
        "confidence": "सिस्टम विश्वास",
        "detected": "🚩 डीपफेक पाया गया",
        "verified": "✅ असली आवाज सत्यापित",
        "export": "📄 रिपोर्ट निर्यात करें (PDF)"
    },
    "Tamil": {
        "title": "🛡️ குரோனோஸ்-வாய்ஸ்: தடயவியல் தணிக்கை",
        "analyst": "தற்போதைய ஆய்வாளர்: ரவி (SBI சென்னை கிளை)",
        "offline": "🔒 வங்கி-தர ஆஃப்லைன் பயன்முறை",
        "sidebar_title": "🔍 தடயவியல் சான்றுகள்",
        "phonetic": "ஒலியியல் மேம்படுத்தல்",
        "stability": "MFCC நிலைத்தன்மை",
        "pitch": "சுருதி மாறுபாடு (F0)",
        "bio": "உயிரியல் சமிக்ஞைகள்",
        "breath_ok": "🫁 இயற்கை சுவாசம் கண்டறியப்பட்டது",
        "breath_no": "🫁 இயற்கை சுவாச முறை இல்லை",
        "heatmap": "🧬 முரண்பாடு வெப்பவரைபடம்",
        "input_header": "ஆடியோ ஆதார உள்ளீடு",
        "report_portal": "📊 தேசிய சைபர் கிரைம் போர்டல் ↗️",
        "start_audit": "டீப்ஃபேக் தணிக்கையைத் தொடங்கு",
        "confidence": "அமைப்பு நம்பிக்கை",
        "detected": "🚩 டீப்ஃபேக் கண்டறியப்பட்டது",
        "verified": "✅ உண்மையான குரல் சரிபார்க்கப்பட்டது",
        "export": "📄 அறிக்கையை ஏற்றுமதி செய் (PDF)"
    }
}

# --- 3. SET PAGE CONFIG & LEGIBILITY CSS ---
st.set_page_config(page_title="Chronos-Voice Forensic", layout="wide")

st.markdown("""
    <style>
    /* SOFT LIGHT BACKGROUND FOR READABILITY */
    .stApp {
        background: linear-gradient(135deg, #e0eafc 0%, #cfdef3 100%);
        color: #2c3e50;
    }

    /* CREATIVE DRAG & DROP BOX STYLING */
    [data-testid="stFileUploader"] {
        background-color: #ffffff;
        border: 2px dashed #3498db;
        border-radius: 15px;
        padding: 20px;
        transition: all 0.3s ease;
    }
    [data-testid="stFileUploader"]:hover {
        border-color: #2ecc71;
        background-color: #f7f9fb;
    }

    /* ENHANCED TEXT CONTRAST FOR SBI BRANCH USE */
    div[data-testid="stVerticalBlock"] > div:has(div.stMarkdown) {
        background: rgba(255, 255, 255, 0.95) !important;
        border-radius: 12px !important;
        padding: 25px !important;
        border: 1px solid #dcdde1 !important;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1) !important;
    }

    /* SIDEBAR LEGIBILITY */
    section[data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 2px solid #3498db;
    }

    /* HIGH-CONTRAST LABELS */
    .deviance-label { color: #57606f !important; font-size: 11px; text-transform: uppercase; font-weight: 800; letter-spacing: 1.2px; }
    .deviance-value { color: #1e3799 !important; font-family: 'Courier New', monospace; font-size: 18px; font-weight: bold; }
    
    h1, h2, h3, p { color: #1e272e !important; font-weight: 700 !important; }

    /* STATUS METRICS */
    [data-testid="stMetricValue"] { color: #2980b9 !important; font-weight: 900 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- HELPER FUNCTIONS (KEEPING ORIGINAL LOGIC) ---
def generate_audit_hash(file_data):
    return hashlib.sha256(file_data).hexdigest()[:16]

def generate_pdf_report(audit_id, metrics, score):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Chronos-Voice Forensic Audit Report", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Audit Trace ID: {audit_id}", ln=True)
    pdf.cell(200, 10, txt=f"System Confidence: {int(score*100)}%", ln=True)
    pdf.cell(200, 10, txt=f"MFCC Stability: {100-metrics['mfcc_std']:.1f}%", ln=True)
    pdf.cell(200, 10, txt=f"Pitch Variance: {metrics['pitch']:.1f}Hz", ln=True)
    pdf.ln(10)
    pdf.cell(200, 10, txt="Result: " + ("DEEPFAKE DETECTED" if score < 0.35 else "REAL VOICE VERIFIED"), ln=True)
    return pdf.output(dest='S').encode('latin-1')

# --- 4. SIDEBAR: FORENSIC EVIDENCE ---
with st.sidebar:
    st.markdown("### ⋮ Settings")
    selected_lang = st.selectbox("🌐 Language", ["English", "Hindi", "Tamil"])
    st.divider()
    
    t = translations.get(selected_lang, translations["English"])
    st.markdown(f"### {t['sidebar_title']}")
    st.markdown(f"<div class='deviance-label'>{t['phonetic']}</div>", unsafe_allow_html=True)
    lang_focus = st.selectbox("Model Focus", ["Tamil", "Hindi", "Malayalam", "Telugu"])

    if 'metrics' in st.session_state:
        m = st.session_state.metrics
        st.markdown(f"<div class='deviance-label'>{t['stability']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='deviance-value'>{100-m['mfcc_std']:.1f}%</div>", unsafe_allow_html=True)
        
        st.markdown(f"<div class='deviance-label'>{t['pitch']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='deviance-value'>{m['pitch']:.1f}Hz</div>", unsafe_allow_html=True)

        st.markdown(f"<div class='deviance-label'>{t['bio']}</div>", unsafe_allow_html=True)
        breath_text = t['breath_ok'] if m['jitter'] > 0.005 else t['breath_no']
        st.markdown(f"<div class='bio-box' style='background:#f1f2f6; border-radius:10px;'>{breath_text}</div>", unsafe_allow_html=True)

# --- 5. MAIN DASHBOARD ---
st.title(t['title'])
st.write(f"**{t['analyst']}**")
st.markdown(f"<span style='background: #27ae60; padding:8px 20px; border-radius:50px; font-size:12px; font-weight:bold; color:white;'>{t['offline']}</span>", unsafe_allow_html=True)

# CREATIVE UPLOADER AREA
uploaded_file = st.file_uploader(t['input_header'], type=['mp3', 'wav', 'mp4'])
st.markdown(f"[**{t['report_portal']}**](https://cybercrime.gov.in/Webform/Crime_AuthoLogin.aspx)")

if uploaded_file:
    file_bytes = uploaded_file.read()
    audit_id = generate_audit_hash(file_bytes)
    st.info(f"**Audit Trace ID:** `{audit_id}`")
    
    if st.button(t['start_audit']):
        with st.spinner("Analyzing spectral patterns..."):
            temp_path = f"audit_{uploaded_file.name}"
            with open(temp_path, "wb") as f: f.write(file_bytes)
            
            # Logic preservation
            vector, metrics = extract_21d_features(temp_path)
            st.session_state.metrics = metrics
            st.session_state.trust_score = clf.predict(vector) 
            st.session_state.audit_complete = True
            os.remove(temp_path)

    if 'audit_complete' in st.session_state:
        col1, col2 = st.columns(2)
        score = st.session_state.trust_score
        with col1:
            st.metric(t['confidence'], f"{int(score * 100)}%")
            if score < 0.35: st.error(t['detected'])
            else: st.success(t['verified'])
        
        with col2:
            pdf_data = generate_pdf_report(audit_id, st.session_state.metrics, score)
            st.download_button(t['export'], data=pdf_data, file_name=f"Chronos_Report_{audit_id}.pdf", use_container_width=True)