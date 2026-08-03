from app.auth.jwt_handler import create_access_token

token = create_access_token(
    {
        "sub": "testuser2@example.com",
        "id": 5
    }
)

print(token)