import os
from flask import Flask
from routes.web import pages
from model.models import db
from flask_migrate import Migrate

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

# 1. Konfigurasi Dasar
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# 2. Pengaturan URI Database
if os.environ.get("DATABASE_URL"):
    # Konfigurasi untuk PostgreSQL di Vercel
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL").replace(
        "postgres://", "postgresql://"
    )
else:
    # Konfigurasi untuk SQLite di lokal
    db_path = os.path.join(basedir, "database", "helios.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"

# Inisialisasi Database
db.init_app(app)
migrate = Migrate(app, db)

# Registrasi Blueprint
app.register_blueprint(pages)

if not os.environ.get("DATABASE_URL") and not os.environ.get("POSTGRES_URL"):
    with app.app_context():
        # Logika ini HANYA untuk lokal (Laptop Advan Anda)
        folder_db = os.path.join(basedir, "database")
        if not os.path.exists(folder_db):
            os.makedirs(folder_db)
        db.create_all()
        print("Lokal: SQLite siap.")
else:
    print("Server: Menggunakan Cloud Database.")

if __name__ == "__main__":
    app.run(debug=True)
