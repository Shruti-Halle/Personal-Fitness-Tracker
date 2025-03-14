import streamlit as st
import extra_streamlit_components as stx
from utils.auth import AuthManager
from pages.dashboard import show_dashboard
from pages.profile import show_profile

# Configure the app
st.set_page_config(
    page_title="Fitness Tracker",
    page_icon="🏃‍♂️",
    layout="wide"
)

# Initialize session state
if 'user_email' not in st.session_state:
    st.session_state.user_email = None
if 'user_name' not in st.session_state:
    st.session_state.user_name = None

# Load custom CSS
with open('styles/main.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def main():
    auth_manager = AuthManager()

    # Side navigation
    with st.sidebar:
        st.title("🏃‍♂️ Fitness Tracker")
        if st.session_state.user_email:
            st.write(f"Welcome, {st.session_state.user_name}!")
            if st.button("Logout"):
                st.session_state.user_email = None
                st.session_state.user_name = None
                st.rerun()  # Updated from experimental_rerun

    # Authentication handling
    if not st.session_state.user_email:
        tab1, tab2 = st.tabs(["Login", "Register"])

        with tab1:
            with st.form("login_form"):
                st.subheader("Login")
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                login_submitted = st.form_submit_button("Login")

                if login_submitted:
                    success, result = auth_manager.login_user(email, password)
                    if success:
                        st.session_state.user_email = email
                        st.session_state.user_name = result
                        st.success("Login successful!")
                        st.rerun()  # Updated from experimental_rerun
                    else:
                        st.error(result)

        with tab2:
            with st.form("register_form"):
                st.subheader("Register")
                name = st.text_input("Name")
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                register_submitted = st.form_submit_button("Register")

                if register_submitted:
                    if not name or not email or not password:
                        st.error("Please fill all fields")
                    else:
                        success, message = auth_manager.register_user(email, password, name)
                        if success:
                            st.success(message)
                        else:
                            st.error(message)

    else:
        # Navigation tabs for authenticated users
        tab1, tab2 = st.tabs(["Dashboard", "Profile"])

        with tab1:
            show_dashboard()

        with tab2:
            show_profile()

if __name__ == "__main__":
    main()