from django.urls import path

from . import views

urlpatterns = [
   
    path('risk/add_asset_risk/<int:asset_id>', views.add_asset_risk, name='add_asset_risk'),
    path('risk/view_risk_add_mitigation/<int:risk_id>/', views.view_risk_add_mitigation,name='view_risk_add_mitigation'),
    path('risk/view_risk_edit/<int:risk_id>/', views.view_risk_edit, name='view_risk_edit'),
    path('risk/edit_risk/<int:risk_id>', views.edit_risk, name='edit_risk'),
    path('risk/view_risk/<int:risk_id>/', views.view_risk, name='view_risk'),
    path('report/report_filter', views.report_filter, name='report_filter'),
    path('report/export/<str:file_format>/', views.report_export, name='report_export'),
    path('risk/edit_risk_mitigation', views.edit_risk_mitigation, name='edit_risk_mitigation'),
    path('mitigation/view_mitigation', views.view_mitigations, name='view_mitigation'),
    path('mitigation/add_mitigation', views.add_mitigation, name='add_mitigation'),
    path('asset/add_asset', views.add_asset, name='add_asset'),
    path('asset/view_asset/<int:asset_id>/', views.view_asset, name='view_asset'),
    path('asset/edit_asset/<int:asset_id>/', views.edit_asset, name='edit_asset'),
    path('risk/add_risk', views.add_risk, name = 'add_risk'),
    path('asset/asset_filter', views.assets_filter, name = 'assets_filter'),
    path('risk/risk_filter', views.risk_filter, name='risk_filter'),
    path('audit/audit_log_filter', views.audit_log_filter, name='audit_log_filter'),
    path('', views.home, name='home'),
    path('<slug:page_name>', views.page, name='page'),
    
]
