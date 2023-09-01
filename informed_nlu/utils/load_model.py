from importlib import import_module

MODELS = {
    "C_ROBERTA": "contradiction_detection.models.CRoberta",
}


def load_model(type_model, *args, **kwargs):
    """
    function to load different parsers
    """
    try:
        callable_path = MODELS[type_model]
        parts = callable_path.split(".")
        module_name = ".".join(parts[:-1])
        class_name = parts[-1]
    except KeyError:
        raise KeyError(f'Model "{type_model}" is not implemented.')

    module = import_module(module_name)
    class_ = getattr(module, class_name)
    return class_(*args, **kwargs)
