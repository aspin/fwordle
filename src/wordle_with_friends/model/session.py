import uuid
from typing import Any, Dict

from src.wordle_with_friends import serializer


class Session(serializer.Custom):
    id: uuid.UUID

    def __init__(self, session_id: uuid.UUID):
        self.id = session_id

    def to_json(self) -> Dict[str, Any]:
        return {"id": str(self.id)}

    @classmethod
    def new(cls):
        return Session(uuid.uuid4())
