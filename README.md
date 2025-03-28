# 📚 Book Data Exploration App – Airbus Data Governance Challenge

This interactive Streamlit app was developed as part of the Airbus Data Management & Governance technical challenge. It demonstrates how public data can be collected, cleaned, enriched, and transformed into valuable insights for decision-makers.

---

## 🚀 Features

- 🔍 **Search and filter** books by genre, rating, price, and title
- 📊 **General insights** on book diversity, publication trends, and pricing
- 🎯 **Filtered KPIs** that respond to user-selected criteria
- 📌 **Summary insights**: Best value genres, top-rated categories, and the current bestseller
- ⚙️ Built with clean, modular code and user-friendly layout
- 🔁 Reset filters at any time with one click

---

## 🧪 Dataset

The dataset was enriched using the **Google Books API**, cleaned to remove missing/irrelevant values, and filtered to include only English-language books with valid metadata. Final columns include:

- `title`, `authors`, `average_rating`, `genre`, `description`, `price`, `page_count`, `publication_date`, and more.

---

## 🛠 Tech Stack

- **Python 3.10+**
- **Streamlit** – for the interactive dashboard
- **Pandas** – for data manipulation
- **Plotly Express** – for advanced interactive visualizations
- **Requests** – to access and enrich data via public APIs

---

## ⚙️ Installation & Run Locally

1. Clone the repo or unzip the folder
2. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   streamlit run app.py
   ```

---

## 👨‍💼 Author

Talel Taieb  
Apprenticeship candidate – Airbus Real Estate  
`taleltaieb@example.com`

---
