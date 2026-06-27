from django.urls import path

from . import views

urlpatterns = [
    
    path('edit_mitigation',views.edit_mitigation, name= 'edit_mitigation'),
    path('view_mitigation', views.view_mitigations, name='view_mitigation'),
    path('add_mitigation', views.add_mitigation, name='add_mitigation'),
    path('add_asset', views.add_asset, name='add_asset'),
    path('view_asset/<int:asset_id>/', views.view_asset, name='view_asset'),
    path('edit_asset/<int:asset_id>/', views.edit_asset, name='edit_asset'),
    path('add_risk', views.add_risk, name = 'add_risk'),
    path('asset_filter', views.assets_filter, name = 'assets_filter'),
    path('', views.home, name='home'),
    path('<slug:page_name>', views.page, name='page'),
    
]
