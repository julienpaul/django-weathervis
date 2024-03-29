# Stdlib imports
# Core Django import
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views import defaults as default_views
from django.views.generic import TemplateView

# Third-party app imports
# Imports from my apps

admin.site.site_header = (
    "Django Weathervis Adminsitration"  # default: "Django Administration"
)
admin.site.index_title = "Weathervis Administration"  # default: "Site administration"
admin.site.site_title = "Django weathervis admin"  # default: "Django site admin"

urlpatterns = [
    path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    path(
        "about/", TemplateView.as_view(template_name="pages/about.html"), name="about"
    ),
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # User management
    path("users/", include("src.users.urls", namespace="users")),
    path("accounts/", include("allauth.urls")),
    # Your stuff: custom urls includes go here
    path(
        "organisations/",
        include("src.organisations.urls", namespace="organisations"),
    ),
    path(
        "stations/",
        include("src.stations.urls", namespace="stations"),
    ),
    path(
        "plots/",
        include("src.plots.urls", namespace="plots"),
    ),
    path(
        "domains/",
        include("src.domains.urls", namespace="domains"),
    ),
    path(
        "margins/",
        include("src.margins.urls", namespace="margins"),
    ),
    path(
        "model_grids/",
        include("src.model_grids.urls", namespace="model_grids"),
    ),
    # path(
    #     "charts/",
    #     TemplateView.as_view(template_name="pages/charts.html"),
    #     name="charts",
    # ),
    path(
        "campaigns/",
        include("src.campaigns.urls", namespace="campaigns"),
    ),
    path(
        "vmeteograms/",
        include("src.vertical_meteograms.urls", namespace="vmeteograms"),
    ),
    path(
        "smeteograms/",
        include("src.surface_meteograms.urls", namespace="smeteograms"),
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
