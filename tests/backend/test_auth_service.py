from app.services.auth_service import AuthService


class FakeRepo:
    def __init__(self):
        self.users = {}

    def get_by_email(self, email):
        return self.users.get(email)

    def create(self, email, password_hash):
        user = type("U", (), {"id": 1, "email": email, "password_hash": password_hash})
        self.users[email] = user
        return user


def test_signup_and_login():
    repo = FakeRepo()
    service = AuthService(repo)
    tokens = service.signup("demo@example.com", "Password123")
    assert "access_token" in tokens
    tokens2 = service.login("demo@example.com", "Password123")
    assert "refresh_token" in tokens2
