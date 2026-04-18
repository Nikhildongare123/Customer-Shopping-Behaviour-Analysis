import streamlit as st
import pickle
import numpy as np
import warnings
import gzip
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

/* Background */
.stApp {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    min-height: 100vh;
}

/* Title */
h1 {
    font-family: 'Playfair Display', serif !important;
    color: #e2c97e !important;
    letter-spacing: 1px;
    text-align: center;
}

h3 {
    font-family: 'DM Sans', sans-serif !important;
    color: #a8b2d8 !important;
    font-size: 0.85rem !important;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 0.2rem !important;
}

/* Cards */
.card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(226,201,126,0.2);
    border-radius: 16px;
    padding: 1.5rem 2rem;
    margin-bottom: 1.2rem;
    backdrop-filter: blur(10px);
}

/* Result box */
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

/* Feature importance bar */
.feat-bar-wrap { margin: 0.4rem 0; }
.feat-label {
    color: #c9d1d9;
    font-size: 0.8rem;
    display: flex;
    justify-content: space-between;
    margin-bottom: 3px;
}
.feat-bar-bg {
    background: rgba(255,255,255,0.08);
    border-radius: 4px;
    height: 8px;
    width: 100%;
}
.feat-bar-fill {
    background: linear-gradient(90deg, #e2c97e, #f0a500);
    border-radius: 4px;
    height: 8px;
}

/* Select boxes & sliders */
.stSelectbox label, .stSlider label, .stNumberInput label {
    color: #a8b2d8 !important;
    font-size: 0.82rem !important;
    text-transform: uppercase;
    letter-spacing: 1.5px;
}
.stSelectbox > div > div {
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(226,201,126,0.3) !important;
    border-radius: 10px !important;
    color: #e6edf3 !important;
}

/* Button */
.stButton > button {
    background: linear-gradient(135deg, #e2c97e, #f0a500) !important;
    color: #1a1a2e !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.75rem 2rem !important;
    width: 100%;
    letter-spacing: 1px;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(226,201,126,0.4) !important;
}

/* Divider */
hr { border-color: rgba(226,201,126,0.15) !important; }

/* Hide Streamlit branding */
#MainMenu, footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Load Model ────────────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    with open("model.pkl.gz", "rb") as f:
        return pickle.load(f)

try:
    model = load_model()
    model_loaded = True
except FileNotFoundError:
    model_loaded = False

# ── Feature Options ───────────────────────────────────────────────────────────
GENDER_OPTIONS       = ["Male", "Female"]
ITEM_OPTIONS         = ["Blouse","Sweater","Jeans","Sandals","Sneakers","Shirt","Shorts",
                        "Coat","Handbag","Shoes","Dress","Skirt","Sunglasses","Pants",
                        "Jacket","Gloves","Belt","Boots","Scarf","Hat","Socks","Jewelry",
                        "Backpack","T-shirt","Hoodie","Leggings"]
CATEGORY_OPTIONS     = ["Clothing","Footwear","Outerwear","Accessories"]
LOCATION_OPTIONS     = ["Kentucky","Maine","Massachusetts","Rhode Island","Oregon","Wyoming",
                        "Montana","Louisiana","West Virginia","Missouri","Arkansas","Hawaii",
                        "Delaware","New Hampshire","New York","Alabama","Mississippi","North Dakota",
                        "Oklahoma","South Dakota","New Mexico","Iowa","Vermont","Arizona","Texas",
                        "Virginia","Tennessee","New Jersey","Nevada","Ohio","Idaho","California",
                        "Michigan","Wisconsin","Georgia","Nebraska","North Carolina","Washington",
                        "Utah","Maryland","Colorado","Pennsylvania","Alaska","Connecticut",
                        "Indiana","Minnesota","Florida","Kansas","South Carolina","Illinois"]
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

FEATURE_IMPORTANCES = {
    "Age": 0.1277, "Review Rating": 0.1235, "Gender": 0.1226,
    "Season": 0.1066, "Item Purchased": 0.0846, "Previous Purchases": 0.0786,
    "Color": 0.0669, "Location": 0.0626, "Frequency of Purchases": 0.0511,
    "Payment Method": 0.0424, "Size": 0.0393, "Category": 0.0353,
    "Subscription Status": 0.0223, "Shipping Type": 0.0195, "Discount Applied": 0.0169,
}

# Encode categoricals as label encoding (simple index)
def encode(val, options):
    return options.index(val) if val in options else 0

# ── UI ────────────────────────────────────────────────────────────────────────
st.markdown("<h1>🛍️ Purchase Amount Predictor</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#7b8eb8;margin-top:-0.5rem;margin-bottom:1.5rem;'>Random Forest · Shopping Behaviour Model</p>", unsafe_allow_html=True)

if not model_loaded:
    st.error("⚠️ Model file not found. Place `1776502619820_model__3_.pkl` in the same folder as this app.")
    st.stop()

# ── Input Form ────────────────────────────────────────────────────────────────
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("### 👤 Customer Profile")
col1, col2, col3 = st.columns(3)
with col1:
    age = st.number_input("Age", min_value=18, max_value=80, value=30)
with col2:
    gender = st.selectbox("Gender", GENDER_OPTIONS)
with col3:
    previous_purchases = st.number_input("Previous Purchases", min_value=0, max_value=100, value=5)
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
    location = st.selectbox("Location (State)", sorted(LOCATION_OPTIONS))
    shipping = st.selectbox("Shipping Type", SHIPPING_OPTIONS)
    subscription = st.selectbox("Subscription Status", SUBSCRIPTION_OPTIONS)
with col2:
    discount = st.selectbox("Discount Applied", DISCOUNT_OPTIONS)
    payment = st.selectbox("Payment Method", PAYMENT_OPTIONS)
    frequency = st.selectbox("Frequency of Purchases", FREQUENCY_OPTIONS)
st.markdown("</div>", unsafe_allow_html=True)

# ── Predict ───────────────────────────────────────────────────────────────────
if st.button("✨  Predict Purchase Amount"):
    features = np.array([[
        age,
        encode(gender, GENDER_OPTIONS),
        encode(item, ITEM_OPTIONS),
        encode(category, CATEGORY_OPTIONS),
        encode(location, sorted(LOCATION_OPTIONS)),
        encode(size, SIZE_OPTIONS),
        encode(color, COLOR_OPTIONS),
        encode(season, SEASON_OPTIONS),
        review_rating,
        encode(subscription, SUBSCRIPTION_OPTIONS),
        encode(shipping, SHIPPING_OPTIONS),
        encode(discount, DISCOUNT_OPTIONS),
        previous_purchases,
        encode(payment, PAYMENT_OPTIONS),
        encode(frequency, FREQUENCY_OPTIONS),
    ]])

    prediction = model.predict(features)[0]

    st.markdown(f"""
    <div class='result-box'>
        <div class='result-label'>Predicted Purchase Amount</div>
        <div class='result-amount'>${prediction:.2f}</div>
        <div class='result-label' style='margin-top:0.5rem;font-size:0.75rem;opacity:0.7;'>
            RandomForestRegressor · 100 trees · 15 features
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Feature Importance ────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
with st.expander("📊 Feature Importances", expanded=False):
    max_imp = max(FEATURE_IMPORTANCES.values())
    for feat, imp in FEATURE_IMPORTANCES.items():
        pct = imp * 100
        bar_w = int((imp / max_imp) * 100)
        st.markdown(f"""
        <div class='feat-bar-wrap'>
            <div class='feat-label'><span>{feat}</span><span>{pct:.1f}%</span></div>
            <div class='feat-bar-bg'>
                <div class='feat-bar-fill' style='width:{bar_w}%;'></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
