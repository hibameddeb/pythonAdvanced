import streamlit as st

st.write('Hello World hiba')
x = st.text_input('Favorite Movie?')
st.write(f"Your favorite movie is: {x}")

is_clicked = st.button("Click Me")
if is_clicked:
    st.write("Button clicked!")

rating = st.slider('Rate your favorite movie (1-10)', min_value=1, max_value=10, value=5)
st.write(f"You rated the movie: {rating}/10")

genre = st.selectbox('Select your favorite movie genre', 
                     options=['Action', 'Comedy', 'Drama', 'Horror', 'Romance', 'Sci-Fi'])
st.write(f"Your favorite movie genre is: {genre}")