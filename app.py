import streamlit as st
import pickle
import numpy as np
import warnings
import gzip
import os
from pathlib import Path
warnings.filterwarnings("ignore")

# ── ASCII Art Styling ──────────────────────────────────────────────────────────
ASCII_ART = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                     🛍️  PURCHASE PREDICTOR  🛍️               ║
    ║              Random Forest · Shopping Behaviour AI            ║
    ╚══════════════════════════════════════════════════════════════╝
"""

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="🛍️ Purchase Amount Predictor",
    page_icon="🛍️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS with PERFECT Background ─────────────────────────────────────────
st.markdown("""
<style>
/* Import fonts */
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=DM+Sans:wght@400;500&family=Fira+Code:wght@400;600&display=swap');

/* Fix Streamlit default white background */
.stApp {
    background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    min-height: 100vh;
}

/* Main container background fix */
.main > div {
    background: transparent !important;
}

/* Block container styling */
.block-container {
    background: transparent !important;
    padding-top: 2rem !important;
}

/* All text colors */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: #e6e6fa !important;
}

/* Title styling */
h1 {
    font-family: 'Fira Code', monospace !important;
    background: linear-gradient(135deg, #e2c97e, #f0a500);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-align: center;
    font-size: 2.5rem !important;
    font-weight: 700 !important;
    letter-spacing: 2px;
    margin-bottom: 0.5rem !important;
}

/* Subtitle */
.subtitle {
    text-align: center;
    color: #a8b2d8;
    font-family: 'Fira Code', monospace;
    font-size: 0.8rem;
    letter-spacing: 3px;
    margin-bottom: 2rem;
    border-bottom: 1px solid rgba(226,201,126,0.3);
    display: inline-block;
    padding-bottom: 0.5rem;
}

/* Cards with glass morphism */
.card {
    background: rgba(15, 12, 41, 0.6);
    border: 1px solid rgba(226,201,126,0.25);
    border-radius: 20px;
    padding: 1.5rem 2rem;
    margin-bottom: 1.2rem;
    backdrop-filter: blur(12px);
    box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    transition: transform 0.3s ease;
}

.card:hover {
    transform: translateY(-5px);
    border-color: rgba(226,201,126,0.5);
}

/* Result box */
.result-box {
    background: linear-gradient(135deg, rgba(226,201,126,0.15), rgba(240,165,0,0.15));
    border: 2px solid #e2c97e;
    border-radius: 25px;
    padding: 2rem;
    text-align: center;
    margin-top: 1.5rem;
    backdrop-filter: blur(10px);
    animation: glow 2s ease-in-out infinite alternate;
}

@keyframes glow {
    from {
        box-shadow: 0 0 10px rgba(226,201,126,0.3);
    }
    to {
        box-shadow: 0 0 20px rgba(226,201,126,0.6);
    }
}

.result-amount {
    font-family: 'Fira Code', monospace;
    font-size: 3.5rem;
    background: linear-gradient(135deg, #e2c97e, #f0a500);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1;
    font-weight: bold;
}

.result-label {
    color: #a8b2d8;
    font-size: 0.85rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-top: 0.5rem;
}

/* Input fields */
.stSelectbox > div > div, .stNumberInput > div > div {
    background: rgba(15, 12, 41, 0.8) !important;
    border: 1px solid rgba(226,201,126,0.3) !important;
    border-radius: 12px !important;
    color: #e6e6fa !important;
}

.stSelectbox label, .stSlider label, .stNumberInput label {
    color: #e2c97e !important;
    font-size: 0.8rem !important;
    text-transform: uppercase;
    letter-spacing: 2px;
    font-weight: 500 !important;
}

/* Slider styling */
.stSlider > div > div > div {
    background-color: #e2c97e !important;
}

/* Button styling */
.stButton > button {
    background: linear-gradient(135deg, #e2c97e, #f0a500) !important;
    color: #0f0c29 !important;
    font-family: 'Fira Code', monospace !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    border: none !important;
    border-radius: 15px !important;
    padding: 0.85rem 2rem !important;
    width: 100%;
    letter-spacing: 2px;
    transition: all 0.3s ease !important;
    text-transform: uppercase;
}

.stButton > button:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 30px rgba(226,201,126,0.5) !important;
    letter-spacing: 3px;
}

/* Social links styling */
.social-links {
    text-align: center;
    margin-top: 2rem;
    padding: 1rem;
    border-top: 1px solid rgba(226,201,126,0.2);
}

.social-btn {
    display: inline-block;
    margin: 0 10px;
    padding: 8px 20px;
    background: rgba(226,201,126,0.1);
    border: 1px solid rgba(226,201,126,0.3);
    border-radius: 30px;
    color: #e2c97e;
    text-decoration: none;
    font-family: 'Fira Code', monospace;
    font-size: 0.85rem;
    transition: all 0.3s ease;
}

.social-btn:hover {
    background: rgba(226,201,126,0.2);
    border-color: #e2c97e;
    transform: translateY(-2px);
    letter-spacing: 1px;
}

/* ASCII art styling */
.ascii-container {
    text-align: center;
    margin-bottom: 1rem;
}

.ascii-art {
    font-family: 'Fira Code', monospace;
    font-size: 0.7rem;
    color: #e2c97e;
    white-space: pre;
    display: inline-block;
    text-shadow: 0 0 10px rgba(226,201,126,0.3);
    line-height: 1.2;
}

/* Hide Streamlit branding */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }

/* Scrollbar styling */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}
::-webkit-scrollbar-track {
    background: #0f0c29;
}
::-webkit-scrollbar-thumb {
    background: #e2c97e;
    border-radius: 10px;
}
::-webkit-scrollbar-thumb:hover {
    background: #f0a500;
}
</style>
""", unsafe_allow_html=True)

# ── Display ASCII Art ──────────────────────────────────────────────────────────
st.markdown(f"""
<div class='ascii-container'>
    <pre class='ascii-art'>
{ASCII_ART}
    </pre>
</div>
""", unsafe_allow_html=True)

# ── Load Model with File Detection ────────────────────────────────────────────────
@st.cache_resource
def find_and_load_model():
    """Automatically find and load model file from various locations."""
    
    # List all possible model filenames
    possible_filenames = [
        "model.pkl.gz",
        "model.pkl",
        "1776502619820_model__3_.pkl",
        "1776502619820_model__3_.pkl.gz",
        "purchase_model.pkl",
        "random_forest_model.pkl",
        "shopping_model.pkl.gz"
    ]
    
    # List all possible directories to check
    directories_to_check = [
        ".",  # Current directory
        "./models",
        "./model",
        "../models",
        str(Path.home() / "Downloads"),  # Downloads folder
        str(Path.home() / "Desktop"),    # Desktop folder
    ]
    
    found_files = []
    
    # Search for model files
    for directory in directories_to_check:
        if os.path.exists(directory):
            for filename in possible_filenames:
                filepath = os.path.join(directory, filename)
                if os.path.exists(filepath):
                    found_files.append(filepath)
    
    # Also search for any .pkl or .pkl.gz files in current directory
    for file in os.listdir("."):
        if file.endswith((".pkl", ".pkl.gz")) and "model" in file.lower():
            if os.path.join(".", file) not in found_files:
                found_files.append(os.path.join(".", file))
    
    # Try to load each found file
    for filepath in found_files:
        try:
            if filepath.endswith('.gz'):
                with gzip.open(filepath, "rb") as f:
                    model = pickle.load(f)
            else:
                with open(filepath, "rb") as f:
                    model = pickle.load(f)
            
            # Success! Return the model and file info
            return model, filepath
        except Exception as e:
            continue
    
    # If no model found, return None
    return None, None

# Load the model
model, model_path = find_and_load_model()

# ── Display Model Status ──────────────────────────────────────────────────────
if model is not None:
    st.success(f"✅ Model loaded successfully from: `{model_path}`")
    
    # Try to get model info
    try:
        if hasattr(model, 'n_estimators'):
            st.info(f"📊 Model: Random Forest with {model.n_estimators} trees")
        elif hasattr(model, 'best_estimator_'):
            st.info(f"📊 Model: {type(model).__name__} (Optimized)")
        else:
            st.info(f"📊 Model Type: {type(model).__name__}")
    except:
        pass
else:
    st.error("""
    ❌ **No model file found!**
    
    **Please upload your model file using the file uploader below:**
    """)
    
    # File uploader as fallback
    uploaded_file = st.file_uploader(
        "Upload your model file (.pkl or .pkl.gz)", 
        type=['pkl', 'gz']
    )
    
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.gz'):
                model = pickle.load(gzip.open(uploaded_file, 'rb'))
            else:
                model = pickle.load(uploaded_file)
            st.success("✅ Model loaded successfully from upload!")
            model_path = "uploaded_file"
        except Exception as e:
            st.error(f"❌ Failed to load uploaded model: {e}")
    
    st.info("""
    **Troubleshooting tips:**
    1. Make sure your model file is in the same folder as this app
    2. Check the file name (expected: `model.pkl.gz` or similar)
    3. Or use the file uploader above to upload your model
    """)
    
    # Show current directory contents
    st.markdown("### 📁 Files in current directory:")
    try:
        files = os.listdir(".")
        pkl_files = [f for f in files if f.endswith(('.pkl', '.pkl.gz'))]
        if pkl_files:
            for f in pkl_files:
                st.code(f"📄 {f}")
        else:
            st.code("No .pkl or .pkl.gz files found")
    except:
        pass
    
    st.stop()

# ── Feature Options ───────────────────────────────────────────────────────────
GENDER_OPTIONS       = ["Male", "Female"]
ITEM_OPTIONS         = ["Blouse","Sweater","Jeans","Sandals","Sneakers","Shirt","Shorts",
                        "Coat","Handbag","Shoes","Dress","Skirt","Sunglasses","Pants",
                        "Jacket","Gloves","Belt","Boots","Scarf","Hat","Socks","Jewelry",
                        "Backpack","T-shirt","Hoodie","Leggings"]
CATEGORY_OPTIONS     = ["Clothing","Footwear","Outerwear","Accessories"]
LOCATION_OPTIONS     = sorted(["Kentucky","Maine","Massachusetts","Rhode Island","Oregon","Wyoming",
                        "Montana","Louisiana","West Virginia","Missouri","Arkansas","Hawaii",
                        "Delaware","New Hampshire","New York","Alabama","Mississippi","North Dakota",
                        "Oklahoma","South Dakota","New Mexico","Iowa","Vermont","Arizona","Texas",
                        "Virginia","Tennessee","New Jersey","Nevada","Ohio","Idaho","California",
                        "Michigan","Wisconsin","Georgia","Nebraska","North Carolina","Washington",
                        "Utah","Maryland","Colorado","Pennsylvania","Alaska","Connecticut",
                        "Indiana","Minnesota","Florida","Kansas","South Carolina","Illinois"])
SIZE_OPTIONS         = ["XS","S","M","L","XL"]
COLOR_OPTIONS        = ["Turquoise","White","Charcoal","Silver","Lavender","Teal","Olive",
                        "Indigo","Peach","Gold","Green","Maroon","Pink","Terra Cotta",
                        "Black","Brown","Violet","Beige","Blue","Red","Orange","Yellow",
                        "Purple","Cyan","Magenta","Gray"]
SEASON_OPTIONS       = ["Winter","Spring","Summer","Fall"]
SUBSCRIPTION_OPTIONS = ["Yes","No"]
SHIPPING_OPTIONS     = ["Free Shipping","Express","Standard","Next Day Air","Store Pickup","2-Day Shipping"]
DISCOUNT_OPTIONS     = ["Yes","No"]
PAYMENT_OPTIONS      = ["Credit Card","Venmo","Cash","PayPal","Debit Card","Bank Transfer"]
FREQUENCY_OPTIONS    = ["Weekly","Fortnightly","Bi-Weekly","Monthly","Every 3 Months","Quarterly","Annually"]

def encode(val, options):
    """Encode categorical value to its index."""
    try:
        return options.index(val)
    except ValueError:
        return 0

# ── Main Title ────────────────────────────────────────────────────────────────
st.markdown("<h1>⚡ PURCHASE AMOUNT PREDICTOR ⚡</h1>", unsafe_allow_html=True)
st.markdown("<div style='text-align: center;'><div class='subtitle'>RANDOM FOREST · SHOPPING BEHAVIOUR AI</div></div>", unsafe_allow_html=True)

# ── Input Form ────────────────────────────────────────────────────────────────
with st.container():
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### 👤 CUSTOMER PROFILE")
    col1, col2, col3 = st.columns(3)
    with col1:
        age = st.number_input("Age", min_value=18, max_value=80, value=30, step=1)
    with col2:
        gender = st.selectbox("Gender", GENDER_OPTIONS)
    with col3:
        previous_purchases = st.number_input("Previous Purchases", min_value=0, max_value=100, value=5, step=1)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### 🛒 PRODUCT DETAILS")
    col1, col2 = st.columns(2)
    with col1:
        item = st.selectbox("Item Purchased", ITEM_OPTIONS)
        category = st.selectbox("Category", CATEGORY_OPTIONS)
        color = st.selectbox("Color", COLOR_OPTIONS)
    with col2:
        size = st.selectbox("Size", SIZE_OPTIONS)
        season = st.selectbox("Season", SEASON_OPTIONS)
        review_rating = st.slider("Review Rating", 1.0, 5.0, 3.5, 0.1)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### 📦 TRANSACTION DETAILS")
    col1, col2 = st.columns(2)
    with col1:
        location = st.selectbox("Location (State)", LOCATION_OPTIONS)
        shipping = st.selectbox("Shipping Type", SHIPPING_OPTIONS)
        subscription = st.selectbox("Subscription Status", SUBSCRIPTION_OPTIONS)
    with col2:
        discount = st.selectbox("Discount Applied", DISCOUNT_OPTIONS)
        payment = st.selectbox("Payment Method", PAYMENT_OPTIONS)
        frequency = st.selectbox("Frequency of Purchases", FREQUENCY_OPTIONS)
    st.markdown("</div>", unsafe_allow_html=True)

# ── Predict Button ────────────────────────────────────────────────────────────
if st.button("✨ PREDICT PURCHASE AMOUNT ✨", type="primary", use_container_width=True):
    if model is not None:
        features = np.array([[
            float(age),
            float(encode(gender, GENDER_OPTIONS)),
            float(encode(item, ITEM_OPTIONS)),
            float(encode(category, CATEGORY_OPTIONS)),
            float(encode(location, LOCATION_OPTIONS)),
            float(encode(size, SIZE_OPTIONS)),
            float(encode(color, COLOR_OPTIONS)),
            float(encode(season, SEASON_OPTIONS)),
            float(review_rating),
            float(encode(subscription, SUBSCRIPTION_OPTIONS)),
            float(encode(shipping, SHIPPING_OPTIONS)),
            float(encode(discount, DISCOUNT_OPTIONS)),
            float(previous_purchases),
            float(encode(payment, PAYMENT_OPTIONS)),
            float(encode(frequency, FREQUENCY_OPTIONS)),
        ]])
        
        try:
            prediction = model.predict(features)[0]
            
            st.markdown(f"""
            <div class='result-box'>
                <div class='result-label'>══ PREDICTED PURCHASE AMOUNT ══</div>
                <div class='result-amount'>${prediction:,.2f}</div>
                <div class='result-label'>Random Forest Regressor</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.balloons()
            
        except Exception as e:
            st.error(f"❌ Prediction failed: {str(e)}")
            st.info("The model might expect different feature names or format. Check model training details.")
    else:
        st.error("❌ No model loaded. Please upload a model file first.")

# ── Social Links & Footer ─────────────────────────────────────────────────────
st.markdown("""
<div class='social-links'>
    <a href='https://linkedin.com/in/YOUR_USERNAME' target='_blank' class='social-btn'>
        🔗 LinkedIn
    </a>
    <a href='https://github.com/YOUR_USERNAME' target='_blank' class='social-btn'>
        🐙 GitHub
    </a>
    <a href='https://twitter.com/YOUR_USERNAME' target='_blank' class='social-btn'>
        🐦 Twitter
    </a>
</div>
""", unsafe_allow_html=True)

# Footer with ASCII style
st.markdown("""
<div style='text-align: center; margin-top: 2rem; padding: 1rem;'>
    <pre style='font-family: "Fira Code", monospace; font-size: 0.7rem; color: #e2c97e; opacity: 0.6;'>
    ════════════════════════════════════════════════════════════════
    🛍️  AI-Powered Shopping Predictor | Built with Streamlit  🛍️
    ════════════════════════════════════════════════════════════════
    </pre>
</div>
""", unsafe_allow_html=True)
