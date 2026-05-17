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


def create_app():
    app = Flask(__name__)

    # 1. Load Konfigurasi dari Object
    app.config.from_object(Config)
    # Admin dark theme
    app.config["FLASK_ADMIN_SWATCH"] = "cerulean"

    # 2. Inisialisasi Extension
    db.init_app(app)
    Migrate(app, db)

    # Setup Login Manager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "pages.login"

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Setup Flask-Admin
    admin = Admin(app, name="Super Admin", index_view=MyAdminIndexView())
    admin.template_mode = "bootstrap4"

    # Daftarkan view menggunakan class yang diimpor dari config/admin_views.py
    admin.add_view(ExperienceView(Experience, db))
    admin.add_view(MyAdminView(Skill, db))
    admin.add_view(MyAdminView(Equipment, db))
    admin.add_view(MyAdminView(NavItem, db))
    admin.add_view(
        ArticleAdminView(Article, db, name="Manage Articles", category="Content")
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
            category="Content",  # Disatukan dalam kelompok dropdown menu "Content" yang sama
        )
    )
    # 3. Registrasi Blueprint
    app.register_blueprint(pages)

    # 4. Setup Otomatis (Hanya Lokal)
    if not Config.IS_VERCEL:
        setup_local_database(app)
    else:
        print("Sistem Helios: Berjalan di Server (Cloud DB).")

    return app


def setup_local_database(app):
    """Mengurus folder dan tabel SQLite saat di laptop Advan."""
    with app.app_context():
        db_dir = os.path.join(app.root_path, "database")
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)
            print("Folder database lokal dibuat.")

        db.create_all()

        user_env = app.config.get("ADMIN_USERNAME")
        pass_env = app.config.get("ADMIN_PASSWORD")

        if user_env and pass_env:
            if not User.query.filter_by(username=user_env).first():
                new_user = User(username=user_env)
                new_user.set_password(pass_env)

                db.session.add(new_user)
                db.session.commit()
                print(f"Sistem Helios: User '{user_env}' berhasil dibuat.")
        else:
            print("PERINGATAN: ADMIN_USERNAME atau ADMIN_PASSWORD di .env kosong!")
        print("Sistem Helios Lokal: Database & Tabel siap.")


# Inisiasi Aplikasi
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
