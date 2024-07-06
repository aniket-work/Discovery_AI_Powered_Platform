import streamlit as st
from database import init_db
from auth import login_page, signup_page, forgot_password_page
import os
import pandas as pd
from streamlit_option_menu import option_menu

# Initialize the database
init_db()

# Set page config
st.set_page_config(page_title="My Streamlit App", layout="wide")

# Custom CSS for footer and cards
st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stApp {
        display: flex;
        flex-direction: column;
        min-height: 100vh;
    }
    .main {
        flex-grow: 1;
    }
    .custom-footer {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background-color: #f0f2f6;
        padding: 10px;
        text-align: center;
    }
    .space-card {
        padding: 20px;
        border-radius: 5px;
        margin-bottom: 10px;
        background-color: #f0f2f6;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if 'page' not in st.session_state:
    st.session_state.page = 'login'

# Main app logic
if not st.session_state.logged_in:
    if st.session_state.page == 'login':
        login_page()
    elif st.session_state.page == 'signup':
        signup_page()
    elif st.session_state.page == 'forgot_password':
        forgot_password_page()
else:
    # Your existing app code goes here
    st.header("My Streamlit App")

    # Sidebar with icons
    with st.sidebar:
        st.title("Navigation")
        selected = option_menu(
            menu_title=None,
            options=["Profile", "Create Space", "Analyze", "Search", "Settings", "Logout"],
            icons=["person", "plus-square", "graph-up", "search", "gear", "box-arrow-right"],
            default_index=1,
            orientation="vertical",
        )

    if selected == "Logout":
        st.session_state.logged_in = False
        st.session_state.page = 'login'
        st.experimental_rerun()


    # Function to read space info
    def read_space_info(space_path):
        info_file = os.path.join(space_path, "space_info.txt")
        if os.path.exists(info_file):
            with open(info_file, "r") as f:
                lines = f.readlines()
                return {
                    "name": lines[0].strip(),
                    "type": lines[1].strip(),
                    "description": " ".join(lines[2].strip().split()[:5])
                }
        return None


    # Main content
    if selected == "Create Space":
        st.subheader("Create Space")

        # Show existing spaces
        spaces_folder = "spaces"
        existing_spaces = os.listdir(spaces_folder) if os.path.exists(spaces_folder) else []

        st.write("Existing Spaces:")
        cols = st.columns(3)
        for idx, space in enumerate(existing_spaces):
            space_info = read_space_info(os.path.join(spaces_folder, space))
            if space_info:
                with cols[idx % 3]:
                    st.markdown(f"""
                    <div class="space-card">
                        <h3>{space_info['name']}</h3>
                        <p>Type: {space_info['type']}</p>
                        <p>Description: {space_info['description']}...</p>
                    </div>
                    """, unsafe_allow_html=True)

        # Create new space
        st.subheader("Create New Space")
        space_name = st.text_input("Space Name")
        space_type = st.radio("Space Type", ["File-based", "Query-based"])
        space_description = st.text_area("Space Description")

        if space_type == "Query-based":
            query = st.text_area("Enter your query")
            if st.button("Create Query-based Space"):
                if space_name and space_description:
                    new_space_path = os.path.join(spaces_folder, space_name)
                    os.makedirs(new_space_path, exist_ok=True)
                    with open(os.path.join(new_space_path, f"{space_name}.txt"), "w") as f:
                        f.write(query)
                    with open(os.path.join(new_space_path, "space_info.txt"), "w") as f:
                        f.write(f"{space_name}\n{space_type}\n{space_description}")
                    st.success(f"Created query-based space: {space_name}")
                else:
                    st.error("Please provide a space name and description")

        else:  # File-based
            uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
            if uploaded_file is not None:
                if space_name and space_description:
                    new_space_path = os.path.join(spaces_folder, space_name)
                    os.makedirs(new_space_path, exist_ok=True)
                    df = pd.read_csv(uploaded_file)
                    file_name = f"{space_name}.csv"
                    df.to_csv(os.path.join(new_space_path, file_name), index=False)
                    with open(os.path.join(new_space_path, "space_info.txt"), "w") as f:
                        f.write(f"{space_name}\n{space_type}\n{space_description}")
                    st.success(f"Created file-based space: {space_name}")

                    # Display the contents of the uploaded file
                    st.write("Preview of uploaded file:")
                    st.dataframe(df.head())
                else:
                    st.error("Please provide a space name and description")

    elif selected == "Profile":
        st.subheader("Profile")
        st.write(f"Welcome, {st.session_state.username}!")

    elif selected == "Analyze":
        st.subheader("Analyze")
        st.write("This is the analyze page.")

    elif selected == "Search":
        st.subheader("Search")
        st.write("This is the search page.")

    elif selected == "Settings":
        st.subheader("Settings")
        st.write("This is the settings page.")

    # Footer
    st.markdown(
        """
        <div class="custom-footer">
            © 2024 My Streamlit App. All rights reserved.
        </div>
        """,
        unsafe_allow_html=True
    )