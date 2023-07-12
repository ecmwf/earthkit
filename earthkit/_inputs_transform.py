"""
Module containing methods to transform the inputs of functions based on the function type setting,
common signitures or mapping defined at call time
"""
from ast import Module
import inspect
import types
import typing as T
from functools import wraps

from earthkit import data

try:
    UNION_TYPES = [T.Union, types.UnionType]
except AttributeError:
    # This sort of Union is not allowed in versions of python<3.9
    UNION_TYPES = [
        T.Union,
    ]

EMPTY_TYPES = [inspect._empty]


TRANSFORMERS = {
}

def transform(value, kwarg_type):
    transformer = TRANSFORMERS.get(
        kwarg_type, data.transform
    )
    transformed = transformer(value, kwarg_type)
    return transformed

def ensure_iterable(input_item):
    """Ensure that an item is iterable"""
    if not isinstance(input_item, (tuple, list, dict)):
        return [input_item]
    return input_item


def transform_function_inputs(function, **kwarg_types):
    """
    Transform the inputs to a function to match the requirements.
    earthkit.data handles the input arg/kwarg format.
    """

    def _wrapper(kwarg_types, *args, **kwargs):
        kwarg_types = {**kwarg_types}
        signature = inspect.signature(function)
        mapping = signature_mapping(signature, kwarg_types)

        for arg, name in zip(args, signature.parameters):
            kwargs[name] = arg
        # transform kwargs if necessary
        for j, (key, value) in enumerate([(k, v) for k, v in kwargs.items() if k in mapping]):
            kwarg_types = ensure_iterable(mapping[key])
            # Transform value if necessary
            if type(value) not in kwarg_types:
                for kwarg_type in kwarg_types:
                    try:
                        kwargs[key] = transform(value, kwarg_type)
                    except ValueError:
                        # Transform was not possible, move to next kwarg type.
                        # If no trnasform is possible, format is unchanged and we rely on function to raise
                        # an Error.
                        continue
                    break
        result = data.from_object(function(**kwargs))

        return result

    @wraps(function)
    def wrapper(*args, **kwargs):
        return _wrapper(kwarg_types, *args, **kwargs)

    return wrapper


def signature_mapping(signature, kwarg_types):
    """
    Map args and kwargs to object types, using hierarchical selection method:
    1. Type setting
    2. Explicitly defined type
    3. Do nothing
    """
    mapping = {}
    for key, parameter in signature.parameters.items():
        annotation = parameter.annotation
        if annotation not in EMPTY_TYPES:
            # 1. Use type setting from function
            if T.get_origin(annotation) in UNION_TYPES:
                kwarg_type = T.get_args(annotation)
            else:
                kwarg_type = annotation
        elif key in kwarg_types:
            # 2. Check for specifically assigned format
            kwarg_type = kwarg_types.get(key)
        else:
            # 3. Do nothing, cannot assign None, as None is a valid type
            continue
        mapping[key] = kwarg_type
    return mapping


def transform_module_inputs(in_module, decorator=transform_function_inputs, **decorator_kwargs):
    """
    Transform the inputs to all functions in a module.
    """
    # wrapped_module must be different to original to prevent overriding py-cached module
    wrapped_module = Module
    for name in dir(in_module):
        if name.startswith('_'):
            continue
        func = getattr(in_module, name)
        if isinstance(func, types.FunctionType):
            setattr(wrapped_module, name, decorator(func, **decorator_kwargs))
        else:
            # If not a func, we just copy
            setattr(wrapped_module, name, func)
    return wrapped_module
