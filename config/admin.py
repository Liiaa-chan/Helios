import os
from flask import redirect, url_for
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from wtforms import TextAreaField, DateField, SelectField, StringField # Ditukar sepenuhnya ke StringField
from model.models import Category

# Tempat penyimpanan data gambar fisik (try-except aman untuk Read-Only Vercel)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
UPLOAD_PATH = os.path.join(PROJECT_ROOT, "static")

try:
    os.makedirs(UPLOAD_PATH, exist_ok=True)
    print("Folder upload berhasil diverifikasi/dibuat.")
except OSError:
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

    # Menambahkan CSS gelap secara global di kelas induk utama
    extra_css = ["/static/css/admin_dark.css"]


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
        "image_url": StringField, # Menyimpan URL teks CDN Cloudinary dari FilePond
    }

    # FIX 1: Kosongkan form_extra_fields agar tidak memicu deteksi unggahan lokal PIL/Pillow
    form_extra_fields = {}

    # FIX 2: Menghapus .all() agar WTForms menerima objek Query yang valid untuk pemetaan relasi
    form_args = {
        "categories": {
            "query_factory": lambda: Category.query.filter_by(
                kode_kategori="article"
            )
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

    # FIX 3: Menggunakan 'column_labels' bawaan agar label terjemahan form ter-render sempurna
    column_labels = {
        "date": "Tanggal Rilis Artikel",
        "title": "Judul Artikel",
        "description": "Deskripsi Singkat",
        "categories": "Pilih Kategori Artikel",
        "skills": "Tech Stack (Skills Related)",
        "image_url": "Upload Hero Image (via FilePond Cloud)",
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
        "image_url": StringField, # Menyimpan URL teks CDN Cloudinary dari FilePond
    }

    # FIX 1: Kosongkan form_extra_fields agar tidak memicu deteksi unggahan lokal PIL/Pillow
    form_extra_fields = {}

    # FIX 2: Menghapus .all() agar WTForms menerima objek Query yang valid untuk pemetaan relasi
    form_args = {
        "categories": {
            "query_factory": lambda: Category.query.filter_by(
                kode_kategori="project"
            )
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

    # FIX 3: Menggunakan 'column_labels' bawaan agar label terjemahan form ter-render sempurna
    column_labels = {
        "date": "Tanggal Penyelesaian Proyek",
        "title": "Judul Proyek",
        "description": "Deskripsi Proyek",
        "categories": "Pilih Kategori Proyek",
        "image_url": "Image Project (via FilePond Cloud)",
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

    # FIX: Menggunakan 'column_labels' bawaan agar label terjemahan form ter-render sempurna
    column_labels = {
        "name": "Nama Kategori (e.g. Internet of Things, Reflections)",
        "kode_kategori": "Peruntukan Kategori / Tipe Data",
    }


class CVAdminView(MyAdminView):
    """Konfigurasi panel kontrol untuk mengelola berkas CV Resume dengan FilePond"""

    column_list = ["title", "file_name", "is_active", "uploaded_at"]
    column_searchable_list = ["title"]
    column_filters = ["is_active"]

    form_columns = ["title", "file_name", "external_link", "is_active"]

    # 1. SUNTIKKAN CSS FILEPOND (Akan digabungkan ke master.html secara otomatis)
    extra_css = [
        "https://unpkg.com/filepond/dist/filepond.css",
        "https://unpkg.com/filepond-plugin-image-preview/dist/filepond-plugin-image-preview.css",
    ]

    # 2. SUNTIKKAN JS FILEPOND & SCRIPT KUSTOM ANDA
    extra_js = [
        "https://unpkg.com/filepond-plugin-image-preview/dist/filepond-plugin-image-preview.js",
        "https://unpkg.com/filepond/dist/filepond.js",
        "/static/js/admin_custom.js",  # <-- Memanggil script inisialisasi kustom
    ]

    # FIX 1: Kosongkan form_extra_fields karena file_name sekarang berinteraksi dengan API Cloudinary asinkron
    form_extra_fields = {}

    # Menjadikan file_name sebagai StringField biasa agar menampung tautan aman Cloudinary
    form_overrides = {
        "file_name": StringField,
    }
    
    # FIX: Menyelaraskan ke properti 'column_labels' standar Flask-Admin
    column_labels = {
        "title": "Nama / Label CV",
        "file_name": "Upload Berkas CV PDF/DOCX (via FilePond Cloud)",
        "external_link": "Tautan Cloud Permanen (Alternatif Vercel)",
        "is_active": "Aktifkan CV Ini di Frontend",
        "uploaded_at": "Tanggal Unggah",
    }
