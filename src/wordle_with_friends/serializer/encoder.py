import json
from typing import Any, Dict


def dumps(obj: Any) -> str:
    return json.dumps(obj, cls=EnhancedJSONEncoder)


class Simple:
    pass


class Custom:
    def to_json(self) -> Dict[str, Any]:
        return self.__dict__


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, Simple):
            return o.__dict__
        if isinstance(o, Custom):
            return o.to_json()
        return super().default(o)
