import os
from flask import Flask
from flask_admin import Admin
from flask_login import LoginManager
from routes.web import pages
from model import (
    db,
    Experience,
    Skill,
    Equipment,
    NavItem,
    User,
    Article,
    Project,
    Category,
)
from flask_migrate import Migrate
from config import (
    Config,
    MyAdminView,
    ExperienceView,
    MyAdminIndexView,
    ArticleAdminView,
    ProjectAdminView,
    CategoryAdminView,
)

# Integrasi otomatis pembacaan file .env untuk fleksibilitas lokal
from dotenv import load_dotenv

load_dotenv()


def create_app():
    app = Flask(__name__)

    # 1. Load Konfigurasi dari Object (Membaca Environment Variables dari .env lokal atau Vercel)
    app.config.from_object(Config)

    # Deteksi lingkungan secara dinamis
    # Vercel secara otomatis menyuntikkan env VERCEL=1 ke dalam serverless container
    is_vercel = os.environ.get("VERCEL") == "1" or app.config.get("IS_VERCEL", False)
    app.config["IS_VERCEL"] = is_vercel

    # Tema gelap premium untuk panel Flask-Admin
    app.config["FLASK_ADMIN_SWATCH"] = "cyborg"

    # 2. Inisialisasi Extension Database & Migrasi
    db.init_app(app)
    Migrate(app, db)

    # Setup Login Manager untuk Keamanan Akses
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "pages.login"

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Setup Flask-Admin Dashboard
    admin = Admin(app, name="Super Admin", index_view=MyAdminIndexView())
    admin.template_mode = "bootstrap4"

    # Registrasi Semua Halaman Manajemen Admin secara Konsisten menggunakan db.session
    admin.add_view(ExperienceView(Experience, db.session, name="Manage Experience"))
    admin.add_view(MyAdminView(Skill, db.session, name="Manage Skills"))
    admin.add_view(MyAdminView(Equipment, db.session, name="Manage Equipment"))
    admin.add_view(MyAdminView(NavItem, db.session, name="Manage Navigation"))

    admin.add_view(
        ArticleAdminView(
            Article, db.session, name="Manage Articles", category="Content"
        )
    )
    admin.add_view(
        ProjectAdminView(
            Project,
            db.session,
            name="Manage Projects",
            category="Content",
        )
    )
    admin.add_view(
        CategoryAdminView(
            Category,
            db.session,
            name="Manage Categories",
            category="Content",
        )
    )

    # 3. Registrasi Blueprint Rute Pengunjung
    app.register_blueprint(pages)

    # 4. Sinkronisasi Skema & Pembuatan Akun Admin Otomatis (Lokal & Cloud)
    setup_database_schema(app)

    return app


def setup_database_schema(app):
    """
    Mengurus pembuatan folder (jika lokal), verifikasi tabel,
    dan pembuatan user admin otomatis menggunakan kredensial dari Env Vercel/Lokal.
    """
    with app.app_context():
        is_vercel = app.config.get("IS_VERCEL", False)

        # Tampilkan status booting sistem Helios di terminal
        print("\n" + "=" * 60)
        if is_vercel:
            print("🪐 SISTEM HELIOS: BERJALAN DI SERVER CLOUD (VERCEL)")
            # Sensor URI database untuk keamanan log Vercel
            db_uri = app.config.get("SQLALCHEMY_DATABASE_URI", "")
            masked_uri = db_uri.split("@")[-1] if "@" in db_uri else "Database Cloud"
            print(f"🔗 Database: PostgreSQL ({masked_uri})")
        else:
            print("💻 SISTEM HELIOS: BERJALAN DI LINGKUNGAN LOKAL")
            print("🔗 Database: SQLite (database/helios.db)")
        print("=" * 60)

        # A. Pengondisian Folder Database Lokal (Hanya berjalan di luar Vercel untuk menghindari Read-Only Crash)
        if not is_vercel:
            db_dir = os.path.join(app.root_path, "database")
            if not os.path.exists(db_dir):
                try:
                    os.makedirs(db_dir, exist_ok=True)
                    print("✅ Folder database lokal berhasil diverifikasi/dibuat.")
                except Exception as e:
                    print(f"⚠️ Bypass pembuatan folder database: {e}")

        # B. Pembuatan Tabel Otomatis (Aman untuk Postgres Vercel & SQLite Lokal)
        try:
            db.create_all()
            print("✅ Sinkronisasi skema tabel database berhasil.")
        except Exception as e:
            print(f"❌ Gagal melakukan sinkronisasi tabel: {e}")

        # C. Pembuatan Akun Admin Terverifikasi dari Environment Variables
        user_env = app.config.get("ADMIN_USERNAME") or os.environ.get("ADMIN_USERNAME")
        pass_env = app.config.get("ADMIN_PASSWORD") or os.environ.get("ADMIN_PASSWORD")

        if user_env and pass_env:
            try:
                # Cari apakah user tersebut sudah terdaftar di database cloud / lokal
                existing_user = User.query.filter_by(username=user_env).first()

                if not existing_user:
                    # Jika user belum ada, buat baru dan lakukan hashing password secara aman
                    new_user = User(username=user_env)
                    new_user.set_password(pass_env)

                    db.session.add(new_user)
                    db.session.commit()
                    print(
                        f"👤 Akun admin '{user_env}' sukses dibuat dan disimpan ke database!"
                    )
                else:
                    print(
                        f"ℹ️ Akun admin '{user_env}' sudah terdaftar di database. Pembuatan dilewati."
                    )
            except Exception as e:
                print(f"⚠️ Gagal memverifikasi / menyimpan user admin: {e}")
        else:
            print(
                "⚠️ PERINGATAN: ADMIN_USERNAME atau ADMIN_PASSWORD di environment masih kosong!"
            )

        print("=" * 60 + "\n")


# Inisiasi Aplikasi WSGI Flask utama untuk Vercel
app = create_app()

if __name__ == "__main__":
    # Menjalankan dengan mode debug aktif jika dijalankan langsung di lokal
    app.run(debug=True)
