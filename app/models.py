from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phonenumber = db.Column(db.String(20), nullable=False)
    password_hashed = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"<User {self.name}>"