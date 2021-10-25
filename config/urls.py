from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("makers", include("makers.urls")),
    path("users", include("users.urls")),
<<<<<<< HEAD
    path("makers", include("makers.urls")),
=======
>>>>>>> b829d56a874a7268d8066a0fecf457f48dd9bce2
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
