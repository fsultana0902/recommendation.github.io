import streamlit as st
import pickle
import pandas as pd
import requests
import base64


def add_background(image):
    with open(image, "rb") as image:
        encoded_string = base64.b64encode(image.read())
    st.markdown(
        f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"jpeg"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
        unsafe_allow_html=True
    )


add_background('img.jpeg')


def get_poster(movie_id):
    d = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=04aecb59aee36e1d70fa29ee12151ad9&language=en-US'.format(
            movie_id))
    details = d.json()
    return "http://image.tmdb.org/t/p/w500" + details['poster_path']


def recommend(movie):
    index_of_movie = movies[movies.title == movie]['index'].values[0]
    s = similarity[index_of_movie]
    movies_list = sorted(list(enumerate(s)), reverse=True, key=lambda x: x[1])[1:7]
    rec_movies = []
    movie_posters = []
    for i in movies_list:
        mov_id = movies.iloc[i[0]].id
        rec_movies.append(movies.iloc[i[0]].title)
        movie_posters.append(get_poster(mov_id))
    return rec_movies, movie_posters


movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('sim.pkl', 'rb'))
st.title('Movie Recommendation Engine')
movie_selected = st.selectbox(
    'Select a movie to watch?',
    movies['title'].values)
if st.button('Recommend'):
    movie_names, posters = recommend(movie_selected)
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1:
        st.text(movie_names[0])
        st.image(posters[0])
    with col2:
        st.text(movie_names[1])
        st.image(posters[1])

    with col3:
        st.text(movie_names[2])
        st.image(posters[2])
    with col4:
        st.text(movie_names[3])
        st.image(posters[3])
    with col5:
        st.text(movie_names[4])
        st.image(posters[4])
    with col6:
        st.text(movie_names[5])
        st.image(posters[5])
