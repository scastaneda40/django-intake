import secrets

# Generate a secure key
key = secrets.token_urlsafe(32)
print(f"Your encryption key: {key}")
