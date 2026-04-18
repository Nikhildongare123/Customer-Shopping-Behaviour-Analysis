import streamlit as st
import pickle
import numpy as np
import warnings
import gzip
import pandas as pd
warnings.filterwarnings("ignore")

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="🛍️ Purchase Amount Predictor",
    page_icon="🛍️",
    layout="centered",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=DM+Sans:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    min-height: 100vh;
}

h1 {
    font-family: 'Playfair Display', serif !important;
    color: #e2c97e !important;
    letter-spacing: 1px;
    text-align: center;
}

.card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(226,201,126,0.2);
    border-radius: 16px;
    padding: 1.5rem 2rem;
    margin-bottom: 1.2rem;
    backdrop-filter: blur(10px);
}

.result-box {
    background: linear-gradient(135deg, #e2c97e22, #f0a50022);
    border: 2px solid #e2c97e;
    border-radius: 20px;
    padding: 2rem;
    text-align: center;
    margin-top: 1.5rem;
}
.result-amount {
    font-family: 'Playfair Display', serif;
    font-size: 3.5rem;
    color: #e2c97e;
    line-height: 1;
}
.result-label {
    color: #a8b2d8;
    font-size: 0.9rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: 0.5rem;
}

.stButton > button {
    background: linear-gradient(135deg, #e2c97e, #f0a500) !important;
    color: #1a1a2e !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.75rem 2rem !important;
    width: 100%;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(226,201,126,0.4) !important;
}

/* Fix for select boxes */
.stSelectbox label, .stSlider label, .stNumberInput label {
    color: #a8b2d8 !important;
}
</style>
""", unsafe_allow_html=True)

# ── Load Model ────────────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    """Load the trained model from a gzipped pickle file."""
    try:
        # Try different possible filenames
        possible_files = ["model.pkl.gz", "1776502619820_model__3_.pkl", "model.pkl"]
        
        for filename in possible_files:
            try:
                if filename.endswith('.gz'):
                    with gzip.open(filename, "rb") as f:
                        model = pickle.load(f)
                else:
                    with open(filename, "rb") as f:
                        model = pickle.load(f)
                st.success(f"✅ Model loaded successfully from {filename}")
                return model
            except FileNotFoundError:
                continue
            except Exception as e:
                continue
        
        st.error("❌ No model file found. Please check the model file name.")
        return None
    except Exception as e:
        st.error(f"❌ Model loading failed: {e}")
        return None

# Load the model
model = load_model()

if model is None:
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

# Helper function for encoding categoricals
def encode(val, options):
    """Encode categorical value to its index."""
    try:
        return options.index(val)
    except ValueError:
        return 0

# ── UI Header ────────────────────────────────────────────────────────────────
st.markdown("<h1>🛍️ Purchase Amount Predictor</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#7b8eb8;margin-bottom:1.5rem;'>Random Forest · Shopping Behaviour Model</p>", unsafe_allow_html=True)

# ── Input Form ────────────────────────────────────────────────────────────────
with st.container():
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### 👤 Customer Profile")
    col1, col2, col3 = st.columns(3)
    with col1:
        age = st.number_input("Age", min_value=18, max_value=80, value=30, step=1)
    with col2:
        gender = st.selectbox("Gender", GENDER_OPTIONS)
    with col3:
        previous_purchases = st.number_input("Previous Purchases", min_value=0, max_value=100, value=5, step=1)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### 🛒 Product Details")
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
    st.markdown("### 📦 Transaction Details")
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
if st.button("✨  Predict Purchase Amount", type="primary", use_container_width=True):
    # Prepare features in the correct order
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
        # Make prediction
        prediction = model.predict(features)[0]
        
        # Display result
        st.markdown(f"""
        <div class='result-box'>
            <div class='result-label'>Predicted Purchase Amount</div>
            <div class='result-amount'>${prediction:,.2f}</div>
            <div class='result-label' style='margin-top:0.5rem;font-size:0.75rem;opacity:0.7;'>
                Random Forest Regressor
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Add a small celebration effect
        st.balloons()
        
    except Exception as e:
        st.error(f"❌ Prediction failed: {str(e)}")
        st.info("Please check if the model expects different features or input format.")

# ── Feature Importance (Optional) ────────────────────────────────────────────
with st.expander("ℹ️ About the Model", expanded=False):
    st.markdown("""
    **Model Information:**
    - **Algorithm:** Random Forest Regressor
    - **Features:** 15 customer and product attributes
    - **Target:** Purchase amount in USD
    
    **How to use:**
    1. Fill in customer details
    2. Select product information
    3. Add transaction details
    4. Click "Predict Purchase Amount"
    
    The model will estimate the likely purchase amount based on historical shopping patterns.
    """)
