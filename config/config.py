import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Load Env Func
env_path = os.path.join(basedir, ".env")
load_dotenv(env_path)


class Config:
    # Secrets Account
    SECRET_KEY = os.getenv("SECRET_KEY") or os.getenv("SECRET_KEY")
    ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

    # Secrets Database
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    IS_VERCEL = os.environ.get("VERCEL") == "1"

    db_url = (
        os.environ.get("DATABASE_URL")
        or os.environ.get("POSTGRES_URL")
        or os.environ.get("POSTGRES_URL_POSTGRES_URL")
        or os.environ.get("POSTGRES_URL_DATABASE_URL")
    )

    if IS_VERCEL:
        if db_url:
            if db_url.startswith("postgres://"):
                db_url = db_url.replace("postgres://", "postgresql://", 1)
            SQLALCHEMY_DATABASE_URI = db_url
        else:
            raise RuntimeError(
                "DATABASE_URL tidak ditemukan di Environment Variables Vercel!"
            )
    else:
        db_path = os.path.join(basedir, "database", "helios.db")
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{db_path}"
