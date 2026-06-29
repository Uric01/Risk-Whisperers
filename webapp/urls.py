from django.urls import path

from . import views

urlpatterns = [
    path('view_risk_edit/<int:risk_id>/', views.view_risk_edit, name='view_risk_edit'),
    path('view_risk/<int:risk_id>/', views.view_risk, name='view_risk'),
    path('report_filter', views.report_filter, name='report_filter'),
    path('edit_risk_mitigation', views.edit_risk_mitigation, name='edit_risk_mitigation'),
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
