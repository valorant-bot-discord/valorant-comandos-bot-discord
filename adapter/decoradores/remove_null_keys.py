from typing import Callable, Dict, Any


def remove_null_keys(func: Callable) -> Callable:
    def wrapper(*args, **kwargs) -> Dict[str, Any]:
        result = func(*args, **kwargs)
        if isinstance(result, dict):
            return {k: v for k, v in result.items() if v is not None}
        return result
    return wrapper