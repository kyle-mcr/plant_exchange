from django.urls import path
from final_project import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("register", views.register_view, name="register"),
    path("logout", views.logout_view, name="logout"),
    path("add", views.create_profile, name="add"),
    path("delete/<int:id>", views.delete, name="delete"),
    path("info/<int:id>", views.info, name="info"),
    path("mylistings", views.mylistings, name="mylistings"),
    path("faq", views.faq, name="faq"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)