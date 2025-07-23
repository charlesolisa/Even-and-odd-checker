import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
import os
import uuid
import json

USER_DATA_FILE = "users.json"

def load_users():
    if not os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "w") as f:
            json.dump({}, f)
    with open(USER_DATA_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USER_DATA_FILE, "w") as f:
        json.dump(users, f)

users = load_users()

def set_styles():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800&display=swap');

        html, body, [class*="css"] {
            font-family: 'Poppins', sans-serif;
        }

        .stApp {
            background-image: url("https://i.imgur.com/0eMT5Hg.jpeg");
            background-size: cover;
            background-repeat: no-repeat;
            background-position: center;
        }

        section[data-testid="stSidebar"] {
            background: linear-gradient(to bottom, #2c3e50, #34495e);
            color: white !important;
            font-weight: bold !important;
            padding: 20px;
            border-radius: 0 20px 20px 0;
        }

        section[data-testid="stSidebar"] * {
            color: white !important;
            font-weight: bold !important;
        }

        input {
            background-color: white !important;
            color: #ff4d4d !important;
            border-radius: 8px !important;
            padding: 10px;
        }

        input:focus {
            outline: 2px solid #00cc66;
        }

        label:has(input[type="text"]), label:has(input[type="password"]) {
            color: white !important;
        }

        input[type="text"], input[type="password"] {
            background-color: #333 !important;
            color: white !important;
            border: 1px solid #555 !important;
        }

        .white-box {
            background-color: rgba(255,255,255,0.95);
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.15);
            margin: 20px 0;
        }

        /* Fixed notification styles for better visibility */
        div[data-testid="stNotification"] {
            background-color: rgba(255, 0, 0, 0.1) !important;
            color: #333 !important;
            font-weight: bold !important;
            border-radius: 10px !important;
            padding: 12px !important;
            border: 2px solid #ddd !important;
            margin: 10px 0 !important;
        }

        /* Specific styles for different alert types */
        .stAlert > div {
            background-color: rgba(255, 255, 255, 0.95) !important;
            color: #333 !important;
            font-weight: bold !important;
            border-radius: 10px !important;
            padding: 15px !important;
            margin: 10px 0 !important;
        }

        /* Error messages - red background */
        .stAlert[data-baseweb="notification"][kind="error"] > div,
        div[data-testid="stNotification"][kind="error"] {
            background-color: rgba(255, 200, 200, 0.95) !important;
            border: 2px solid #ff4444 !important;
            color: #cc0000 !important;
        }

        /* Warning messages - yellow background */
        .stAlert[data-baseweb="notification"][kind="warning"] > div,
        div[data-testid="stNotification"][kind="warning"] {
            background-color: rgba(255, 0, 0, 0.1) !important;
            border: 2px solid #ffaa00 !important;
            color: #996600 !important;
        }

        /* Success messages - green background */
        .stAlert[data-baseweb="notification"][kind="success"] > div,
        div[data-testid="stNotification"][kind="success"] {
            background-color: rgba(255, 0, 0, 0.1) !important;
            border: 2px solid #00cc66 !important;
            color: #006633 !important;
        }

        button {
            background: linear-gradient(to right, #00cc66, #00b359) !important;
            color: white !important;
            font-weight: bold !important;
            border-radius: 10px !important;
            padding: 10px 20px !important;
            border: none;
        }

        button:hover {
            background: linear-gradient(to right, #00e673, #00cc66) !important;
            transform: scale(1.02);
        }

        h1, h2, h3 {
            background: linear-gradient(to right, #00cc66, #0099cc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        label, .stSelectbox label, .stNumberInput label {
            color: white !important;
            font-weight: bold;
        }
        </style>
    """, unsafe_allow_html=True)

language_options = {
    'English': 'en',
    'French': 'fr',
    'Spanish': 'es',
    'German': 'de',
    'Arabic': 'ar',
    'Chinese (Simplified)': 'zh-CN'
}

def register_page():
    st.markdown("<div class='white-box'><h2>📝 Register</h2></div>", unsafe_allow_html=True)
    new_username = st.text_input("Choose a username", value="", max_chars=20, help="Only letters allowed")
    new_password = st.text_input("Choose a password", type="password")
    if st.button("Register"):
        if new_username in users:
            st.warning("Username already exists.")
        elif new_username == "" or new_password == "":
            st.warning("Username and password cannot be empty.")
        elif not new_username.isalpha():
            st.error("Username should only contain letters.")
        else:
            users[new_username] = {"password": new_password, "role": "user"}
            save_users(users)
            st.success("Registration successful! You can now log in.")

def login_page():
    st.markdown("<div class='white-box'><h1>🧮 Even and Odd Checker</h1></div>", unsafe_allow_html=True)
    st.markdown("<div class='white-box'><h2>🔓 Login</h2></div>", unsafe_allow_html=True)
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in users and users[username]["password"] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.role = users[username].get("role", "user")
            st.success(f"Welcome {username.title()}!")
            st.rerun()
        else:
            st.error("Invalid username or password")

def logout():
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.role = None
    st.rerun()

def even_odd_app():
    name = st.text_input("Enter your name", max_chars=30, help="Only letters allowed")
    if name and not name.isalpha():
        st.error("Name should only contain letters.")
        return

    num = st.number_input("Enter a number", step=1, format="%i")
    selected_language = st.selectbox("Choose a language", list(language_options.keys()))

    if st.button("Check & Translate"):
        if not name:
            st.warning("Please enter your name.")
        else:
            result = f"{name}, {num} is an even number 💯" if num % 2 == 0 else f"{name}, {num} is an odd number ✌️"
            st.markdown(f"<div class='white-box'><h4>🗣 Original:</h4><p>{result}</p></div>", unsafe_allow_html=True)

            lang_code = language_options[selected_language]
            try:
                translated = GoogleTranslator(source='auto', target=lang_code).translate(result)
                st.markdown(f"<div class='white-box'><h4>🌍 {selected_language}:</h4><p>{translated}</p></div>", unsafe_allow_html=True)

                tts = gTTS(text=translated, lang=lang_code)
                filename = f"{uuid.uuid4()}.mp3"
                tts.save(filename)

                with open(filename, 'rb') as audio_file:
                    st.audio(audio_file.read(), format='audio/mp3')
                os.remove(filename)
            except Exception as e:
                st.error(f"Translation/audio failed: {e}")

def main_app():
    st.markdown(f"""
    <div class="white-box" style="text-align:center;">
        <h1>🎉 Welcome {st.session_state.username.title()}!</h1>
        <p style='font-size:18px;'>Try the activity below:</p>
    </div>
    """, unsafe_allow_html=True)

    even_odd_app()

    st.markdown("---")
    if st.button("🔒  Logout"):
        logout()

# 🚀 Run the App
set_styles()

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.role = None

if st.session_state.logged_in:
    main_app()
else:
    menu = st.sidebar.radio("Menu", ["Login", "Register"])
    if menu == "Register":
        register_page()
    else:
        login_page()
