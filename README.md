# Customer-Shopping-Behaviour-Analysis
purchase-predictor/
│
├── app.py                 # Main Streamlit application
├── model.pkl.gz          # Trained model file (optional)
├── requirements.txt      # Python dependencies
├── README.md            # Project documentation
│
├── assets/              # Images and assets
│   ├── screenshot.png
│   └── demo.gif
│
├── notebooks/           # Jupyter notebooks for model training
│   └── model_training.ipynb
│
└── data/               # Sample data
    └── sample_customer_data.csv
# 🛍️ Purchase Amount Predictor

<div align="center">

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Random Forest](https://img.shields.io/badge/Random_Forest-FF6B6B?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Machine Learning](https://img.shields.io/badge/Machine_Learning-00ADD8?style=for-the-badge&logo=ai&logoColor=white)

An AI-powered web application that predicts customer purchase amounts based on shopping behavior using Random Forest Regression.

[![Live Demo](https://img.shields.io/badge/Live_Demo-FF4785?style=for-the-badge&logo=streamlit&logoColor=white)](https://your-app-url.streamlit.app)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/yourusername)

</div>

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Demo](#-demo)
- [Installation](#-installation)
- [Usage](#-usage)
- [Model Information](#-model-information)
- [Project Structure](#-project-structure)
- [Technologies Used](#-technologies-used)
- [Contributing](#-contributing)
- [License](#-license)
- [Contact](#-contact)
- [Acknowledgments](#-acknowledgments)

## 🎯 Overview

The **Purchase Amount Predictor** is a sophisticated machine learning application that helps businesses and marketers predict how much a customer is likely to spend based on various factors including:

- Customer demographics (age, gender)
- Product preferences (item type, category, color, size)
- Transaction details (shipping method, payment method, subscription status)
- Behavioral data (previous purchases, purchase frequency, review ratings)

This tool enables data-driven decision making for:
- Personalized marketing campaigns
- Inventory management
- Customer segmentation
- Revenue forecasting

## ✨ Features

### 🎨 Modern UI/UX
- **Glass morphism design** with gradient backgrounds
- **Responsive layout** that works on desktop and tablet
- **Animated elements** with hover effects and glow animations
- **ASCII art styling** for a unique tech aesthetic

### 📊 Comprehensive Input Features
- **15 different features** covering all aspects of customer shopping behavior
- **50+ US states** location selection
- **25+ product types** including clothing, accessories, and footwear
- **20+ color options** for personalized product selection

### 🤖 AI-Powered Predictions
- **Random Forest Regressor** with 100 decision trees
- **Real-time predictions** with instant feedback
- **Confidence indicators** through visual effects
- **Balloon celebration** on successful predictions

### 🔧 Technical Features
- **Automatic model detection** from multiple locations
- **File upload fallback** for custom models
- **Cached model loading** for optimal performance
- **Error handling** with user-friendly messages

## 🎬 Demo

### Application Interface
╔══════════════════════════════════════════════════════════════╗
║ 🛍️ PURCHASE PREDICTOR 🛍️ ║
║ Random Forest · Shopping Behaviour AI ║
╚══════════════════════════════════════════════════════════════
┌─────────────────────────────────────────────────────────────┐
│ 👤 CUSTOMER PROFILE │
│ ┌──────────┬──────────┬──────────────────┐ │
│ │ Age: 30 │ Gender: Male │ Prev Purchases: 5 │ │
│ └──────────┴──────────┴──────────────────┘ │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ 🛒 PRODUCT DETAILS │
│ Item: Shoes | Category: Footwear | Color: Black │
│ Size: M | Season: Summer | Rating: 4.2/5 │
└─────────────────────────────────────────────────────────────┘
✨ PREDICT PURCHASE AMOUNT ✨

══ PREDICTED PURCHASE AMOUNT ══
💰 $127.50 💰
