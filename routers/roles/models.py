from fastapi import FastAPI, HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware

app = FastAPI()

# Define role-based access control (RBAC) structure
RESOURCES_FOR_ROLES = {
    'admin': {
        'resource1': ['read', 'write', 'delete'],
        'resource2': ['read', 'write'],
    },
    'user': {
        'resource1': ['read'],
        'resource2': ['read', 'write'],
    }
}

# Sample user data (can be fetched from a database)
USERS = {
    'user1': {'username': 'user1', 'password': 'password', 'role': 'user'},
    'admin1': {'username': 'admin1', 'password': 'adminpassword', 'role': 'admin'}
}

# Optionally, define paths to be excluded from checking for permissions
EXLUDED_PATHS = ['docs', 'openapi.json']


# Map request methods to actions
def translate_method_to_action(method: str) -> str:
    method_permission_mapping = {
        'GET': 'read',
        'POST': 'write',
        'PUT': 'update',
        'DELETE': 'delete',
    }
    return method_permission_mapping.get(method.upper(), 'read')


# CHeck if permission granted or not
def has_permission(user_role, resource_name, required_permission):
    if user_role in RESOURCES_FOR_ROLES and resource_name in RESOURCES_FOR_ROLES[user_role]:
        return required_permission in RESOURCES_FOR_ROLES[user_role][resource_name]
    return False


# Define a custom Middleware for handling RBAC
class RBACMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_method = str(request.method).upper()
        print(request_method)
        action = translate_method_to_action(request_method)
        print(action)
        resource = request.url.path[1:]
        print(resource)
        if not resource in EXLUDED_PATHS:
            admin1 = USERS['admin1']  # Switch between user and admin by commenting out this or the next line
            # user1 = USERS['user1']
            if not has_permission(admin1['role'], resource, action):
                raise HTTPException(status_code=403, detail="Insufficient permissions")
        response = await call_next(request)
        return response


# Add the middleware to FastAPI
app.add_middleware(RBACMiddleware)


# Example protected route for resource 1
@app.get("/resource1")
async def resource1():
    return {"message": "This is a resource1 route"}


@app.post("/resource1/add/{item}")
async def add_resource1(item: int):
    return {"message": item}


@app.delete("/resource1")
async def delete_resource1():
    return {"message": "This resource1 is deleted"}


# Example protected route for resource 2
@app.get("/resource2")
async def resource2():
    return {"message": "This is an resource2 route"}


@app.post("/resource2")
async def add_resource2(add: int):
    return {"message": add}


@app.delete("/resource2")
async def delete_resource2():
    return {"message": "This resource2 is deleted"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
