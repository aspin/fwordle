import dataclasses
import json
from enum import Flag
from typing import Dict, Type, TypeVar, Any, List, Optional, Union, Set

import humps

from src.wordle_with_friends.serializer import encoder
from src.wordle_with_friends.serializer.case import Case

T = TypeVar("T")
_TYPE_HANDLER_MAPPING = {}


def decodes(model_class: Type[T], model_params: str, model_case: Case = Case.SNAKE) -> T:
    model_dict = json.loads(model_params)
    return decode(model_class, model_dict, model_case)


def decode(model_class: Type[T], model_params: Dict[str, Any], model_case: Case = Case.SNAKE) -> T:
    """
    Loads a model class instance from the dictionary.

    This function ensures that models are forward compatible. If attributes are
    added to the model in future versions, and those versions are serialized somewhere
    (e.g. Redis), this function ensures that only attributes that the current
    version knows about are loaded.

    It's best not to dive too deeply into this class, as it is not particularly sane.

    :param model_class: class of the model to load into
    :param model_params: attributes from the retrieved model to load
    :param model_case: case of the attribute names from the retrieved model
                       these attribute names will be converted to snake_case for lookup
                       of type information
    :return: instance of model class
    """
    try:
        if issubclass(model_class, encoder.Custom):
            return model_class.from_json(model_params)

        attributes = {}
        if dataclasses.is_dataclass(model_class):
            fields = {attribute.name: attribute.type for attribute in dataclasses.fields(model_class)}
        else:
            fields = model_class.__annotations__

        for attribute_name, attribute_type in fields.items():
            if model_case == Case.SNAKE:
                model_attribute_name = attribute_name
            else:
                model_attribute_name = humps.camelize(attribute_name)
            if model_attribute_name in model_params:
                attributes[attribute_name] = _load_attribute(
                    attribute_type, model_params[model_attribute_name], model_case=model_case
                )
        return model_class(**attributes)
    except Exception as e:
        raise TypeError(
            f"Could not load model of type {model_class} from data: {model_params}"
        ) from e


def _load_attribute(
    attribute_type: Type[T],
    attribute_value: Any,
    cast_basic_values: bool = True,
    model_case: Case = Case.SNAKE,
) -> Optional[T]:
    """
    Loads an attribute and attempts to cast it to the correct class type.

    For dataclasses, recurse and attempt to load the original model.
    For Any types, None values, or Generic types, return the provided value as is.
    For builtin `typing` types, special handling is generally required.
        List/Dict/... have been implemented for now.
    For Flag enum types, use the Flag name for loading / writing.
    For basic types, construct the objects normally.

    :param attribute_type: class of the attribute to load
    :param attribute_value: attribute value to parse
    :param cast_basic_values: if to cast between str, int, etc.
    :return: instance of attribute value
    """
    if hasattr(attribute_type, "__annotations__"):
        return decode(attribute_type, attribute_value, model_case)
    elif attribute_type == Any or attribute_value is None or attribute_type.__class__ == TypeVar:
        return attribute_value
    elif hasattr(attribute_type, "__origin__"):
        if attribute_type.__origin__ in _TYPE_HANDLER_MAPPING:
            return _TYPE_HANDLER_MAPPING[attribute_type.__origin__](
                attribute_type, attribute_value, model_case
            )
        else:
            raise NotImplementedError(
                f"Model loader is not capable of loading a "
                f"{attribute_type.__origin__} type. Please implement a handler."
            )
    elif issubclass(attribute_type, Flag):
        return attribute_type[str(attribute_value)]
    else:
        if cast_basic_values:
            return attribute_type(attribute_value)
        elif not isinstance(attribute_value, attribute_type):
            raise TypeError(f"{attribute_value} is not of type {attribute_type}.")
        else:
            return attribute_value


def _load_list(list_type: Type[T], list_value: Any, model_case: Case) -> List:
    if isinstance(list_value, dict):
        raise ValueError("Forcibly raising when trying to cast Dict to List.")

    if len(list_type.__args__) != 1:
        raise ValueError("List type annotation requires 1 or 0 args.")

    list_param = list_type.__args__[0]
    return [
        _load_attribute(list_param, list_entry, model_case=model_case) for list_entry in list_value
    ]


def _load_set(set_type: Type[T], set_value: Any, model_case: Case) -> Set:
    if isinstance(set_value, dict):
        raise ValueError("Forcibly raising when trying to cast Dict to Set.")

    if len(set_type.__args__) != 1:
        raise ValueError("List type annotation requires 1 or 0 args.")

    set_param = set_type.__args__[0]
    return {_load_attribute(set_param, set_entry, model_case=model_case) for set_entry in set_value}


def _load_dict(dict_type: Type[T], dict_value: Any, model_case: Case) -> Dict:
    if not isinstance(dict_value, Dict):
        raise TypeError("Cannot deserialize value {} to Dict type {}".format(dict_value, dict_type))

    if len(dict_type.__args__) != 2:
        raise ValueError("Dict type annotation requires 2 or 0 args.")

    key_type = dict_type.__args__[0]
    value_type = dict_type.__args__[1]
    return {
        _load_attribute(key_type, key, model_case=model_case): _load_attribute(
            value_type, value, model_case=model_case
        )
        for key, value in dict_value.items()
    }


def _load_optional(optional_type: Type[T], optional_value: Any, model_case: Case) -> Optional:
    if len(optional_type.__args__) != 1:
        raise ValueError("Optional types must have a type annotation.")

    optional_param = optional_type.__args__[0]
    return _load_attribute(optional_param, optional_value, model_case=model_case)


def _load_union(union_type: Type[T], union_value: Any, model_case: Case) -> Any:
    if len(union_type.__args__) == 2 and type(None) in union_type.__args__:
        # special case of an optional
        return _load_attribute(union_type.__args__[0], union_value, model_case=model_case)
    else:
        for union_param in union_type.__args__:
            # noinspection PyBroadException
            try:
                return _load_attribute(
                    union_param, union_value, cast_basic_values=False, model_case=model_case
                )
            except Exception as _e:
                continue
        raise NotImplementedError(
            f"Could not find a union type that matched value. "
            f"Types: {union_type.__args__}, Value: {union_value}"
        )


_TYPE_HANDLER_MAPPING.update(
    {
        list: _load_list,
        List: _load_list,
        set: _load_set,
        Set: _load_set,
        dict: _load_dict,
        Dict: _load_dict,
        Optional: _load_optional,
        Union: _load_union,
    }
)
