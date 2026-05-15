from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import json

db = SQLAlchemy()

# Tabel Bantuan (Association Table) untuk relasi Many-to-Many antara Article dan Skill
article_skills = db.Table(
    "article_skills",
    db.Column("article_id", db.Integer, db.ForeignKey("articles.id"), primary_key=True),
    db.Column("skill_id", db.Integer, db.ForeignKey("skills.id"), primary_key=True),
)


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


class Article(db.Model):
    __tablename__ = "articles"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    # Kategori utama (masih berupa teks karena biasanya unik per artikel)
    categories = db.Column(db.String(100), default="General")
    date = db.Column(db.String(50))
    image_url = db.Column(db.String(500))
    content = db.Column(db.Text)  # Isi lengkap artikel (Markdown/HTML)

    # RELASI MANY-TO-MANY ke Skill
    # Sekarang kita tidak pakai string tech_stack, tapi berelasi langsung
    skills = db.relationship(
        "Skill",
        secondary=article_skills,
        backref=db.backref("articles", lazy="dynamic"),
    )

    def __repr__(self):
        return f"<Article {self.title}>"

    def get_category_list(self):
        """Memecah string categories menjadi list untuk looping badge di template"""
        if not self.categories:
            return ["General"]
        return [c.strip() for c in self.categories.split(",")]

    def has_tech_category(self):
        """Mengecek apakah artikel mengandung kategori teknologi untuk memunculkan tech stack"""
        # Daftar kata kunci kategori yang dianggap sebagai konten teknis
        tech_keywords = [
            "Tech",
            "Technology",
            "Development",
            "Software",
            "Coding",
            "Arduino",
        ]
        current_categories = self.get_category_list()

        # Mengembalikan True jika ada salah satu kata kunci yang cocok (case-insensitive)
        return any(
            keyword.lower() in [c.lower() for c in current_categories]
            for keyword in tech_keywords
        )
