from fwordle import wtypes
from fwordle.messages.base import Message, MessageType


class GameParameters(Message[wtypes.GameParameters]):
    def __init__(self, game_parameters: wtypes.GameParameters):
        self.message_type = MessageType.GAME_PARAMETERS
        self.payload = game_parameters
