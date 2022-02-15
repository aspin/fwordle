from typing import Dict

from src.wordle_with_friends import model


class SessionManager:
    sessions: Dict[str, model.Session]

    def __init__(self):
        self.sessions = {}

    def __contains__(self, item: str):
        return item in self.sessions

    def create_new(self) -> model.Session:
        session = model.Session.new()
        self.sessions[session.id] = session
        return session
