from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import json

db = SQLAlchemy()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def set_password(self, password_mentah):
        # PASTIKAN diisi ke self.password (sesuai nama kolom di atas)
        self.password = generate_password_hash(password_mentah)

    def check_password(self, password_mentah):
        # PASTIKAN mengecek dari self.password
        return check_password_hash(self.password, password_mentah)


class NavItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String(100), nullable=False)
    icon = db.Column(db.String(50))


class Social(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    link = db.Column(db.String(200), nullable=False)
    icon = db.Column(db.String(50))


class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    icon = db.Column(db.String(100))


class Equipment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20))  # 'software' atau 'hardware'
    category = db.Column(db.String(100))
    name = db.Column(db.String(100), nullable=True)
    # Menyimpan list sebagai string JSON
    data_list = db.Column(db.Text)


class Experience(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    company = db.Column(db.String(100))
    location = db.Column(db.String(100))
    work_type = db.Column(db.String(50))
    duration = db.Column(db.String(100))
    description = db.Column(db.Text)

    @property
    def items(self):
        return json.loads(self.data_list) if self.data_list else []
