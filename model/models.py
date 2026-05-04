from flask_sqlalchemy import SQLAlchemy
import json

db = SQLAlchemy()


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

    @property
    def items(self):
        return json.loads(self.data_list) if self.data_list else []
