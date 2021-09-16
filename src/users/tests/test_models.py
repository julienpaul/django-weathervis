import pytest
from django.core import mail

from src.users.models import User

pytestmark = pytest.mark.django_db


def test_get_short_name(user: User):
    """
    GIVEN a User instance
    WHEN  run get_short_name method
    THEN  return first 'word' of user name
    """
    assert user.get_short_name() == next(iter(user.name.split()), "")


def test_get_short_name_blank(user: User):
    """
    GIVEN a User instance
      With blank name
    WHEN  run get_short_name method
    THEN  return None
    """
    user.name = ""
    assert user.get_short_name() is None


def test_get_full_name(user: User):
    """
    GIVEN a User instance
    WHEN  run get_full_name method
    THEN  return user name
    """
    assert user.get_full_name() == user.name


def test_get_full_name_blank(user: User):
    """
    GIVEN a User instance
      With blank name
    WHEN  run get_full_name method
    THEN  return None
    """
    user.name = ""
    assert user.get_full_name() is None  # == user.name


def test_email_user(user: User):
    """
    GIVEN a User instance
      And a subject
      And a message
    WHEN  run email_user method
    THEN  send and email to the user

    based on https://github.com/django/django/blob/main/tests/auth_tests/test_models.py
    """

    # valid send_mail parameters
    kwargs = {
        "fail_silently": False,
        "auth_user": None,
        "auth_password": None,
        "connection": None,
        "html_message": None,
    }
    user.email_user(
        subject="Subject here",
        message="This is a message",
        from_email="from@domain.com",
        **kwargs,
    )
    assert len(mail.outbox) == 1
    message = mail.outbox[0]
    assert message.subject == "Subject here"
    assert message.body == "This is a message"
    assert message.from_email == "from@domain.com"
    assert message.to == [user.email]


def test_user_get_absolute_url(user: User):
    assert user.get_absolute_url() == f"/users/@{user.username}/"
