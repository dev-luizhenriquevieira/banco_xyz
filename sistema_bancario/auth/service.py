from dataclasses import dataclass


@dataclass
class UserSession:
    username: str
    role: str


class AuthService:
    def __init__(self):
        self._users = {
            "consultor": {"password": "1234", "role": "consultor"},
            "admin": {"password": "admin123", "role": "admin"},
        }
        self._session = None

    @property
    def session(self):
        return self._session

    def login(self, username, password):
        user = self._users.get(username)
        if not user or user["password"] != password:
            return False, "Credenciais invalidas.", None

        self._session = UserSession(username=username, role=user["role"])
        return True, "Login realizado com sucesso.", self._session

    def logout(self):
        self._session = None

    def is_authenticated(self):
        return self._session is not None
