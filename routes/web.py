from flask import (
    Blueprint,
    render_template,
    abort,
    redirect,
    url_for,
    flash,
    request,
    jsonify,
    make_response,
)
import os
import json
import traceback

from flask_login import login_user, logout_user, login_required, current_user
from jinja2 import TemplateNotFound

import cloudinary
import cloudinary.uploader

# Import Model
from model import User
from model.models import (
    NavItem,
    Social,
    Skill,
    Equipment,
    Experience,
    Article,
    Project,
    CV,
)

# ---------------------------------------------------------------------------
# Blueprint Setup
# ---------------------------------------------------------------------------

pages = Blueprint("pages", __name__, template_folder="templates")


# ---------------------------------------------------------------------------
# Route Mappings
# ---------------------------------------------------------------------------

ROUTE_MAPPINGS = {
    "/": "index.html",
    "/resume": "pages/resume.html",
    "/articles": "pages/articles.html",
    "/projects": "pages/project.html",
}


# ---------------------------------------------------------------------------
# Helper: Konfigurasi Cloudinary
# Dipisah menjadi fungsi sendiri agar bisa dipanggil ulang setiap request.
# Di serverless environment (Vercel, AWS Lambda), state modul bisa di-reset
# antar invokasi, sehingga config top-level tidak bisa diandalkan.
# ---------------------------------------------------------------------------


def configure_cloudinary():
    """
    Membaca CLOUDINARY_URL dari environment dan mengonfigurasi SDK.
    Mengembalikan True jika berhasil, False jika gagal.
    """
    cloudinary_url = os.environ.get("CLOUDINARY_URL", "").strip().strip('"').strip("'")

    if not cloudinary_url:
        print("❌ CLOUDINARY: Environment variable CLOUDINARY_URL tidak ditemukan.")
        return False

    if not cloudinary_url.startswith("cloudinary://"):
        print(f"❌ CLOUDINARY: Format URL tidak valid → '{cloudinary_url}'")
        return False

    try:
        url_clean = cloudinary_url.replace("cloudinary://", "")
        credentials, cloud_name = url_clean.split("@")
        api_key, api_secret = credentials.split(":")

        cloudinary.config(
            cloud_name=cloud_name.strip(),
            api_key=api_key.strip(),
            api_secret=api_secret.strip(),
            secure=True,
        )
        print("✅ CLOUDINARY: Konfigurasi berhasil.")
        return True

    except Exception as e:
        print(f"❌ CLOUDINARY: Gagal mem-parsing URL → {e}")
        return False


# ---------------------------------------------------------------------------
# Auth Routes
# ---------------------------------------------------------------------------


@pages.route("/login", methods=["GET", "POST"])
def login():
    # Jika sudah login, redirect ke halaman admin
    if current_user.is_authenticated:
        return redirect(url_for("admin.index"))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for("admin.index"))

        flash("Username atau password salah!", "error")

    return render_template("auth/login.html")


@pages.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("pages.login"))


# ---------------------------------------------------------------------------
# Helper: Data Umum Semua Halaman
# ---------------------------------------------------------------------------


def get_common_data():
    """Mengambil data dasar yang dibutuhkan oleh semua halaman (navbar, footer, dll)."""
    nav_items = NavItem.query.all()
    socials = Social.query.all()
    skills = Skill.query.all()

    equipment_db = Equipment.query.all()
    software_list = []
    hardware_list = []

    for eq in equipment_db:
        details = json.loads(eq.data_list) if eq.data_list else []

        if eq.type == "software":
            software_list.append({"category": eq.category, "items": details})
        else:
            hardware_list.append(
                {"category": eq.category, "name": eq.name, "specs": details}
            )

    equipment_data = {"software": software_list, "hardware": hardware_list}

    return nav_items, socials, skills, equipment_data


# ---------------------------------------------------------------------------
# Error Handler
# ---------------------------------------------------------------------------


@pages.app_errorhandler(404)
def page_not_found(e):
    nav_item, socials, skills, _ = get_common_data()
    return (
        render_template(
            "errors/404.html",
            nav_item=nav_item,
            socials=socials,
            skills=skills,
        ),
        404,
    )


# ---------------------------------------------------------------------------
# Dynamic Route Handler
# ---------------------------------------------------------------------------


def create_route_handler(template_path, endpoint_name):
    """Membuat handler rute secara dinamis dengan endpoint unik per rute."""

    def handler():
        nav_item, socials, skills, equipment_data = get_common_data()

        context = {
            "nav_item": nav_item,
            "socials": socials,
            "skills": skills,
            "equipment_data": equipment_data,
        }

        if endpoint_name == "resume":
            context["experiences"] = Experience.query.order_by(
                Experience.id.desc()
            ).all()
            context["active_cv"] = CV.query.filter_by(is_active=True).first()

        if endpoint_name == "articles":
            context["articles"] = Article.query.order_by(Article.id.desc()).all()

        if endpoint_name == "projects":
            context["projects"] = Project.query.order_by(Project.id.desc()).all()

        try:
            return render_template(template_path, **context)
        except TemplateNotFound:
            abort(404)

    handler.__name__ = endpoint_name
    return handler


# Register semua rute dari ROUTE_MAPPINGS secara dinamis
for route_path, template_path in ROUTE_MAPPINGS.items():
    endpoint_name = route_path.strip("/").replace("/", "_") or "index"

    pages.add_url_rule(
        route_path,
        endpoint=endpoint_name,
        view_func=create_route_handler(template_path, endpoint_name),
    )


# ---------------------------------------------------------------------------
# Detail Routes (SEO-friendly slug)
# ---------------------------------------------------------------------------


@pages.route("/articles/<string:slug>")
def article_detail(slug):
    """Menampilkan detail artikel berdasarkan slug."""
    nav_item, socials, skills, equipment_data = get_common_data()
    article = Article.query.filter_by(slug=slug).first_or_404()

    context = {
        "nav_item": nav_item,
        "socials": socials,
        "skills": skills,
        "equipment_data": equipment_data,
        "item": article,
        "back_url": url_for("pages.articles"),
    }
    return render_template("pages/detail_wrapper.html", **context)


@pages.route("/projects/<string:slug>")
def project_detail(slug):
    """Menampilkan detail project berdasarkan slug."""
    nav_item, socials, skills, equipment_data = get_common_data()
    project = Project.query.filter_by(slug=slug).first_or_404()

    context = {
        "nav_item": nav_item,
        "socials": socials,
        "skills": skills,
        "equipment_data": equipment_data,
        "item": project,
        "back_url": url_for("pages.projects"),
    }
    return render_template("pages/detail_wrapper.html", **context)


# ---------------------------------------------------------------------------
# API Upload (Cloudinary via FilePond)
# ---------------------------------------------------------------------------


@pages.route("/api/upload", methods=["POST"])
def api_upload():
    """
    Menerima file dari FilePond dan meneruskannya ke Cloudinary.

    Cloudinary dikonfigurasi ulang di sini (bukan di level modul) karena
    di serverless environment, state antar-invokasi tidak dijamin persisten.
    """

    # Step 1: Pastikan Cloudinary terkonfigurasi dengan benar sebelum upload
    if not configure_cloudinary():
        return (
            jsonify(
                {
                    "error": "Konfigurasi Cloudinary gagal. Pastikan CLOUDINARY_URL sudah diset di environment."
                }
            ),
            500,
        )

    # Step 2: Validasi keberadaan file dalam request
    if not request.files:
        print("❌ API UPLOAD: request.files kosong, FilePond tidak mengirim file.")
        return jsonify({"error": "Tidak ada berkas yang diterima oleh server."}), 400

    file_key = next(iter(request.files), None)
    uploaded_file = request.files[file_key]

    if not uploaded_file or uploaded_file.filename == "":
        print("❌ API UPLOAD: Nama file kosong atau tidak valid.")
        return jsonify({"error": "Berkas tidak valid."}), 400

    print(f"📦 API UPLOAD: Mengalirkan '{uploaded_file.filename}' ke Cloudinary...")

    # Step 3: Lakukan upload ke Cloudinary
    try:
        upload_result = cloudinary.uploader.upload(
            uploaded_file,
            folder="helios_portfolio",
            resource_type="auto",
        )
        secure_url = upload_result.get("secure_url")
        print(f"✅ UPLOAD SUCCESS: {secure_url}")
        return secure_url, 200

    except Exception as e:
        print(f"❌ CLOUDINARY UPLOAD FAILED: {str(e)}")
        traceback.print_exc()
        return jsonify({"error": f"Cloudinary Upload Failed: {str(e)}"}), 500


# XML For Crawl Data
@pages.route("/sitemap.xml", methods=["GET"])
def sitemap():
    """Menghasilkan peta situs XML secara dinamis untuk Googlebot"""
    base_url = "https://dianwicaksono.my.id/"

    # 1. Daftar halaman statis utama
    static_pages = [
        {"loc": f"{base_url}/", "changefreq": "daily", "priority": "1.0"},
        {"loc": f"{base_url}/resume", "changefreq": "monthly", "priority": "0.8"},
        {"loc": f"{base_url}/articles", "changefreq": "daily", "priority": "0.9"},
        {"loc": f"{base_url}/projects", "changefreq": "daily", "priority": "0.9"},
    ]

    # 2. Ambil halaman dinamis dari database secara asinkron
    try:
        articles = Article.query.all()
        for article in articles:
            static_pages.append(
                {
                    "loc": f"{base_url}/articles/{article.slug}",
                    "changefreq": "weekly",
                    "priority": "0.7",
                }
            )

        projects = Project.query.all()
        for project in projects:
            static_pages.append(
                {
                    "loc": f"{base_url}/projects/{project.slug}",
                    "changefreq": "weekly",
                    "priority": "0.7",
                }
            )
    except Exception as e:
        print(f"⚠️ Gagal memuat data dinamis untuk sitemap: {e}")

    # 3. Rakit dokumen XML standar sitemap
    xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

    for page in static_pages:
        xml_content += "  <url>\n"
        xml_content += f'    <loc>{page["loc"]}</loc>\n'
        xml_content += f'    <changefreq>{page["changefreq"]}</changefreq>\n'
        xml_content += f'    <priority>{page["priority"]}</priority>\n'
        xml_content += "  </url>\n"

    xml_content += "</urlset>"

    # Kembalikan response berupa text/xml murni agar bisa diparsing Google
    response = make_response(xml_content)
    response.headers["Content-Type"] = "application/xml"
    return response
