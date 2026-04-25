import streamlit as st
import joblib
import numpy as np

# Page setup
st.set_page_config(page_title="Amblyopia Detector", page_icon="👁️", layout="wide")

# STYLES 
st.markdown("""
    <style>
        /* Main background */
        .stApp {
            background-color: #f9f7fb;
        }
        
        /* Sidebar styling */
        section[data-testid="stSidebar"] {
            background-color: #1a1a2e;
            border-right: 2px solid #16213e;
        }
        
        /* Sidebar text and labels */
        section[data-testid="stSidebar"] .stMarkdown, 
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] .stSelectbox label,
        section[data-testid="stSidebar"] .stNumberInput label {
            color: #ffffff !important;
            font-weight: 500 !important;
        }
        
        section[data-testid="stSidebar"] h2 {
            color: #aa7bc2 !important;
            font-weight: 600 !important;
        }
        
        /* Sidebar selectbox styling */
        section[data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] {
            background-color: #0f0f1a;
            border-radius: 10px;
            border: 1px solid #2a2a4a;
        }
        
        section[data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] input {
            color: white !important;
            background-color: #0f0f1a !important;
        }
        
        /* Sidebar number inputs - dark theme */
        section[data-testid="stSidebar"] .stNumberInput div[data-baseweb="input"] {
            background-color: #0f0f1a !important;
            border-radius: 10px !important;
            border: 1px solid #2a2a4a !important;
        }
        
        section[data-testid="stSidebar"] .stNumberInput input {
            background-color: #0f0f1a !important;
            border-radius: 10px !important;
            border: none !important;
            color: white !important;
            font-weight: 500 !important;
        }
        
        /* Sidebar +/- buttons */
        section[data-testid="stSidebar"] .stNumberInput button {
            background-color: #0f0f1a !important;
            border: 1px solid #2a2a4a !important;
            color: white !important;
            font-weight: bold !important;
            font-size: 18px !important;
        }
        
        section[data-testid="stSidebar"] .stNumberInput button:hover {
            background-color: #2a2a4a !important;
            color: white !important;
        }
        
        section[data-testid="stSidebar"] .stNumberInput button svg {
            color: white !important;
            fill: white !important;
        }
        
        /* Dropdown menu */
        section[data-testid="stSidebar"] .stSelectbox ul {
            background-color: #0f0f1a !important;
        }
        
        /* Main buttons */
        div.stButton > button {
            background: linear-gradient(135deg, #8957a5 0%, #aa7bc2 100%);
            color: white;
            border-radius: 12px;
            padding: 12px 24px;
            font-size: 16px;
            font-weight: bold;
            width: 100%;
            border: none;
            box-shadow: 0 2px 8px rgba(137, 87, 165, 0.25);
            transition: all 0.3s ease;
        }
        
        div.stButton > button:hover {
            background: linear-gradient(135deg, #774591 0%, #9b6ab5 100%);
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(137, 87, 165, 0.35);
        }
        
        /* Card styles for metrics and summary */
        .metric-card {
            background: linear-gradient(135deg, #ffffff 0%, #f5eff9 100%);
            padding: 20px;
            border-radius: 16px;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.04);
            border: 1px solid #e8ddf0;
        }
        
        /* Info boxes */
        .custom-info {
            background-color: #f0eaf5;
            border-left: 4px solid #8957a5;
            padding: 16px;
            border-radius: 12px;
            margin: 10px 0;
            color: #3a2c42;
        }
        
        /* App title section */
        .app-title {
            text-align: center;
            margin-bottom: 20px;
        }
        
        .app-title h1 {
            font-size: 42px;
            font-weight: 700;
            color: #8957a5 !important;
            margin-bottom: 5px;
            background: transparent;
        }
        
        .app-title p {
            color: #8957a5;
            font-size: 16px;
            opacity: 0.8;
        }
        
        /* Welcome banner */
        .welcome-message {
            background: linear-gradient(135deg, #e8ddf0 0%, #f3edf7 100%);
            padding: 20px;
            border-radius: 16px;
            text-align: center;
            margin: 20px 0 25px 0;
            border: 1px solid #dccce8;
        }
        
        .welcome-message h3 {
            color: #8957a5 !important;
            margin-bottom: 8px;
            font-size: 22px;
        }
        
        .welcome-message p {
            color: #5a4a6a;
            font-size: 15px;
            margin: 0;
        }
        
        /* Result cards */
        .result-success {
            background-color: #e8f5e9;
            padding: 25px;
            border-radius: 16px;
            border-left: 5px solid #4CAF50;
        }
        
        .result-error {
            background-color: #ffebee;
            padding: 25px;
            border-radius: 16px;
            border-left: 5px solid #f44336;
        }
        
        /* Risk level colors */
        .risk-high { color: #f44336; font-weight: bold; }
        .risk-medium { color: #ff9800; font-weight: bold; }
        .risk-low { color: #4caf50; font-weight: bold; }
        
        h1, h2, h3 {
            color: #8957a5 !important;
        }
        
        hr {
            border-color: #e2d4eb;
        }
        
        /* Footer */
        .footer {
            text-align: center;
            color: #a090b0;
            font-size: 16px;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #e2d4eb;
        }
        
        /* About page metric cards */
        .about-metric-card {
            background: linear-gradient(135deg, #ffffff 0%, #f5eff9 100%);
            padding: 25px 15px;
            border-radius: 16px;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.04);
            border: 1px solid #e8ddf0;
        }
        
        .about-metric-card h2 {
            color: #8957a5 !important;
            font-size: 36px;
            margin-bottom: 8px;
            margin-left: 12px;
            text-align: center;
            font-weight: 700;
            display: block;
            width: 100%;
        }
        
        .about-metric-card p {
            color: #5a4a6a;
            font-weight: 500;
            margin: 0;
            text-align: center;
            font-size: 14px;
            display: block;
            width: 100%;
        }
        
        /* Patient summary cards */
        .summary-card {
            background: linear-gradient(135deg, #ffffff 0%, #f5eff9 100%);
            padding: 12px;
            border-radius: 12px;
            text-align: center;
            border: 1px solid #e8ddf0;
        }
        
        .summary-card b {
            color: #8957a5;
            font-size: 14px;
            display: block;
            margin-bottom: 5px;
        }
        
        .summary-card span {
            color: #3a2c42;
            font-size: 18px;
            font-weight: 600;
        }
    </style>
""", unsafe_allow_html=True)

# Load the trained model
@st.cache_resource
def load_model():
    return joblib.load("amblyopia_rf_model.pkl")

model = load_model()

# Track page navigation and reset state
if 'page' not in st.session_state:
    st.session_state.page = 'main'

if 'reset_trigger' not in st.session_state:
    st.session_state.reset_trigger = 0

# ABOUT PAGE
def about_page():
    # Back button to return to main page
    col1, col2, col3 = st.columns([1, 6, 1])
    with col1:
        if st.button("← Back", use_container_width=True):
            st.session_state.page = 'main'
            st.rerun()
    
    st.markdown("""
        <div style="text-align:center; margin: 10px 0 20px 0;">
            <h1 style="font-size: 36px;">📖 About Amblyopia</h1>
            <p style="color:#5a4a6a;">Understanding Lazy Eye - Causes, Symptoms & Treatment</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Three columns for Symptoms, Causes, Treatment
    colA, colB, colC = st.columns(3)
    
    with colA:
        st.markdown("""
            <div class="metric-card" style="text-align:left;">
                <h3 style="color:#8957a5;">🔍 Symptoms</h3>
                <ul style="color:#3a2c42;">
                    <li>Blurred vision in one eye</li>
                    <li>Frequent eye strain and headaches</li>
                    <li>Poor depth perception</li>
                    <li>Frequent eye rubbing</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    
    with colB:
        st.markdown("""
            <div class="metric-card" style="text-align:left;">
                <h3 style="color:#8957a5;">⚡ Causes</h3>
                <ul style="color:#3a2c42;">
                    <li>Strabismus (eye misalignment)</li>
                    <li>Refractive errors</li>
                    <li>Family history</li>
                    <li>Premature birth</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    
    with colC:
        st.markdown("""
            <div class="metric-card" style="text-align:left;">
                <h3 style="color:#8957a5;">💊 Treatment</h3>
                <ul style="color:#3a2c42;">
                    <li>Eye patching therapy</li>
                    <li>Corrective glasses</li>
                    <li>Vision therapy</li>
                    <li>Early detection is key</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Model performance metrics
    st.markdown("<h2 style='text-align:center;'>📊 Model Performance</h2>", unsafe_allow_html=True)
    
    perf_cols = st.columns(4)
    metrics = [
        ("91%", "Accuracy"),
        ("588", "Patient Records"),
        ("100", "Decision Trees"),
        ("10", "Features Used")
    ]
    
    for col, (value, label) in zip(perf_cols, metrics):
        with col:
            st.markdown(f"""
                <div class="about-metric-card">
                    <h2>{value}</h2>
                    <p>{label}</p>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="footer">
            Developed by <b>Prince Joshi</b> | Aspiring Data Analyst
        </div>
    """, unsafe_allow_html=True)

# MAIN PAGE 
def main_page():
    # App header
    st.markdown("""
        <div class="app-title">
            <h1>👁️ Amblyopia Detector</h1>
            <p>Machine Learning based Lazy Eye Detection</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Welcome greeting
    st.markdown("""
        <div class="welcome-message">
            <h3>🌟 Welcome to the Amblyopia Detection System</h3>
            <p>Early detection of Amblyopia (Lazy Eye) using advanced Machine Learning algorithms</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Sidebar inputs
    with st.sidebar:
        st.markdown("<h2 style='text-align:center;'>🧾 Patient Details</h2>", unsafe_allow_html=True)
        st.markdown("---")
        
        reset_key = f"reset_{st.session_state.reset_trigger}"
        
        age = st.number_input("Age of Patient", min_value=2, max_value=10, value=5, key=f"age_{reset_key}", help="Patient age between 2 to 10 years")
        va_left = st.number_input("Visual Acuity (Left Eye)", min_value=0.0, max_value=1.0, value=0.4, step=0.05, key=f"va_left_{reset_key}", help="1.0 = Perfect vision, 0.0 = No vision")
        va_right = st.number_input("Visual Acuity (Right Eye)", min_value=0.0, max_value=1.0, value=0.4, step=0.05, key=f"va_right_{reset_key}", help="1.0 = Perfect vision, 0.0 = No vision")
        refractive_error = st.number_input("Refractive Error", min_value=0.0, max_value=5.0, value=1.2, step=0.1, key=f"refractive_{reset_key}", help="Higher value means more refractive error")
        ocular_alignment = st.selectbox("Ocular Alignment", ["Normal", "Misaligned"], key=f"ocular_{reset_key}")
        vision_result = st.selectbox("Vision Screening Result", ["Pass", "Refer", "Fail"], key=f"vision_{reset_key}")
        strabismus = st.selectbox("Strabismus Present?", ["No", "Yes"], key=f"strabismus_{reset_key}")
        family_history = st.selectbox("Family History?", ["No", "Yes"], key=f"family_{reset_key}")
        premature_birth = st.selectbox("Premature Birth?", ["No", "Yes"], key=f"premature_{reset_key}")
        eye_patch = st.selectbox("Eye Patching Treatment?", ["No", "Yes"], key=f"patch_{reset_key}")
        
        st.markdown("---")
        
        if st.button("🔄 Reset All Fields", use_container_width=True):
            st.session_state.reset_trigger += 1
            st.rerun()
    
    # About page navigation button
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        if st.button("📖 About Amblyopia", use_container_width=True):
            st.session_state.page = 'about'
            st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Brief info cards
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
            <div class="custom-info">
                <b>👁️ What is Amblyopia?</b><br>
                Also known as Lazy Eye — a vision disorder where one eye is weaker than the other.
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
            <div class="custom-info">
                <b>🤖 How it works?</b><br>
                Fill patient details in the sidebar and click Predict to get instant results using Random Forest (91% accuracy).
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Convert user inputs to model-compatible format
    # Ocular Alignment: Misaligned=0, Normal=1
    ocular_alignment_enc = 1 if ocular_alignment == "Normal" else 0
    
    # Vision Screening Result: alphabetical order = Fail, Pass, Refer
    # So: Fail=0, Pass=1, Refer=2
    if vision_result == "Fail":
        vision_result_enc = 0
    elif vision_result == "Pass":
        vision_result_enc = 1
    else:
        vision_result_enc = 2
    
    # Binary fields: No=0, Yes=1
    strabismus_enc = 1 if strabismus == "Yes" else 0
    family_history_enc = 1 if family_history == "Yes" else 0
    premature_birth_enc = 1 if premature_birth == "Yes" else 0
    eye_patch_enc = 1 if eye_patch == "Yes" else 0
    
    # Final feature array in the order model expects
    input_data = np.array([[age, va_left, va_right, strabismus_enc, family_history_enc,
                            premature_birth_enc, eye_patch_enc, vision_result_enc,
                            refractive_error, ocular_alignment_enc]])
    
    # Prediction button
    if st.button("🔍 Predict Amblyopia", use_container_width=True):
        prediction = model.predict(input_data)[0]
        confidence = model.predict_proba(input_data)[0]
        confidence_score = round(max(confidence) * 100, 2)
        
        # Confidence specifically for Amblyopic class
        amblyopic_confidence = round(confidence[1] * 100, 2)
        
        # Determine risk level (only relevant if prediction is Amblyopic)
        if prediction == 1:
            if amblyopic_confidence >= 85:
                risk_html = '<span class="risk-high">🔴 High Risk</span>'
            elif amblyopic_confidence >= 70:
                risk_html = '<span class="risk-medium">🟠 Medium Risk</span>'
            else:
                risk_html = '<span class="risk-low">🟢 Low Risk</span>'
        else:
            risk_html = '<span class="risk-low">🟢 Low Risk (Not Amblyopic)</span>'
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Patient summary section
        st.markdown("<h2 style='text-align:center;'>🧾 Patient Summary</h2>", unsafe_allow_html=True)
        
        sum_cols = st.columns(5)
        summary_data = [
            ("Age", f"{age} yrs"),
            ("VA Left", f"{va_left}"),
            ("VA Right", f"{va_right}"),
            ("Strabismus", strabismus),
            ("Family History", family_history)
        ]
        
        for col, (label, value) in zip(sum_cols, summary_data):
            with col:
                st.markdown(f"""
                    <div class="summary-card">
                        <b>{label}</b>
                        <span>{value}</span>
                    </div>
                """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Show confidence and risk
        st.markdown(f"""
            <h3 style='text-align:center; color:#3a2c42;'>
                🎯 Model Confidence: <b style='color:#8957a5;'>{confidence_score}%</b>
                <br><br>
                Risk Level: {risk_html}
            </h3>
        """, unsafe_allow_html=True)
        
        st.progress(int(confidence_score))
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Final result message
        if prediction == 1:
            st.markdown("""
                <div class="result-error">
                    <h2 style='color:#c62828;'>⚠️ Amblyopic Detected</h2>
                    <p style='color:#3a2c42; font-size:16px;'>The patient is predicted to be <b>Amblyopic (Lazy Eye)</b>.</p>
                    <p style='color:#3a2c42;'>Please consult an <b>Ophthalmologist</b> immediately for further diagnosis and treatment.</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div class="result-success">
                    <h2 style='color:#2e7d32;'>✅ Not Amblyopic</h2>
                    <p style='color:#3a2c42; font-size:16px;'>The patient is predicted to be <b>Not Amblyopic</b>.</p>
                    <p style='color:#3a2c42;'>No immediate action required. Regular eye checkups are still recommended.</p>
                </div>
            """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
        <div class="footer">
            Developed by <b>Prince Joshi</b> | Aspiring Data Analyst
        </div>
    """, unsafe_allow_html=True)

# PAGE ROUTING
if st.session_state.page == 'main':
    main_page()
else:
    about_page()