import streamlit as st
import pickle
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import seaborn as sns

st.set_page_config(
    page_title="YouTube Comment Sentiment Analysis", 
    page_icon="💬",  
)

# Memuat dataset
df = pd.read_csv('./data/predicted_comment_yt.csv')

# Memuat model
nb_model = pickle.load(open('./model/model_nb.pkl', 'rb'))

stopwords_df = pd.read_csv('./data/stopwords.csv', header=None, names=['stopword'])
list_stopwords = stopwords_df['stopword'].tolist()

df['cleaned_comment'] = df['cleaned_comment'].fillna('').astype(str)

# Add custom CSS
st.markdown("""
    <style>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap" rel="stylesheet">

    .subheader {
        color: #ffff; 
        font-family: 'Poppins', sans-serif;
    }
            
    .stDataFrame {
        background-color: #ffffff; 
        border-radius: 15px;
        padding: 10px; 
    }
            
    .stSelectbox div {
        color: #ffff; 
    }
    </style>

""", unsafe_allow_html=True)

# Sidebar menu untuk navigasi
menu = st.sidebar.selectbox(
    'Select an Option', 
    ['🔍Sentiment Analysis', '📊Analysis Overview']
)

# Add About button to sidebar
if st.sidebar.button("ℹ️ About"):
    with st.sidebar.expander("About This App", expanded=True):
        st.write("""
        Aplikasi ini menganalisis komentar YouTube untuk menentukan sentimen mereka—apakah positif, negatif, atau netral. 
        Aplikasi ini dibangun menggunakan model Pemrosesan Bahasa Alami (NLP) yang memprediksi sentimen teks berdasarkan isi komentar.

        **Fitur:**
        - **Analisis Sentimen**: Masukkan komentar YouTube, dan aplikasi akan memprediksi sentimennya.
        - **Gambaran Umum Analisis**: Jelajahi kata-kata paling umum, awan kata, dan kata-kata teratas dalam komentar positif, negatif, dan netral.
        """)
        st.markdown("**Author**: Rheisan Firnandatama")
        st.markdown("**NIM**: 22537141021")

# Fungsi untuk memprediksi sentimen berdasarkan model
def predict_sentiment(text, model):
    if text:
        prediction = model.predict([text])  
        sentiment = prediction[0]
        
        # Menentukan emoji berdasarkan sentimen
        if sentiment == 'positive':
            emoji = '😁' 
        elif sentiment == 'negative':
            emoji = '😡'  
        elif sentiment == 'neutral':
            emoji = '😐'

        # Mengembalikan sentimen dan emoji
        return sentiment, emoji
    return None, None

# Fungsi untuk mendapatkan kata-kata teratas dari komentar
def get_top_n_words(comments_series, n=10):
    all_comments = ' '.join(comments_series.fillna('').astype(str))
    words = [word for word in all_comments.split() if word not in list_stopwords]
    word_count = Counter(words)
    return word_count.most_common(n)

# Fungsi untuk menghasilkan insight berdasarkan visualisasi yang dipilih
def generate_insights(sentiment_option, top_words, visualization_type):
    if visualization_type == 'Word Cloud':
        if sentiment_option == 'All':
            insight = "Kata kunci yang sering muncul dalam komentar akan ditampilkan dalam bentuk awan kata. Kata-kata yang lebih besar menunjukkan frekuensi yang lebih tinggi, mengindikasikan bahwa mereka adalah topik sentral yang dibahas di seluruh sentimen."
        elif sentiment_option == 'Positive':
            insight = "Word Cloud ini menyoroti kata-kata yang paling sering digunakan dalam komentar positif. Kata-kata yang lebih besar menunjukkan topik yang sangat disukai oleh pengguna dengan sentimen positif."
        elif sentiment_option == 'Negative':
            insight = "Word Cloud ini menyoroti kata-kata yang paling sering digunakan dalam komentar negatif. Kata-kata yang lebih besar menunjukkan masalah berulang atau area ketidakpuasan."
        elif sentiment_option == 'Neutral':
            insight = "Word Cloud ini menampilkan kata-kata yang paling sering digunakan dalam komentar netral, menunjukkan topik yang memicu reaksi seimbang dari audiens."

    elif visualization_type == 'Bar Chart':
        if sentiment_option == 'All':
            insight = f"Diagram batang ini menggambarkan kata-kata teratas dari semua komentar, dengan kata-kata seperti '{top_words[0][0]}' dan '{top_words[1][0]}' menjadi yang paling menonjol."
        elif sentiment_option == 'Positive':
            insight = f"Pada diagram batang komentar positif, kata-kata seperti '{top_words[0][0]}' dan '{top_words[1][0]}' menonjol, menunjukkan bahwa kata-kata ini terkait dengan pengalaman positif."
        elif sentiment_option == 'Negative':
            insight = f"Pada diagram batang komentar negatif, kata-kata seperti '{top_words[0][0]}' dan '{top_words[1][0]}' muncul dengan frekuensi tinggi, menyoroti kekhawatiran umum atau area kritik."
        elif sentiment_option == 'Neutral':
            insight = f"Diagram batang komentar netral menunjukkan kata-kata seperti '{top_words[0][0]}' dan '{top_words[1][0]}', mengindikasikan topik yang dibahas secara seimbang."

    elif visualization_type == 'Most Common Words':
        if sentiment_option == 'All':
            insight = "Tabel kata-kata paling umum menampilkan frekuensi kata yang digunakan di semua komentar, memberikan gambaran tentang topik yang paling dibahas."
        elif sentiment_option == 'Positive':
            insight = "Tabel kata-kata paling umum untuk komentar positif menyoroti kata-kata yang sering muncul dalam diskusi yang menguntungkan."
        elif sentiment_option == 'Negative':
            insight = "Tabel kata-kata paling umum untuk komentar negatif mengungkapkan kata-kata yang umum dikaitkan dengan kritik atau umpan balik negatif."
        elif sentiment_option == 'Neutral':
            insight = "Tabel kata-kata paling umum untuk komentar netral menunjukkan kata-kata yang digunakan dalam konteks seimbang tanpa konotasi positif atau negatif yang kuat."

    return insight

if menu == '🔍Sentiment Analysis':
    # Judul Sentiment Analysis
    st.markdown('<h1 class="title">💬 YouTube Comment Sentiment Analysis</h1>', unsafe_allow_html=True)

    # User Input Text
    st.subheader('User Input Text')
    user_input = st.text_area("Enter a comment for analysis:")

    if st.button('Submit'):
        if user_input:
            predicted_sentiment, emoji = predict_sentiment(user_input, nb_model)

            # Display the prediction
            st.subheader('Sentiment Analysis Result')
            st.write(f"Predicted Sentiment for the entered comment: **{predicted_sentiment} {emoji}**")

elif menu == '📊Analysis Overview':
    # Judul Analysis Overview
    st.markdown('<h1 class="title">📊Analysis Overview of YouTube Comments</h1>', unsafe_allow_html=True)

    # Word Cloud Visualization
    st.subheader('Word Cloud of Comments')

    # Sentiment selection dropdown
    sentiment_option = st.selectbox('Select the sentiment you want to analyze', ['All', 'Positive', 'Negative', 'Neutral'])

    # Filter komen berdasarkan sentimen
    if sentiment_option == 'All':
        comments_to_display = df['cleaned_comment']
    else:
        comments_to_display = df[df['predicted_sentiment'] == sentiment_option.lower()]['cleaned_comment']

    # Kombinasi semua comment menjadi single string
    all_comments = ' '.join(comments_to_display)

    # Generate the word cloud
    wordcloud = WordCloud(width=800, height=400,
                        background_color='white',
                        stopwords=list_stopwords,
                        colormap='viridis',
                        random_state=42).generate(all_comments)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(plt)

    # Menampilkan word cloud insight
    wordcloud_insight = generate_insights(sentiment_option, top_words=None, visualization_type='Word Cloud')
    st.write(wordcloud_insight)

    # Top Words berdasarkan Sentiment
    st.subheader('Top Words by Sentiment')

    # Mendapatkan top words
    top_words = get_top_n_words(comments_to_display)

    # Membuat bar chart
    fig, ax = plt.subplots(figsize=(10, 6))

    # Memplot bar chart
    sns.barplot(x=[x[1] for x in top_words], y=[x[0] for x in top_words], ax=ax)
    ax.set_title(f'Top Words in {sentiment_option} Comments')
    ax.set_xlabel('Count')
    ax.set_ylabel('Words')

    # Menampilkan bar chart
    st.pyplot(fig)

    # Menampilkan insight dari bar chart
    barchart_insight = generate_insights(sentiment_option, top_words=top_words, visualization_type='Bar Chart')
    st.write(barchart_insight)

    # Most Common Words
    st.subheader('Most Common Words')
    filtered_words = [word for word in all_comments.split() if word not in list_stopwords]
    word_count = Counter(filtered_words)
    common_words_df = pd.DataFrame(word_count.most_common(20), columns=['Word', 'Frequency'])

    half = len(common_words_df) // 2
    left_column = common_words_df.iloc[:half]
    right_column = common_words_df.iloc[half:]

    # Menaampilkan tabel kata-kata paling umum ke dalam 2 kolom
    col1, col2 = st.columns(2)

    with col1:
        st.dataframe(left_column)

    with col2:
        st.dataframe(right_column)

    # Menampilkan insight dari tabel kata-kata paling umum
    common_words_insight = generate_insights(sentiment_option, top_words=None, visualization_type='Most Common Words')
    st.write(common_words_insight)