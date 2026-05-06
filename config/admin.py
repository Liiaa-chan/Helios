from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import redirect, url_for


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # Jika belum login, lempar ke halaman login
        return redirect(url_for("pages.login"))


class MyAdminView(ModelView):
    """Proteksi: Hanya user yang sudah login bisa masuk /admin"""

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("pages.login"))


class ExperienceView(MyAdminView):
    """Custom form untuk pengisian Experience"""

    column_list = ("title", "company", "duration")
    form_widget_args = {
        "description": {
            "rows": 10,
            "placeholder": "Gunakan | untuk memisahkan poin-poin...",
        }
    }
