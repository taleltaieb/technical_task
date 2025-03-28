import streamlit as st
import pandas as pd
import plotly.express as px
from math import ceil

st.set_page_config(
    page_title="📚 Smart Library Dashboard",
    layout="wide",
    page_icon="📖"
)

@st.cache_data
def load_data():
    df = pd.read_csv("books_enriched_cleaned.csv")
    df = df[df['language_code'].str.startswith('en')]  # Remove non-English books
    return df

df = load_data()





# ---- SIDEBAR ----
st.sidebar.markdown("## 🎯 Filter Your Selection")
if st.sidebar.button("🔁 Reset Filters"):
    for key in st.session_state.keys():
        del st.session_state[key]
        st.session_state.clear()
    
    st.rerun()

top_genres = df['genre'].value_counts().head(30).index.tolist()
genre_options = st.sidebar.multiselect("Select Genres", options=top_genres, default=None, help="Type to search. Leave empty to include all.")
price = st.sidebar.slider("💰 Price Range (EUR)", float(df['price'].min()), float(df['price'].max()), (5.0, 25.0))
rating = st.sidebar.slider("⭐ Rating Range", float(df['average_rating'].min()), float(df['average_rating'].max()), (3.5, 5.0))
min_pages = st.sidebar.slider("📖 Minimum Pages", int(df['num_pages'].min()), int(df['num_pages'].max()), 100)
search_title = st.sidebar.text_input("🔎 Search Book Title (optional)")
max_books = st.sidebar.number_input("Max Books to Display", min_value=10, max_value=1000, value=50)
fast_mode = st.sidebar.checkbox("⚡ Fast Mode (Skip Visuals)", value=False)

# ---- FILTERING ----
filtered_df = df[
    ((df['genre'].isin(genre_options)) if genre_options else True) &
    (df['price'].between(price[0], price[1])) &
    (df['average_rating'].between(rating[0], rating[1])) &
    (df['num_pages'] >= min_pages)
]
if search_title:
    filtered_df = filtered_df[filtered_df['title'].str.contains(search_title, case=False)]
filtered_df = filtered_df.head(int(max_books))

if filtered_df.empty:
    st.warning("⚠️ No books match your current filters. Try adjusting the genre, rating, or price.")
    st.stop()

# ---- HEADER ----
st.title("📚 AI-Powered Library Dashboard")
st.markdown("Empowering smart book selection with data-driven insights for budget, quality, and diversity.")

# ---- FILTER SUMMARY ----
with st.expander("🧾 Current Filters Summary"):
    st.markdown(f"**Genres:** {'All' if not genre_options else ', '.join(genre_options)}")
    st.markdown(f"**Price Range:** €{price[0]} - €{price[1]}")
    st.markdown(f"**Rating Range:** {rating[0]} - {rating[1]}")
    st.markdown(f"**Min Pages:** {min_pages}")
    if search_title:
        st.markdown(f"**Title Search:** {search_title}")
    st.markdown(f"**Max Results:** {max_books}")

# ---- GLOBAL KPIs ----
st.markdown("## 🔵 General Collection KPIs")
gk1, gk2, gk3, gk4 = st.columns(4)
gk1.metric("📘 Total Books", len(df))
gk2.metric("💸 Budget Potential (€)", f"{df['price'].sum():.2f}")
gk3.metric("🧠 Avg. Rating", f"{df['average_rating'].mean():.2f}")
gk4.metric("📖 Avg. Pages", f"{df['num_pages'].mean():.0f}")

# ---- FILTERED KPIs ----
st.markdown("## 🟢 Filtered Data KPIs")
fk1, fk2, fk3, fk4 = st.columns(4)
fk1.metric("📚 Books Selected", len(filtered_df))
fk2.metric("💰 Selection Cost (€)", f"{filtered_df['price'].sum():.2f}")
fk3.metric("📊 Avg. Rating", f"{filtered_df['average_rating'].mean():.2f}")
fk4.metric("📚 Avg. Pages", f"{filtered_df['num_pages'].mean():.0f}")

# ---- SUMMARY INSIGHTS ----
st.markdown("## 📌 Summary Insights")
col1, col2, col3, col4 = st.columns(4)
df_clean = df[~df['genre'].str.lower().isin(['unknown', 'non-classifiable'])]

avg_price_by_genre = df_clean.groupby('genre')['price'].mean().sort_values()
avg_rating_by_genre = df_clean.groupby('genre')['average_rating'].mean().sort_values(ascending=False)
cost_per_rating = df_clean.groupby('genre').apply(lambda x: (x['price'] / x['average_rating']).mean()).sort_values()

col1.metric("📗 Cheapest Genre", avg_price_by_genre.index[0], f"€{avg_price_by_genre.iloc[0]:.2f}")
col2.metric("🌟 Top Rated Genre", avg_rating_by_genre.index[0], f"{avg_rating_by_genre.iloc[0]:.2f}")
col3.metric("💎 Best Value Genre", cost_per_rating.index[0], f"€{cost_per_rating.iloc[0]:.2f} per⭐")

bestseller = df[df['ratings_count'] == df['ratings_count'].max()].iloc[0]
col4.metric("🔥 Bestseller", bestseller['title'], f"{bestseller['ratings_count']} ratings")

# ---- TABS ----
tabs = st.tabs(["📖 Explore Books", "📊 Visual Insights", "📥 Export"])

with tabs[0]:
    st.subheader("📋 Browse Your Books")
    books_per_page = 20
    total_pages = ceil(len(filtered_df) / books_per_page)
    page = st.number_input("Page", min_value=1, max_value=total_pages, value=1)
    paginated_df = filtered_df.iloc[(page - 1) * books_per_page : page * books_per_page]
    st.dataframe(paginated_df[['title', 'authors', 'genre', 'average_rating', 'price', 'num_pages', 'publication_date']], use_container_width=True)

with tabs[1]:
    if not fast_mode:
        st.markdown("### 📘 General Trends (Full Dataset)")
        genre_avg_rating = df_clean.groupby('genre')['average_rating'].mean().sort_values().reset_index().head(15)
        fig1 = px.bar(genre_avg_rating, x='average_rating', y='genre', orientation='h', title="⭐ Top 15 Genres by Avg Rating", text='average_rating', color='average_rating', color_continuous_scale='Blues')
        fig1.update_traces(texttemplate='%{text:.2f}', textposition='outside')
        st.plotly_chart(fig1, use_container_width=True)

        genre_avg_price = df_clean.groupby('genre')['price'].mean().sort_values().reset_index().head(15)
        fig2 = px.bar(genre_avg_price, x='price', y='genre', orientation='h', title="💰 Top 15 Genres by Avg Price", text='price', color='price', color_continuous_scale='Greens')
        fig2.update_traces(texttemplate='€%{text:.2f}', textposition='outside')
        st.plotly_chart(fig2, use_container_width=True)

        st.markdown("### 🟢 Filtered Data Visuals")
        genre_counts = filtered_df['genre'].value_counts().reset_index()
        genre_counts.columns = ['genre', 'count']
        fig3 = px.bar(genre_counts, x='count', y='genre', orientation='h', title='🎨 Genre Distribution (Filtered)', text='count')
        st.plotly_chart(fig3, use_container_width=True)

        fig4 = px.scatter(
            filtered_df, x='price', y='average_rating', color='genre',
            size='num_pages', hover_name='title', size_max=30,
            hover_data=['genre', 'price', 'average_rating'],
            title="💵 Price vs ⭐ Rating (Filtered)")
        st.plotly_chart(fig4, use_container_width=True)

        pub_years_filtered = pd.to_datetime(filtered_df['publication_date'], errors='coerce').dt.year
        pub_trend = pub_years_filtered.value_counts().reset_index()
        pub_trend.columns = ['year', 'count']
        pub_trend = pub_trend.sort_values(by='year')
        fig5 = px.bar(pub_trend, x='year', y='count', title="📅 Books Published Over Time (Filtered)", text='count')
        st.plotly_chart(fig5, use_container_width=True)

with tabs[2]:
    st.subheader("📥 Download Your Current Selection")
    st.download_button(
        label="💾 Download CSV",
        data=filtered_df.to_csv(index=False).encode('utf-8'),
        file_name="selected_books.csv",
        mime="text/csv"
    )

st.markdown("""
---
✅ Created for the Airbus Data Governance Challenge  
👤 By **Talel Taieb** | Clear, focused, and actionable data.
""")
