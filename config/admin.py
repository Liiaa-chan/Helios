from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import redirect, url_for
from wtforms import TextAreaField, DateField, SelectField
from flask_admin.form import ImageUploadField
from model.models import Category
import os

# Tempat penyimpanan data gambar
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
UPLOAD_PATH = os.path.join(PROJECT_ROOT, "static", "uploads")

try:
    os.makedirs(UPLOAD_PATH, exist_ok=True)
    print("Folder upload berhasil diverifikasi/dibuat.")
except OSError:
    # Jika berjalan di Vercel yang read-only, lewati saja agar tidak crash
    print("Berjalan di lingkungan Read-Only (Vercel). Pembuatan folder dilewati.")
    pass

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # Jika belum login, lempar ke halaman login
        return redirect(url_for("pages.login"))


class MyAdminView(ModelView):
    """Proteksi: Hanya user yang sudah login bisa masuk /admin"""

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("pages.login"))


class ExperienceView(MyAdminView):
    """Custom form untuk pengisian Experience"""

    column_list = ("title", "company", "duration")
    form_widget_args = {
        "description": {
            "rows": 10,
            "placeholder": "Gunakan | untuk memisahkan poin-poin...",
        }
    }


class ArticleAdminView(MyAdminView):
    """Custom form dan konfigurasi kelola Articles (Sudah Terproteksi)"""

    column_list = ["title", "categories", "date", "slug"]
    column_searchable_list = ["title", "description", "categories.name"]
    column_filters = ["categories.name", "date"]

    # 1. AMBIL TEMA CSS QUILL & FILEPOND VIA CDN
    extra_css = [
        "https://cdn.jsdelivr.net/npm/quill@2.0.2/dist/quill.snow.css",
        "https://unpkg.com/filepond/dist/filepond.css",
        "https://unpkg.com/filepond-plugin-image-preview/dist/filepond-plugin-image-preview.css",
    ]

    # 2. AMBIL LIBRARY JAVASCRIPT QUILL, FILEPOND PLUGINS & CUSTOM SCRIPT VIA CDN
    extra_js = [
        "https://cdn.jsdelivr.net/npm/quill@2.0.2/dist/quill.js",
        "https://unpkg.com/filepond-plugin-image-preview/dist/filepond-plugin-image-preview.js",
        "https://unpkg.com/filepond/dist/filepond.js",
        "/static/js/admin_custom.js",
    ]

    form_overrides = {
        "date": DateField,
        "description": TextAreaField,
        "content": TextAreaField,
    }

    form_extra_fields = {
        "image_url": ImageUploadField(
            "Hero Image",
            base_path=UPLOAD_PATH,
            relative_path="uploads/",
            allowed_extensions=["jpg", "jpeg", "png", "gif", "webp"],
        )
    }

    form_args = {
        "categories": {
            "query_factory": lambda: Category.query.filter_by(
                kode_kategori="article"
            ).all()
        }
    }

    form_columns = [
        "date",
        "title",
        "description",
        "categories",
        "image_url",
        "content",
        "skills",
    ]

    form_label_modifiers = {
        "date": "Tanggal Rilis Artikel",
        "categories": "Pilih Kategori Artikel",
        "skills": "Tech Stack (Skills Related)",
        "image_url": "Upload Hero Image",
        "content": "Main Content (Quill JS Rich Editor Enabled)",
    }

    def on_model_change(self, form, model, is_created):
        model.generate_slug()


class ProjectAdminView(MyAdminView):
    """Custom form dan konfigurasi kelola Projects (Sudah Terproteksi)"""

    column_list = ["title", "date", "categories", "slug"]
    column_searchable_list = ["title", "description", "categories.name"]
    column_filters = ["categories.name", "date"]

    # AMBIL TEMA CSS QUILL & FILEPOND VIA CDN
    extra_css = [
        "https://cdn.jsdelivr.net/npm/quill@2.0.2/dist/quill.snow.css",
        "https://unpkg.com/filepond/dist/filepond.css",
        "https://unpkg.com/filepond-plugin-image-preview/dist/filepond-plugin-image-preview.css",
    ]

    # AMBIL LIBRARY JAVASCRIPT QUILL, FILEPOND PLUGINS & CUSTOM SCRIPT VIA CDN
    extra_js = [
        "https://cdn.jsdelivr.net/npm/quill@2.0.2/dist/quill.js",
        "https://unpkg.com/filepond-plugin-image-preview/dist/filepond-plugin-image-preview.js",
        "https://unpkg.com/filepond/dist/filepond.js",
        "/static/js/admin_custom.js",
    ]

    form_overrides = {
        "date": DateField,
        "description": TextAreaField,
        "content": TextAreaField,
    }

    form_extra_fields = {
        "image_url": ImageUploadField(
            "Image Project",
            base_path=UPLOAD_PATH,
            relative_path="uploads/",
            allowed_extensions=["jpg", "jpeg", "png", "gif", "webp"],
        )
    }

    form_args = {
        "categories": {
            "query_factory": lambda: Category.query.filter_by(
                kode_kategori="project"
            ).all()
        }
    }

    form_columns = [
        "date",
        "title",
        "description",
        "categories",
        "image_url",
        "content",
        "github_link",
        "demo_link",
        "skills",
    ]

    form_label_modifiers = {
        "date": "Tanggal Penyelesaian Proyek",
        "categories": "Pilih Kategori Proyek",
        "github_link": "GitHub Repository URL",
        "demo_link": "Live Demo / Production URL",
        "skills": "Technologies Used (Tech Stack)",
        "content": "Technical Documentation (Quill JS Rich Editor Enabled)",
    }

    def on_model_change(self, form, model, is_created):
        model.generate_slug()


class CategoryAdminView(MyAdminView):
    """Custom form untuk mengelola master data Kategori Tunggal (Terproteksi)"""

    # Menampilkan kolom nama dan peruntukannya di tabel utama admin
    column_list = ["name", "kode_kategori"]

    # Fitur pencarian dan filter berdasarkan jenis kodenya
    column_searchable_list = ["name", "kode_kategori"]
    column_filters = ["kode_kategori"]

    # Mengubah input teks kode_kategori menjadi Dropdown pilihan baku
    form_overrides = {"kode_kategori": SelectField}

    # Menentukan opsi pilihan di dalam dropdown select
    form_args = {
        "kode_kategori": {
            "choices": [("article", "Article"), ("project", "Project")],
            "validators": [],  # Bisa ditambahkan validator jika diperlukan
        }
    }

    # Kolom yang muncul di form tambah/edit
    form_columns = ["name", "kode_kategori"]

    # Merapikan label text pada form dashboard
    form_label_modifiers = {
        "name": "Nama Kategori (e.g. Internet of Things, Reflections)",
        "kode_kategori": "Peruntukan Kategori / Tipe Data",
    }
