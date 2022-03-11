import json
from typing import Any, Dict, Callable

import humps

from fwordle.serializer.case import Case


def encodes(case: Case) -> Callable[[Any], str]:
    def inner(obj: Any):
        return json.dumps(obj, cls=EnhancedJSONEncoder, case=case)

    return inner


Encoder = Callable[[Any], str]


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
    _case_fn: Callable[[Any], Any]

    def __init__(self, *, case: Case = Case.SNAKE, **kwargs):

        if case == Case.SNAKE:
            self._case_fn = humps.decamelize
        else:
            self._case_fn = humps.camelize

        super().__init__(**kwargs)

    def default(self, o: Any) -> Any:
        if isinstance(o, Simple):
            return self._case_fn(o.__dict__)
        if isinstance(o, Custom):
            return self._case_fn(o.to_json())
        return super().default(o)
