import os
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables from .env
load_dotenv()

st.set_page_config(
    page_title="Shopping Assistant Bot | PS #65",
    page_icon="🛍️",
    layout="wide",
)

# Custom subtle styling for clean product cards
st.markdown(
    """
    <style>
    .rec-card {
        background-color: #f8fafc;
        border: 1px solid #cbd5e1;
        border-left: 5px solid #0f766e;
        border-radius: 6px;
        padding: 16px 20px;
        margin-bottom: 14px;
    }
    .header-banner {
        border-bottom: 2px solid #0f766e;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def get_gemini_client():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None
    return genai.Client(api_key=api_key)


def load_catalog(uploaded_file) -> pd.DataFrame:
    if uploaded_file is not None:
        return pd.read_csv(uploaded_file)
    return pd.read_csv("products.csv")


def generate_recommendations(
    client: genai.Client,
    filtered_df: pd.DataFrame,
    budget: int,
    category: str,
    user_needs: str,
) -> str:
    # Take top 8 candidates sorted by rating to stay concise and relevant
    candidates = filtered_df.sort_values(by="rating", ascending=False).head(8)
    products_table = candidates[
        ["product_id", "name", "brand", "price_inr", "rating", "specs"]
    ].to_markdown(index=False)

    prompt = f"""You are an expert, unbiased e-commerce shopping assistant.
User Budget: INR {budget:,}
Selected Category: {category}
User Specific Needs: "{user_needs}"

Candidate Products (Pre-filtered from Catalog CSV):
{products_table}

Task:
Select the TOP 3 best-matching products strictly from the candidate table above.
If fewer than 3 products exist in the table, recommend all available products in order of fit.

For each recommended product, format your response cleanly using Markdown:
### 1. [Product Name] — INR [Exact Price]
- **Why It Fits Your Needs:** Two concise bullet points linking the product's exact specs directly to "{user_needs}".
- **One Trade-off / Watch-out:** One honest limitation based on the specs or price tier so the buyer makes an informed choice.

Strict Rules:
- Do NOT invent products, prices, ratings, or specifications not present in the table above.
- Keep the tone helpful, objective, and easy to scan.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.3,
        ),
    )
    return response.text


def main():
    st.markdown(
        """
        <div class="header-banner">
            <h1 style="margin:0; color:#0f172a;">🛍️ Shopping Assistant Bot</h1>
            <p style="margin:4px 0 0 0; color:#475569;">
                Smart CSV Product Filtering + Gemini AI Recommendations | <b>Swayam Chavan (Roll No: 65, Class: AIA 07)</b>
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Sidebar Controls
    with st.sidebar:
        st.header("1. Product Catalog")
        uploaded_file = st.file_uploader(
            "Upload custom product CSV (optional)",
            type=["csv"],
            help="Must contain columns: product_id, name, brand, category, price_inr, rating, specs",
        )

        try:
            df = load_catalog(uploaded_file)
        except Exception as e:
            st.error(f"Error reading CSV file: {e}")
            st.stop()

        required_cols = {"product_id", "name", "brand", "category", "price_inr", "rating", "specs"}
        if not required_cols.issubset(set(df.columns)):
            st.error(f"CSV must include columns: {', '.join(sorted(required_cols))}")
            st.stop()

        st.header("2. Budget & Preferences")
        categories = ["All Categories"] + sorted(df["category"].dropna().unique().tolist())
        selected_category = st.selectbox("Product Category", categories)

        min_price = int(df["price_inr"].min())
        max_price = int(df["price_inr"].max())
        default_budget = min(45000, max_price) if max_price >= 45000 else max_price

        max_budget = st.slider(
            "Maximum Budget (INR)",
            min_value=max(500, min_price),
            max_value=max_price,
            value=default_budget,
            step=500,
        )

        user_needs = st.text_area(
            "Describe your needs & use case",
            value="College coding, multitasking, and light video editing with good battery backup",
            height=100,
        )

        recommend_btn = st.button("Find Top 3 Products", type="primary", use_container_width=True)

    # Filter dataframe with Pandas
    filtered_df = df[df["price_inr"] <= max_budget].copy()
    if selected_category != "All Categories":
        filtered_df = filtered_df[filtered_df["category"] == selected_category]

    # Top metrics row
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Catalog Items", len(df))
    col2.metric("Matching Budget & Category", len(filtered_df))
    col3.metric("Max Budget Set", f"INR {max_budget:,}")

    st.subheader("Filtered Product Catalog")
    if filtered_df.empty:
        st.warning(
            f"No products found in **{selected_category}** under **INR {max_budget:,}**. "
            "Try increasing your budget slider in the sidebar."
        )
        st.stop()

    st.dataframe(
        filtered_df.sort_values(by="rating", ascending=False),
        use_container_width=True,
        hide_index=True,
    )

    st.divider()
    st.subheader("AI Top 3 Recommendations")

    if recommend_btn:
        if not user_needs.strip():
            st.warning("Please enter your requirements in the sidebar before generating recommendations.")
            st.stop()

        client = get_gemini_client()
        if client is None:
            st.error(
                "Missing `GEMINI_API_KEY`. Please create a `.env` file with `GEMINI_API_KEY=your_key` "
                "and restart the Streamlit app."
            )
            st.stop()

        with st.spinner("Analyzing specifications and matching top 3 products..."):
            try:
                recommendations_md = generate_recommendations(
                    client=client,
                    filtered_df=filtered_df,
                    budget=max_budget,
                    category=selected_category,
                    user_needs=user_needs.strip(),
                )
                st.markdown('<div class="rec-card">', unsafe_allow_html=True)
                st.markdown(recommendations_md)
                st.markdown("</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Failed to generate recommendations from Gemini API: {e}")
    else:
        st.info("Adjust your category, budget, and needs in the sidebar, then click **Find Top 3 Products**.")


if __name__ == "__main__":
    main()