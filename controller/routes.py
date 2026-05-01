from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

# Eksternal Import
from models.data import SOCIALS, SVGS, PROJECTS

pages = Blueprint("pages", __name__, template_folder="templates")

ROUTE_MAPPINGS = {
    "/": "index.html",
    "/updating": "src/update.html",
    "/python-articles/": "src/update.html",  # Template sama
    "/exotic/": "src/project/exotic.html",
    "/linear/": "src/project/linear.html",
    "/nest/": "src/project/nest.html",
    "/steps/": "src/project/steps.html",
    "/otto/": "src/project/otto.html",
    "/buddaya/": "src/project/buddaya.html",
}


def create_route_handler(template_path, endpoint_name):
    """Creates route handler with unique endpoint"""

    def handler():
        try:
            return render_template(
                template_path, socials=SOCIALS, svgs=SVGS, projects=PROJECTS
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
