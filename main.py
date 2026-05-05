import os
from flask import Flask
from routes.web import pages
from model.models import db
from flask_migrate import Migrate

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

IS_VERCEL = os.environ.get("VERCEL") == "1"

# 1. Konfigurasi Dasar
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# 2. Pengaturan URI Database
if IS_VERCEL or os.environ.get("DATABASE_URL"):
    url = os.environ.get("DATABASE_URL") or os.environ.get("POSTGRES_URL")
    if url and url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
    app.config["SQLALCHEMY_DATABASE_URI"] = url
else:
    db_path = os.path.join(basedir, "database", "helios.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"

# Inisialisasi Database
db.init_app(app)
migrate = Migrate(app, db)

# Registrasi Blueprint
app.register_blueprint(pages)

if not IS_VERCEL:
    with app.app_context():
        folder_db = os.path.join(basedir, "database")
        if not os.path.exists(folder_db):
            os.makedirs(folder_db)
            print("Folder database lokal berhasil dibuat.")
        
        # Di lokal kita pakai create_all() agar praktis
        db.create_all()
        print("Sistem Helios Lokal: Database & Tabel siap.")
else:
    # Di Vercel, kita tidak membuat folder atau db.create_all() secara otomatis
    # Kita akan menggunakan Flask-Migrate via terminal atau dashboard
    print("Sistem Helios Server: Menggunakan cloud database.")

if __name__ == "__main__":
    app.run(debug=True)
