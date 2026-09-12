import pytest
from utils.authentication import hash_password, verify_password
from utils.validation import validate_email, validate_phone, validate_password_strength


def test_password_hashing():
    pw = "Traveler@Secret2026"
    hashed = hash_password(pw)
    assert hashed != pw
    assert verify_password(pw, hashed) is True
    assert verify_password("WrongPassword", hashed) is False


def test_input_validations():
    assert validate_email("user@example.com") is True
    assert validate_email("invalid-email-string") is False
    assert validate_phone("+91 9876543210") is True
    assert validate_password_strength("short")[0] is False
    assert validate_password_strength("validpass123")[0] is True


def test_user_cannot_see_admin_dashboard_in_nav():
    from streamlit.testing.v1 import AppTest
    from pathlib import Path
    app_path = str(Path(__file__).resolve().parent.parent / "app.py")
    at = AppTest.from_file(app_path)
    at.session_state["logged_in"] = True
    at.session_state["user_role"] = "user"
    at.session_state["user_id"] = 2
    at.session_state["user_name"] = "Rohit Sharma"
    at.session_state["user_email"] = "traveler@example.com"
    at.run()
    assert not at.exception
    # Admin dashboard should NOT be accessible or listed for regular users
    sidebar_texts = [m.value for m in at.sidebar.markdown]
    assert not any("Administrator" in t for t in sidebar_texts)


def test_admin_can_access_admin_dashboard():
    from streamlit.testing.v1 import AppTest
    from pathlib import Path
    app_path = str(Path(__file__).resolve().parent.parent / "app.py")
    at = AppTest.from_file(app_path)
    at.session_state["logged_in"] = True
    at.session_state["user_role"] = "admin"
    at.session_state["user_id"] = 1
    at.session_state["user_name"] = "System Administrator"
    at.session_state["user_email"] = "admin@smarttourism.com"
    at.run()
    assert not at.exception
    sidebar_texts = [m.value for m in at.sidebar.markdown]
    assert any("Administrator" in t for t in sidebar_texts)
