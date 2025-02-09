import streamlit as st
from ui.api.user_api import get_jwt_token, create_user, soft_delete
from model.user_request import UserRequest


def login_sidebar():
    st.sidebar.header("Existing User Login")
    login_username = st.sidebar.text_input("Username", key="login_username")
    login_password = st.sidebar.text_input("Password", type="password", key="login_password")

    with st.sidebar:
        col1, _, col3 = st.columns([1, 0.5, 1])
        with col1:
            if st.button("Login"):
                if not st.session_state.jwt_token:
                    token = get_jwt_token(login_username, login_password)
                    if token:
                        st.session_state.jwt_token = token
                        st.sidebar.success("Login successful")
                    else:
                        st.sidebar.error("Login failed, check your credentials")
                else:
                    st.error("User must log out first")

        with col3:
            if st.button("Logout"):
                st.session_state.jwt_token = None
                st.sidebar.success("Logout successful")

        st.divider()
        if st.session_state.jwt_token:
            if st.button("Delete user"):
                response = soft_delete(st.session_state.jwt_token)
                if response:
                    st.error(response["details"])
                else:
                    st.success("User deleted")
                    st.session_state.jwt_token = None
        else:
            with st.expander("New User"):
                with st.form(key="new_user"):
                    first_name = st.text_input("First Name", placeholder="John")
                    last_name = st.text_input("Last Name", placeholder="Doe")
                    email = st.text_input("Email", placeholder="example@gmail.com")
                    phone = st.text_input("Phone", placeholder="0545678123")
                    address = st.text_input("Address - City And Country", placeholder="Tel-Aviv, Israel")
                    username = st.text_input("Username", placeholder="john1234")
                    password = st.text_input("password", type="password")
                    submit_button = st.form_submit_button("Submit")

                    if submit_button:
                        if not first_name:
                            st.error("First name required")
                        elif not last_name:
                            st.error("Last name required")
                        elif not email:
                            st.error("Email required")
                        elif not phone:
                            st.error("Phone required")
                        elif not address:
                            st.error("Address required")
                        elif not username:
                            st.error("Username required")
                        elif not password:
                            st.error("Password required")
                        else:
                            user_request = UserRequest(
                                first_name=first_name,
                                last_name=last_name,
                                email=email,
                                phone=phone,
                                address=address,
                                username=username,
                                password=password
                            )
                            response = create_user(user_request.dict())
                            if response:
                                st.error(response["details"])
                            else:
                                st.success("Form submitted successfully")
