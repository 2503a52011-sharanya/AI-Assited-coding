import pytest
from pathlib import Path
from streamlit.testing.v1 import AppTest

BASE_DIR = Path(__file__).resolve().parent.parent

PAGES = [
    "pages/home.py",
    "pages/explore.py",
    "pages/planner.py",
    "pages/destinations.py",
    "pages/transportation.py",
    "pages/hotels.py",
    "pages/hostels.py",
    "pages/activities.py",
    "pages/budget.py",
    "pages/trips.py",
    "pages/bookings.py",
    "pages/profile.py",
    "pages/admin.py"
]


@pytest.mark.parametrize("page_path", PAGES)
def test_page_renders_content_without_exception(page_path):
    abs_path = str(BASE_DIR / page_path)
    at = AppTest.from_file(abs_path, default_timeout=15)
    # Set default session state
    at.session_state["user_id"] = 2
    at.session_state["user_name"] = "Rohit Sharma"
    at.session_state["user_email"] = "traveler@example.com"
    at.session_state["user_role"] = "user"
    at.session_state["logged_in"] = True
    at.run()

    # Must have zero exceptions
    assert not at.exception, f"Page {page_path} raised exception: {at.exception}"

    # Must render elements (not blank!)
    has_content = (
        len(at.title) > 0 or
        len(at.header) > 0 or
        len(at.subheader) > 0 or
        len(at.markdown) > 0 or
        len(at.button) > 0 or
        len(at.text_input) > 0
    )
    assert has_content, f"Page {page_path} rendered completely BLANK with no elements!"
