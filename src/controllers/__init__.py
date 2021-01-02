from src.controllers.user_profile_controller import user_profile
from src.controllers.auth_controller import auth
from src.controllers.posts_controller import posts

registerable_controllers = [
    auth,
    user_profile,
    posts,
]