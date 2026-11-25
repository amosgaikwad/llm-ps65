# Shopping Assistant Bot (PS #65)

An AI-powered e-commerce product recommendation assistant built with **Python**, **Pandas**, **Streamlit**, and **Google Gemini 2.5 Flash**. Users upload or select a product catalog CSV, specify their category, maximum budget, and specific needs, and receive the top 3 tailored product recommendations with clear justifications and trade-offs.

**Student Details:**
- **Name:** Swayam Chavan
- **Roll No:** 65
- **Enrollment Number:** ADT23SOCB1197
- **Class:** AIA 07
- **Problem Statement:** #65 — Shopping Assistant Bot

---

## Problem Statement
Shoppers are often confused by large product catalogs with overlapping technical specifications and price tiers. This application filters a structured product CSV using `pandas` based on budget and category constraints, then sends the top candidate rows to an LLM to recommend the **best 3 products** with clear, need-specific reasons.

---

## Features
- **Deterministic Budget & Category Filtering:** Uses `pandas` to strictly filter items within the user's budget before invoking the LLM, preventing price hallucinations.
- **Custom CSV Support:** Comes preloaded with a sample 25-product catalog (`products.csv`) and supports uploading any custom e-commerce CSV.
- **Grounded AI Reasoning:** Uses Gemini 2.5 Flash to match product specifications directly to the user's natural-language use case while highlighting one honest trade-off per product.
- **Clean Streamlit Interface:** Interactive sidebar controls paired with a live filtered catalog preview and formatted recommendation cards.

---

## Project Structure
```text
llm-ps65-65/
├── app.py              # Main Streamlit web application
├── products.csv        # Sample product catalog dataset (25 items)
├── requirements.txt    # Python dependencies
├── .env.example        # Template for environment variables
├── .gitignore          # Excludes .env, venv/, and cache files
└── README.md           # Project documentation
```

---

## How to Run Locally

### 1. Clone the Repository
```bash
git clone https://github.com/swayamchavan/llm-ps65-65.git
cd llm-ps65-65
```

### 2. Create a Virtual Environment & Install Dependencies
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Configure Your Gemini API Key
Create a `.env` file in the root directory and add your API key from Google AI Studio:
```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
```

### 4. Launch the Streamlit App
```bash
streamlit run app.py
```

---

## Sample Test Inputs
1. **Electronics (Budget: ₹45,000):** *"College coding and light video editing"* → Recommends mid-range Ryzen 5 / Core i5 laptops with 16GB RAM and SSD storage.
2. **Home Appliances (Budget: ₹15,000):** *"Compact kitchen appliances for a bachelor flat"* → Recommends induction cooktops, air fryers, and microwave ovens suited for small spaces.
3. **Audio (Budget: ₹5,000):** *"Long battery life and good mic for online classes"* → Recommends wireless over-ear headphones and ANC earbuds under ₹5,000.