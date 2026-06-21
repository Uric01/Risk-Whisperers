from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('<slug:page_name>', views.page, name='page'),
]
