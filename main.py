import streamlit as st
import os
import pandas as pd
from pathlib import Path
import shutil
import base64
import json

# Define file paths and user credentials
CREDENTIALS = {"username": "malik", "password": "oteiut_yust*212"}
UPLOAD_DIR = Path("uploaded_files")
NOTEPAD_FILE = Path("notepad.txt")

# Ensure the upload directory exists
UPLOAD_DIR.mkdir(exist_ok=True)

# Initialize session state variables
if "login_attempts" not in st.session_state:
    st.session_state.login_attempts = 0
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "notepad_content" not in st.session_state:
    st.session_state.notepad_content = ""

def authenticate(username, password):
    return username == CREDENTIALS["username"] and password == CREDENTIALS["password"]

def reset_login_attempts():
    st.session_state.login_attempts = 0

def block_ip():
    st.session_state.logged_in = False
    st.session_state.login_attempts = 6  # simulate blocking

def login_page():
    st.title("Login Page")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if authenticate(username, password):
            reset_login_attempts()
            st.session_state.logged_in = True
            st.experimental_rerun()
        else:
            st.session_state.login_attempts += 1
            if st.session_state.login_attempts >= 6:
                block_ip()
                st.error("Your IP is blocked due to too many failed login attempts.")
            else:
                st.error("Invalid username or password.")

def upload_file():
    st.title("Upload Document")
    uploaded_file = st.file_uploader("Choose a file", type=["pdf", "jpg", "mp4", "txt"])

    if uploaded_file:
        file_path = UPLOAD_DIR / uploaded_file.name
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success("File uploaded successfully.")

def list_files():
    st.title("Uploaded Documents")
    files = list(UPLOAD_DIR.glob("*"))
    if files:
        for file in files:
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.write(file.name)
            with col2:
                if st.button("Download", key=file.name):
                    with open(file, "rb") as f:
                        st.download_button(label="Download", data=f, file_name=file.name)
            with col3:
                if st.button("Delete", key=f.name + "_delete"):
                    os.remove(file)
                    st.success(f"{file.name} deleted.")
                    st.experimental_rerun()
    else:
        st.write("No files uploaded yet.")

def notepad():
    st.title("Mini Notepad")
    text = st.text_area("Notepad", value=st.session_state.notepad_content, height=200)

    if st.button("Save"):
        st.session_state.notepad_content = text
        with open(NOTEPAD_FILE, "w") as f:
            f.write(text)
        st.success("Notepad content saved.")

    if st.button("Load"):
        if NOTEPAD_FILE.exists():
            with open(NOTEPAD_FILE, "r") as f:
                st.session_state.notepad_content = f.read()
            st.text_area("Notepad", value=st.session_state.notepad_content, height=200)
            st.success("Notepad content loaded.")
        else:
            st.warning("No notepad file found.")

def main():
    if st.session_state.logged_in:
        st.sidebar.title("Navigation")
        selection = st.sidebar.radio("Go to", ["Upload Document", "View Documents", "Notepad"])

        if selection == "Upload Document":
            upload_file()
        elif selection == "View Documents":
            list_files()
        elif selection == "Notepad":
            notepad()
    else:
        login_page()

if __name__ == "__main__":
    main()
