from flask import Blueprint, render_template, abort, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from model import User
from jinja2 import TemplateNotFound
import json
import cloudinary
import cloudinary.uploader

# Import Model
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

# Inisiasi pages blueprint dengan folder templates sebagai views
pages = Blueprint("pages", __name__, template_folder="templates")

ROUTE_MAPPINGS = {
    "/": "index.html",
    "/resume": "pages/resume.html",
    "/articles": "pages/articles.html",
    "/projects": "pages/project.html",
}


@pages.route("/login", methods=["GET", "POST"])
def login():
    # Jika sudah login, jangan biarkan masuk ke halaman login lagi
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
    return redirect(url_for("auth/login.html"))


def get_common_data():
    """Fungsi pembantu untuk mengambil data dasar yang dibutuhkan semua halaman."""
    nav_items = NavItem.query.all()
    socials = Social.query.all()
    skills = Skill.query.all()

    # Mengambil dan memproses data Equipment
    equipment_db = Equipment.query.all()
    software_list = []
    hardware_list = []

    for eq in equipment_db:
        # Mengubah kembali string JSON dari database menjadi list Python
        details = json.loads(eq.data_list) if eq.data_list else []

        if eq.type == "software":
            software_list.append({"category": eq.category, "items": details})
        else:
            hardware_list.append(
                {"category": eq.category, "name": eq.name, "specs": details}
            )

    equipment_data = {"software": software_list, "hardware": hardware_list}

    return nav_items, socials, skills, equipment_data


# Error halaman
@pages.app_errorhandler(404)
def page_not_found(e):
    # Mengembalikan template custom 404 dengan status code 404
    nav_item, socials, skills, _ = get_common_data()
    return (
        render_template(
            "errors/404.html",
            nav_item=nav_item,
            socials=socials,
            skills=skills,  # Pastikan data global tetap dikirim agar navbar/footer tidak pecah
        ),
        404,
    )


# Routes Handler
def create_route_handler(template_path, endpoint_name):
    """Creates route handler with unique endpoint"""

    def handler():
        nav_item, socials, skills, equipment_data = get_common_data()

        context = {
            "nav_item": nav_item,
            "socials": socials,
            "skills": skills,
            "equipment_data": equipment_data,
        }

        # Kondisi 1: Mengambil data untuk halaman Resume
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


# Register routes with UNIQUE endpoints
for route_path, template_path in ROUTE_MAPPINGS.items():
    # Generate unique endpoint name from route path
    endpoint_name = route_path.strip("/").replace("/", "_") or "index"

    pages.add_url_rule(
        route_path,
        endpoint=endpoint_name,  # Gunakan endpoint unik
        view_func=create_route_handler(template_path, endpoint_name),
    )


# Routes Khusus untuk articles id.
@pages.route("/articles/<string:slug>")
def article_detail(slug):
    """Handler menggunakan slug untuk rute detail yang ramah SEO"""
    nav_item, socials, skills, equipment_data = get_common_data()

    # Mencari data artikel berdasarkan kolom slug di database
    article = Article.query.filter_by(slug=slug).first_or_404()

    context = {
        "nav_item": nav_item,
        "socials": socials,
        "skills": skills,
        "equipment_data": equipment_data,
        "item": article,  # Tetap dikirim sebagai 'item' agar Canvas mengenalnya
        "back_url": url_for("pages.articles"),
    }
    return render_template("pages/detail_wrapper.html", **context)


@pages.route("/projects/<string:slug>")
def project_detail(slug):
    """Handler Canvas Kosong untuk Detail Project menggunakan Slug"""
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


@pages.route("/api/upload", methods=["POST"])
def api_upload():
    """Endpoint ringkas menerima file dari FilePond dan meneruskannya ke Cloudinary"""
    # Pastikan request memiliki data file
    if not request.files:
        print("❌ CRASH API: Request.files kosong! FilePond tidak mengirimkan file berkas.")
        return jsonify({"error": "Tidak ada file yang dikirim oleh FilePond"}), 400

    file_key = next(iter(request.files), None)
    uploaded_file = request.files[file_key]
    
    print(f"📦 API DETECTED: Mencoba mengunggah file '{uploaded_file.filename}' ke Cloudinary...")
    
    try:
        # Alirkan langsung dari memori RAM ke server awan Cloudinary
        upload_result = cloudinary.uploader.upload(
            uploaded_file,
            folder="helios_portfolio",
            resource_type="auto"
        )
        
        secure_url = upload_result.get("secure_url")
        print(f"✅ UPLOAD SUCCESS: File berhasil di-host di Cloudinary -> {secure_url}")
        
        # Kirim balik URL HTTPS permanen ke FilePond frontend
        return secure_url, 200
        
    except Exception as e:
        # =========================================================================
        # CETAK ERROR SEBENARNYA KE TERMINAL (Biang Kerok Asli Akan Muncul di Sini!)
        # =========================================================================
        print("\n" + "!" * 60)
        print(f"❌ ERROR PADA /api/upload: {str(e)}")
        import traceback
        traceback.print_exc() # Mencetak runtutan baris kode yang menyebabkan crash
        print("!" * 60 + "\n")
        
        return jsonify({"error": str(e)}), 500
