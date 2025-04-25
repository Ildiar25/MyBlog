from collections.abc import Callable
from functools import wraps
from typing import ParamSpec, TypeVar

from flask import abort
from flask_login import current_user


Parameters = ParamSpec("Parameters")
Returned = TypeVar("Returned")


# Checks if user is admin
def admin_required(func: Callable[[Parameters], Returned]) -> Callable[[Parameters], Returned]:
    @wraps(func)
    def wrapping_func(*args: Parameters.args, **kwargs: Parameters.kwargs) -> Returned:
        is_admin = getattr(current_user, "is_admin", False)
        if not is_admin:
            abort(401)
        return func(*args, **kwargs)

    return wrapping_func
