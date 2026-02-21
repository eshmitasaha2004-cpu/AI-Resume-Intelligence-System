import streamlit as st

def create_user(email, password):
    if "users" not in st.session_state:
        st.session_state.users = {}

    if email in st.session_state.users:
        return False

    st.session_state.users[email] = password
    return True


def login_user(email, password):
    if "users" not in st.session_state:
        return False

    return st.session_state.users.get(email) == password