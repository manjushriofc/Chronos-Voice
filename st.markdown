
import streamlit as st

st.set_page_config(
    page_title="Chronos-Voice | Audio Forensics",
    page_icon="🎙️",
    layout="wide"
)

st.markdown("# Chronos-Voice")
st.markdown(
    "**AI-Powered Audio Forensic Audit System**"
)

st.markdown("---")

st.markdown("""
### Welcome to Chronos-Voice

Analyze voice recordings using machine learning
and acoustic feature extraction.

**Key capabilities**
- Audio feature analysis
- SVM-based voice classification
- ONNX model inference
- Structured forensic reports

*Note: Model predictions are assessments, not
definitive proof of audio authenticity.*
""")
