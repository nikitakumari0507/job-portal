from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve


urlpatterns = [
    path(
        "admin/",
        admin.site.urls
    ),

    path(
        "",
        include("core.urls")
    ),

    path(
        "accounts/",
        include("accounts.urls")
    ),

    path(
        "jobs/",
        include("jobs.urls")
    ),

    # Serve only public company logos
    re_path(
        r"^media/company_logos/(?P<path>.*)$",
        serve,
        {
            "document_root": (
                settings.MEDIA_ROOT / "company_logos"
            )
        },
    ),
]