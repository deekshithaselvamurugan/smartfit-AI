from extensions import db
from .models import User

def create_user(name, email, password):
    # Check if user already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return None

    user = User(name=name, email=email)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return user


def authenticate_user(email, password):
    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        return user
    return None
