# src/tests/test_hello.py

from app.gui.app import Application


def test_hello():
    """Simple test to verify pytest is working"""
    message = "Hello, World!"
    assert message == "Hello, World!"


def test_basic_math():
    """Simple math test to verify pytest assertions"""
    result = 1 + 1
    assert result == 2


def test_application_creation():
    """Test that we can create an Application instance"""
    app = Application()
    try:
        assert isinstance(app, Application)
        assert app.title() == "My Tkinter App"
    finally:
        app.destroy()  # Clean up the window