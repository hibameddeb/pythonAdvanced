import streamlit as st

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Go to", ["Home", "Data Structure", "I/O", "Markdown"])

if page == "Home":
    st.write("## Welcome to the Home Page!")
    st.write("Use the sidebar to navigate to other pages.")

elif page == "Data Structure":
    import pages.datastructure as datastructure
    datastructure.run()

elif page == "I/O":
    import pages.io as io
    io.run()

else:
    import pages.markdown as markdown
    markdown.run()

