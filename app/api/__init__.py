from .auth.routes import router as auth_router
from .user.routes import router as user_router
from .user_interest.routes import router as user_interest_router

ROUTERS = [auth_router, user_router, user_interest_router]
