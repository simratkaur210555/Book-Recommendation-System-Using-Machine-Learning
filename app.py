import streamlit as st
import pickle
import numpy as np

st.set_page_config(page_title="Book AI", layout="wide")

pt = pickle.load(open('pt.pkl','rb'))
similarity_scores = pickle.load(open('similarity.pkl','rb'))
books = pickle.load(open('books.pkl','rb'))

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white;
}

.title {
    text-align: center;
    font-size: 65px;
    font-weight: 800;
    background: linear-gradient(90deg, #ff8a00, #e52e71);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    color: #dcdcdc;
    margin-bottom: 40px;
}

div[data-baseweb="select"] {
    background-color: rgba(255,255,255,0.08) !important;
    border-radius: 12px !important;
    backdrop-filter: blur(10px);
}

.stButton>button {
    width: 100%;
    height: 55px;
    font-size: 18px;
    font-weight: 600;
    border-radius: 12px;
    border: none;
    color: white;
    background: linear-gradient(90deg, #ff8a00, #e52e71);
    transition: 0.3s;
}

.stButton>button:hover {
    transform: scale(1.05);
}

.card {
    background: rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 18px;
    text-align: center;
    backdrop-filter: blur(14px);
    transition: 0.4s;
}

.card:hover {
    transform: translateY(-12px) scale(1.05);
}

.book-title {
    font-size: 15px;
    font-weight: 700;
    margin-top: 10px;
}

.book-author {
    font-size: 13px;
    color: #bbbbbb;
}

.section-title {
    font-size: 26px;
    margin-top: 40px;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">📚 Book AI Recommender</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Discover books that match your taste instantly</div>', unsafe_allow_html=True)

selected_book = st.selectbox("", pt.index.values)

def recommend(book_name):
    index = np.where(pt.index == book_name)[0][0]
    similar_items = sorted(
        list(enumerate(similarity_scores[index])),
        key=lambda x: x[1],
        reverse=True
    )[1:6]

    data = []
    for i in similar_items:
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        data.append({
            "title": temp_df['Book-Title'].values[0],
            "author": temp_df['Book-Author'].values[0],
            "image": temp_df['Image-URL-M'].values[0]
        })
    return data

if st.button("✨ Recommend"):
    recs = recommend(selected_book)

    st.markdown('<div class="section-title">✨ Recommended Books</div>', unsafe_allow_html=True)

    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.markdown(f"""
            <div class="card">
                <img src="{recs[i]['image']}" width="130">
                <div class="book-title">{recs[i]['title']}</div>
                <div class="book-author">{recs[i]['author']}</div>
            </div>
            """, unsafe_allow_html=True)