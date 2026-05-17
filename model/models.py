from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import json
import re

db = SQLAlchemy()

# Tabel Bantuan (Association Table) untuk relasi Many-to-Many antara Article dan Skill
article_skills = db.Table(
    "article_skills",
    db.Model.metadata,
    db.Column("article_id", db.Integer, db.ForeignKey("article.id"), primary_key=True),
    db.Column("skill_id", db.Integer, db.ForeignKey("skill.id"), primary_key=True),
)

# Tabel Bantuan untuk relasi Many-to-Many antara Project dan Skill
project_skills = db.Table(
    "project_skills",
    db.Model.metadata,
    db.Column(
        "project_id",
        db.Integer,
        db.ForeignKey("project.id"),
        primary_key=True,
    ),
    db.Column(
        "skill_id",
        db.Integer,
        db.ForeignKey("skill.id"),
        primary_key=True,
    ),
)

article_category_association = db.Table(
    "article_category_association",
    db.Model.metadata,
    db.Column(
        "article_id",
        db.Integer,
        db.ForeignKey("article.id"),
        primary_key=True,
    ),
    db.Column(
        "category_id",
        db.Integer,
        db.ForeignKey("categories.id"),
        primary_key=True,
    ),
)

# Relasi Project <-> Category (Menghubungkan ke tabel tunggal Category)
project_category_association = db.Table(
    "project_category_association",
    db.Model.metadata,
    db.Column(
        "project_id",
        db.Integer,
        db.ForeignKey("project.id"),
        primary_key=True,
    ),
    db.Column(
        "category_id",
        db.Integer,
        db.ForeignKey("categories.id"),
        primary_key=True,
    ),
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

    def __str__(self):
        # Format string ini akan dibaca oleh JavaScript di Canvas untuk memunculkan ikon Devicon
        return f"{self.name}"


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


class Category(db.Model):
    """Model Kategori tunggal dengan pembeda kolom 'kode_kategori'"""

    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    # Kolom pembeda: diisi 'article' untuk artikel, atau 'project' untuk project
    kode_kategori = db.Column(db.String(50), nullable=False, default="article")

    # Mencegah duplikasi nama kategori yang sama di dalam satu tipe kode yang sama
    __table_args__ = (
        db.UniqueConstraint("name", "kode_kategori", name="_name_kode_kategori_uc"),
    )

    def __str__(self):
        return f"{self.name} ({self.kode_kategori.upper()})"


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=True)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.Date, nullable=True)
    image_url = db.Column(db.String(500))
    content = db.Column(db.Text)

    # Relasi Many-to-Many ke Skill
    skills = db.relationship(
        "Skill",
        secondary=article_skills,
        backref=db.backref("articles", lazy="dynamic"),
    )

    # Relasi Many-to-Many ke tabel tunggal Category
    categories = db.relationship(
        "Category",
        secondary=article_category_association,
        backref=db.backref("articles", lazy="dynamic"),
    )

    @property
    def formatted_date(self):
        """Format tanggal ramah bahasa Indonesia"""
        if self.date:
            months = {
                1: "Januari",
                2: "Februari",
                3: "Maret",
                4: "April",
                5: "Mei",
                6: "Juni",
                7: "Juli",
                8: "Agustus",
                9: "September",
                10: "Oktober",
                11: "November",
                12: "Desember",
            }
            return f"{self.date.day} {months[self.date.month]} {self.date.year}"
        return ""

    def get_category_list(self):
        """Helper mempertahankan kompatibilitas dengan template lama"""
        return [cat.name for cat in self.categories]

    def has_tech_category(self):
        """Mengecek apakah artikel mengandung kategori teknologi"""
        tech_keywords = [
            "tech",
            "development",
            "coding",
            "laravel",
            "flask",
            "software",
        ]
        return any(cat.name.lower() in tech_keywords for cat in self.categories)

    def generate_slug(self):
        clean_title = self.title.lower()
        self.slug = re.sub(r"[^a-z0-9]+", "-", clean_title).strip("-")


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=True)
    description = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text)
    image_url = db.Column(db.String(500))
    github_link = db.Column(db.String(200))
    demo_link = db.Column(db.String(200))
    date = db.Column(db.Date, nullable=True)

    # Relasi Many-to-Many ke Skill
    skills = db.relationship(
        "Skill",
        secondary=project_skills,
        backref=db.backref("projects", lazy="dynamic"),
    )

    # Relasi Many-to-Many ke tabel tunggal Category
    categories = db.relationship(
        "Category",
        secondary=project_category_association,
        backref=db.backref("projects", lazy="dynamic"),
    )

    @property
    def formatted_date(self):
        if self.date:
            months = {
                1: "Januari",
                2: "Februari",
                3: "Maret",
                4: "April",
                5: "Mei",
                6: "Juni",
                7: "Juli",
                8: "Agustus",
                9: "September",
                10: "Oktober",
                11: "November",
                12: "Desember",
            }
            return f"{self.date.day} {months[self.date.month]} {self.date.year}"
        return ""

    def get_category_list(self):
        return [cat.name for cat in self.categories]

    def generate_slug(self):
        clean_title = self.title.lower()
        self.slug = re.sub(r"[^a-z0-9]+", "-", clean_title).strip("-")
