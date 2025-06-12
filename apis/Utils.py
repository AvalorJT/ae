import functools

def api_class(api_name: str):
    """Decorator to mark a class as an API class."""
    def class_wrapper(cls):
        setattr(cls, '_api_class_name', api_name)
        return cls
    return class_wrapper

def api_call(func):
    """Decorator to mark a method as an API call."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    wrapper._is_api_call = True # type: ignore[attr-defined] # Attribute to identify marked methods
    return wrapper