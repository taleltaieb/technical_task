# streamlit_app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# Setup
st.set_page_config(page_title="Airbus Library Selection", layout="wide", page_icon="📚")
st.title("📚 Airbus Library Book Selection Dashboard")
st.markdown("This dashboard showcases the data-driven selection of diverse, high-impact books based on scoring logic, diversity quotas, and pricing strategy.")

# Load data
@st.cache_data
def load_data():
    full_df = pd.read_csv("BOOKS_DATASET_final.csv")
    final_df = pd.read_csv("selection_books.csv")
    return full_df, final_df

full_df, final_df = load_data()

# Tabs for full dataset and final selection
tab1, tab2 = st.tabs(["📊 Full Dataset Overview", "🎯 Final 5,000 Selection"])

# TAB 1 - FULL DATA
with tab1:
    st.header("📊 Full Dataset (Filtered & Scored)")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Books", f"{len(full_df):,}")
    col2.metric("Avg. Score", f"{full_df['score_final'].mean():.2f}")
    col3.metric("Avg. Price (€)", f"{full_df['sale price'].mean():.2f}")
    col4.metric("Total Budget (€)", f"{full_df['sale price'].sum():,.0f}")

    fig_score = px.histogram(full_df, x="score_final", nbins=30, title="Book Score Distribution", color_discrete_sequence=["#1f77b4"])
    fig_score.update_layout(template="plotly_dark")
    st.plotly_chart(fig_score, use_container_width=True, key="score_chart_1")

    top_genres = full_df["main_genre"].value_counts().nlargest(15).reset_index()
    top_genres.columns = ["Genre", "Count"]
    fig_genres = px.bar(top_genres, x="Genre", y="Count", title="Top 15 Genres", color="Count", color_continuous_scale="Viridis")
    fig_genres.update_layout(template="plotly_dark")
    st.plotly_chart(fig_genres, use_container_width=True, key="genres_chart_1")

    top_nats = full_df["author_nationality"].value_counts().nlargest(15).reset_index()
    top_nats.columns = ["Nationality", "Count"]
    fig_nats = px.bar(top_nats, x="Nationality", y="Count", title="Top 15 Author Nationalities", color="Count", color_continuous_scale="Plasma")
    fig_nats.update_layout(template="plotly_dark")
    st.plotly_chart(fig_nats, use_container_width=True, key="nats_chart_1")

    age_group_counts = full_df["age_group"].value_counts().reset_index()
    age_group_counts.columns = ["Age Group", "Count"]

    fig_age = px.bar(
        age_group_counts,
        x="Age Group",
        y="Count",
        title="Age Group Distribution",
        color="Count",
        color_continuous_scale="Inferno"
    )
    fig_age.update_layout(template="plotly_dark")
    st.plotly_chart(fig_age, use_container_width=True, key="age_group_chart_1")

    fig_price = px.histogram(full_df, x="sale price", nbins=30, title="Price Distribution (€)", color_discrete_sequence=["#FF7F0E"])
    fig_price.update_layout(template="plotly_dark")
    st.plotly_chart(fig_price, use_container_width=True, key="price_chart_1")

    st.markdown("### 🏆 Top 20 Books by Score")
    top_books = full_df.sort_values("score_final", ascending=False).head(20)
    st.dataframe(top_books[["title", "authors", "main_genre", "average_rating", "ratings_count", "sale price", "score_final"]], use_container_width=True)
    st.markdown("### 📈 Score Final vs Année de Publication")

    plt.figure(figsize=(12, 6))
    
    sns.scatterplot(data=full_df, x="original_publication_year", y="score_final", hue="age_group", palette="Set2", alpha=0.8, s=100, edgecolor='w', linewidth=1.5)

    plt.title("Score Final vs Année de Publication", fontsize=16, fontweight='bold', color="darkblue")
    plt.xlabel("Année de Publication", fontsize=12, fontweight='bold')
    plt.ylabel("Score Final", fontsize=12, fontweight='bold')

    plt.legend(title="Groupe d'âge", fontsize=12, title_fontsize='13', loc='upper left', frameon=True, shadow=True, borderpad=1)

    plt.gca().set_facecolor('lightgray')

    plt.grid(True, which='both', linestyle='--', linewidth=0.5)

    st.pyplot(plt)  

    st.download_button("📥 Download Full Dataset (CSV)", data=full_df.to_csv(index=False).encode("utf-8"), file_name="BOOKS_DATASET.csv")

# TAB 2 - FINAL SELECTION
with tab2:
    st.header("🎯 Final Selection (Top 5,000 with Diversity Quotas)")

    col1, col2, col3 = st.columns(3)
    col1.metric("Selected Books", f"{len(final_df):,}")
    col2.metric("Avg. Score", f"{final_df['score_final'].mean():.2f}")
    col3.metric("Total Budget (€)", f"{final_df['sale price'].sum():,.2f}")

    # Genre chart
    genre_selection = final_df.groupby("main_genre")["sale price"].agg(["count", "sum"]).reset_index().sort_values("count", ascending=False)
    fig_genre_select = px.bar(genre_selection, x="main_genre", y="count", color="sum", color_continuous_scale="Blues", labels={"count": "Book Count", "sum": "Total Price (€)", "main_genre": "Genre"}, title="Top Genres in Final Selection")
    fig_genre_select.update_layout(template="plotly_dark")
    st.plotly_chart(fig_genre_select, use_container_width=True, key="genre_select_chart")

    # Nationality chart
    nat_selection = final_df.groupby("author_nationality")["sale price"].agg(["count", "sum"]).reset_index().sort_values("count", ascending=False)
    fig_nat_select = px.bar(nat_selection.head(10), x="author_nationality", y="count", color="sum", color_continuous_scale="Plasma", title="Top 10 Nationalities in Final Selection")
    fig_nat_select.update_layout(template="plotly_dark")
    st.plotly_chart(fig_nat_select, use_container_width=True, key="nat_select_chart")

    fig_final_score = px.histogram(final_df, x="score_final", nbins=25, title="Score Distribution of Final 5,000 Books", color_discrete_sequence=["#00CC96"])
    fig_final_score.update_layout(template="plotly_dark")
    st.plotly_chart(fig_final_score, use_container_width=True, key="final_score_chart")

    st.download_button("📥 Download Final Book Selection (CSV)", data=final_df.to_csv(index=False).encode("utf-8"), file_name="selection_books.csv")
