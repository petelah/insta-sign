from .main import main_view
from .auth import auth_view
from .profile import profile_view
from.admin import admin_view

registerable_views = [
    main_view,
    auth_view,
    profile_view,
    admin_view
]