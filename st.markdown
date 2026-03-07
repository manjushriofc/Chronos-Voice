# --- PARAMETER HANDLING ---
# Get URL parameters if the user clicked a menu button
params = st.query_params

if "lang" in params:
    st.session_state.lang = params["lang"]
if "theme" in params:
    st.session_state.theme = params["theme"]

# Fallback defaults if session state is empty
if 'lang' not in st.session_state:
    st.session_state.lang = 'en'
if 'theme' not in st.session_state:
    st.session_state.theme = 'cyber'