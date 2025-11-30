from functools import wraps
from django.http import HttpResponseForbidden
from django.utils.translation import gettext_lazy as _


def student_required(view_func):
    """
    Decorator for views that checks that the user is a student.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_student:
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden(_("You do not have permission to access this page. Only students may enter."))
    return _wrapped_view


def admin_required(view_func):
    """
    Decorator for views that checks that the user is an admin (not a student).
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and not request.user.is_student:
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden(_("You do not have permission to access this page. Only administrators may enter."))
    return _wrapped_view
