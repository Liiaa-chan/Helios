from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

# Import Model
from model.data import NAV_ITEMS, SOCIALS, SKILL, EQUIPMENT_DATA

# Inisiasi pages blueprint dengan folder templates sebagai views
pages = Blueprint("pages", __name__, template_folder="templates")

ROUTE_MAPPINGS = {
    "/": "index.html",
    "/resume": "resume.html",
    "/articles": "articles.html",
    "/projects": "project.html",
}


# Error halaman
@pages.app_errorhandler(404)
def page_not_found(e):
    # Mengembalikan template custom 404 dengan status code 404
    return (
        render_template(
            "errors/404.html",
            nav_item=NAV_ITEMS,
            socials=SOCIALS,
            skills=SKILL,  # Pastikan data global tetap dikirim agar navbar/footer tidak pecah
        ),
        404,
    )


# Routes Handler
def create_route_handler(template_path, endpoint_name):
    """Creates route handler with unique endpoint"""

    def handler():
        try:
            return render_template(
                template_path,
                nav_item=NAV_ITEMS,
                socials=SOCIALS,
                skills=SKILL,
                equipment_data=EQUIPMENT_DATA,
            )
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
