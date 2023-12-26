```python
# Import necessary libraries
from flask import request, abort
from functools import wraps
import jwt
import datetime

# Secret key for JWT
SECRET_KEY = 'your_secret_key'

# Function to check if the request is authenticated
def check_auth(token):
    try:
        # Decode the token
        data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return True
    except:
        return False

# Decorator for routes that require authentication
def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Check if the token is in the header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return abort(401, 'Token is missing.')

        if not check_auth(token):
            return abort(401, 'Token is invalid or expired.')

        return f(*args, **kwargs)

    return decorated

# Function to generate a token
def generate_token(user_id):
    token = jwt.encode({
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }, SECRET_KEY, algorithm="HS256")

    return token
```
