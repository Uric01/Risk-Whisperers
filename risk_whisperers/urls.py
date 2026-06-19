from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('webapp/', include('webapp.urls')),
    path("", include("users.urls"))
]
