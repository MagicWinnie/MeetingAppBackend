from .auth.routes import router as auth_router
from .user.routes import router as user_router

ROUTERS = [auth_router, user_router]
