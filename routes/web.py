from flask import Blueprint, render_template, abort, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from model import User
from jinja2 import TemplateNotFound
import json

# Import Model
from model.models import NavItem, Social, Skill, Equipment, Experience

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

    return render_template("pages/login.html")


@pages.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("pages.login"))


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

        if endpoint_name == "resume":
            context["experiences"] = Experience.query.order_by(
                Experience.id.asc()
            ).all()

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
