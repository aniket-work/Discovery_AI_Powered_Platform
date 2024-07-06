import streamlit as st
from database import verify_user, add_user, get_secret_question, verify_secret_answer, update_password


def login_page():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if verify_user(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("Logged in successfully!")
            st.experimental_rerun()
        else:
            st.error("Invalid username or password")

    if st.button("Forgot Password"):
        st.session_state.page = "forgot_password"
        st.experimental_rerun()

    if st.button("Sign Up"):
        st.session_state.page = "signup"
        st.experimental_rerun()


def signup_page():
    st.title("Sign Up")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    secret_question = st.text_input("Secret Question")
    secret_answer = st.text_input("Secret Answer")

    if st.button("Sign Up"):
        if password != confirm_password:
            st.error("Passwords do not match")
        elif not username or not password or not secret_question or not secret_answer:
            st.error("All fields are required")
        else:
            try:
                add_user(username, password, secret_question, secret_answer)
                st.success("Account created successfully!")
                st.session_state.page = "login"
                st.experimental_rerun()
            except Exception as e:
                st.error(f"Error creating account: {str(e)}")

    if st.button("Back to Login"):
        st.session_state.page = "login"
        st.experimental_rerun()


def forgot_password_page():
    st.title("Forgot Password")
    username = st.text_input("Username")
    if username:
        secret_question = get_secret_question(username)
        if secret_question:
            st.write(f"Secret Question: {secret_question}")
            secret_answer = st.text_input("Your Answer")
            new_password = st.text_input("New Password", type="password")
            confirm_password = st.text_input("Confirm New Password", type="password")

            if st.button("Reset Password"):
                if new_password != confirm_password:
                    st.error("Passwords do not match")
                elif verify_secret_answer(username, secret_answer):
                    update_password(username, new_password)
                    st.success("Password updated successfully!")
                    st.session_state.page = "login"
                    st.experimental_rerun()
                else:
                    st.error("Incorrect answer to secret question")
        else:
            st.error("Username not found")

    if st.button("Back to Login"):
        st.session_state.page = "login"
        st.experimental_rerun()