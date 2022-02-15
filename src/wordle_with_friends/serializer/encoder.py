import json
from typing import Any, Dict


def dumps(obj: Any) -> str:
    return json.dumps(obj, cls=EnhancedJSONEncoder)


class Simple:
    pass


class Custom:
    def __init__(self, *args, **kwargs):
        pass

    def to_json(self) -> Dict[str, Any]:
        return self.__dict__

    @classmethod
    def from_json(cls, dict_args: Dict[str, Any]) -> "Custom":
        return Custom(**dict_args)


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, Simple):
            return o.__dict__
        if isinstance(o, Custom):
            return o.to_json()
        return super().default(o)
