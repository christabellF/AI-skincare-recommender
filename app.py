import pandas as pd
import streamlit as st
import time

# Page settings
st.set_page_config(page_title="AI Skincare Recommender", page_icon="🧴", layout="centered")

# Load datasets
data = pd.read_csv("data.csv")
products = pd.read_csv("products.csv")

# Title
st.title("🧴 AI-Based Skincare Recommender")
st.write("Get personalized skincare routine based on your skin type, concerns, age, and budget")

# User Inputs
skin_type = st.selectbox("Select your Skin Type", ["oily", "dry", "combination", "sensitive"])
issue = st.selectbox("Select your Skin Concern", ["acne", "dullness", "pigmentation", "dark spots"])
age_group = st.selectbox("Select your Age Group", ["teen", "young_adult", "adult"])
budget = st.selectbox("Select your Budget", ["low", "medium", "high"])

# ICON MAP
icon_map = {
    "cleanser": "🧼",
    "serum": "💧",
    "moisturizer": "🧴",
    "sunscreen": "☀️"
}

# ------------------ INGREDIENT LOGIC ------------------
def get_ingredients(skin_type, issue, product_type):

    if product_type == "cleanser":
        return "salicylic acid" if skin_type == "oily" else "gentle cleanser base"

    elif product_type == "serum":
        return {
            "acne": "niacinamide",
            "dullness": "vitamin c",
            "pigmentation": "alpha arbutin",
            "dark spots": "kojic acid"
        }.get(issue, "active ingredients")

    elif product_type == "moisturizer":
        return "hyaluronic acid + ceramides" if skin_type == "dry" else "light hydration"

    elif product_type == "sunscreen":
        return "broad spectrum SPF"

    return "basic ingredients"

# ------------------ PRODUCT FROM CSV ------------------
def get_product(product_type, skin_type, issue, budget):

    filtered = products[
        (products["product_type"] == product_type) &
        ((products["skin_type"] == skin_type) | (products["skin_type"] == "any")) &
        ((products["issue"] == issue) | (products["issue"] == "any")) &
        (products["budget"] == budget)
    ]

    if not filtered.empty:
        row = filtered.iloc[0]
        return row["product_name"], row["rating"], row["price"], row["link"]

    return "Standard Product", 4.0, "₹--", "#"

# ------------------ SMART RECOMMEND ------------------
def recommend(skin_type, issue, age_group, budget):

    filtered = data[
        (data["skin_type"] == skin_type) &
        (data["issue"] == issue) &
        (data["age_group"] == age_group) &
        (data["budget"] == budget)
    ]

    if filtered.empty:
        filtered = data[
            (data["skin_type"] == skin_type) &
            (data["issue"] == issue) &
            (data["age_group"] == age_group)
        ]
        st.warning("⚠️ Showing closest match (budget adjusted)")

    if filtered.empty:
        filtered = data[
            (data["skin_type"] == skin_type) &
            (data["issue"] == issue)
        ]
        st.warning("⚠️ Showing general recommendations")

    return filtered

# ------------------ BUTTON ------------------
if st.button("✨ Get My Routine"):

    with st.spinner("Analyzing your skin..."):
        time.sleep(1)

    st.success("✨ Your personalized skincare routine is ready!")

    results = recommend(skin_type, issue, age_group, budget)

    if not results.empty:

        st.subheader("🧴 Your Skincare Routine")

        routine_text = ""

        for _, row in results.iterrows():

            product, rating, price, link = get_product(
                row['product_type'], skin_type, issue, budget
            )

            ingredient = get_ingredients(skin_type, issue, row['product_type'])

            # CARD UI
            st.markdown(f"""
            <div style="
                background-color:#f0f4ff;
                padding:15px;
                border-radius:10px;
                margin-bottom:10px;
                box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
            ">
                <h4>{icon_map[row['product_type']]} {row['product_type'].capitalize()}</h4>
                <p><b>Product:</b> {product}</p>
                <p><b>Key Ingredient:</b> {ingredient}</p>
                <p><b>Price:</b> {price}</p>
                <p><b>Rating:</b> ⭐ {rating}/5</p>
                <p><b>How to use:</b> {row['routine']}</p>
                <a href="{link}" target="_blank">🛒 Buy Now</a>
            </div>
            """, unsafe_allow_html=True)

            # Usage
            if row['product_type'] == 'sunscreen':
                st.write("🌞 Use in morning")
            else:
                st.write("🌙 Use morning & night")

            st.write("---")

            routine_text += f"{row['product_type']}: {product} - {price} ⭐{rating}\n"

        # Download
        st.download_button("📄 Download My Routine", routine_text)

        # Confidence
        st.subheader("📊 Recommendation Confidence")
        st.progress(90)

        # AI Explanation
        st.subheader("🤖 Why this recommendation?")
        st.write(f"""
        Based on your **{skin_type} skin**, **{issue} concern**, and **{budget} budget**,  
        this routine is optimized to give effective and affordable skincare results.
        """)

    else:
        st.warning("No recommendation found. Try different options.")

    # Tips
    st.subheader("💡 Skincare Tips")

    tips = {
        "oily": "Use oil-free products and avoid over-cleansing",
        "dry": "Focus on hydration and avoid harsh cleansers",
        "sensitive": "Use gentle and fragrance-free products",
        "combination": "Balance hydration and oil control"
    }

    st.write(f"- {tips.get(skin_type)}")

    # Fun fact
    st.subheader("🧠 Did You Know?")
    st.write("Niacinamide helps reduce acne and improve skin texture!")