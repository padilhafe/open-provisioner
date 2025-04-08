from app.models.user import User

# Simulated DB
fake_users = [
    User(id=1, name="Alice"),
    User(id=2, name="Bob"),
]

def get_all_users():
    return fake_users

def get_user_by_id(user_id: int):
    return next((user for user in fake_users if user.id == user_id), None)
