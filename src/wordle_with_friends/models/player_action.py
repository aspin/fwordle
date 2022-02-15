from dataclasses import dataclass
from typing import Any


@dataclass
class PlayerAction:
    action: str
    params: Any
