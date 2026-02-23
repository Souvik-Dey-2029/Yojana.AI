from backend.main import app
from fastapi.routing import APIRoute
for route in app.routes:
    if isinstance(route, APIRoute):
        print(f"ROUTE: {route.path} [{','.join(route.methods)}] -> {route.name}")
    else:
        print(f"OTHER: {getattr(route, 'path', 'N/A')} -> {type(route).__name__}")
