from .database import SessionLocal, engine, Base
from .models import User

# Simple DB access wrapper for demo/testing
class DB:
    def __init__(self, session):
        self.session = session

    def get_user_by_email(self, email: str):
        return self.session.query(User).filter(User.email == email).first()

    def create_user(self, email: str, hashed_password: str, full_name: str = None):
        user = User(email=email, hashed_password=hashed_password, full_name=full_name)
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user


def get_db():
    db = SessionLocal()
    try:
        yield DB(db)
    finally:
        db.close()
