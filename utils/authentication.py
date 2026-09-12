import hashlib
import hmac
import os
import streamlit as st
from config.settings import SECRET_KEY
from database.queries import get_user_by_email, get_user_by_id


def hash_password(password: str) -> str:
    """Produces a secure SHA-256 HMAC hash with salt for credentials."""
    salt = SECRET_KEY[:16].encode("utf-8")
    h = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100000)
    return h.hex()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain password against the stored PBKDF2 HMAC hex hash."""
    return hmac.compare_digest(hash_password(plain_password), hashed_password)


def login_user(email: str, password: str):
    """Validates user credentials and initiates the session."""
    user = get_user_by_email(email)
    if not user:
        return False, "No account found with this email address."
    
    if not verify_password(password, user["password_hash"]):
        return False, "Incorrect password. Please try again."
    
    st.session_state["logged_in"] = True
    st.session_state["user_id"] = user["id"]
    st.session_state["user_name"] = user["name"]
    st.session_state["user_email"] = user["email"]
    st.session_state["user_role"] = user.get("role", "user")
    return True, f"Welcome back, {user['name']}!"


def logout_user():
    """Clears user session variables."""
    keys_to_clear = ["logged_in", "user_id", "user_name", "user_email", "user_role"]
    for k in keys_to_clear:
        if k in st.session_state:
            del st.session_state[k]


def get_current_user():
    """Returns currently authenticated user data or None."""
    if not st.session_state.get("logged_in"):
        return None
    user_id = st.session_state.get("user_id")
    if not user_id:
        return None
    return get_user_by_id(user_id)


def is_authenticated() -> bool:
    return bool(st.session_state.get("logged_in", False))


def is_admin() -> bool:
    return st.session_state.get("user_role") == "admin"
