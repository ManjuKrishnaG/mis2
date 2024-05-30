from django.urls import path
from . import views

urlpatterns = [
    path('mis_dashboard/<str:refid>',views.mis_dashboard,name='dashboard' ),
    path('people_trained/', views.people_trained, name='people_trained'),
    path('calender/',views.calender,name='calender'),
    path('adminscrn/',views.adminscrn,name='adminscrn'),
    path('manage/',views.manage,name='manage'),    
    path('save_form_data/', views.save_form_data, name='save_form_data'),
    path('save-data/', views.save_data, name='save-data'),
    path('get-data/', views.get_data, name='get_data'),
    path('enabled-data/', views.enable_data, name='enable-data'),
    path('save_form/', views.save_form, name='save_form'),
    path('disable-data/', views.disable_data, name='disable-data'),
    path('update_approval_request/', views.update_approval_request, name='update_approval_request'),
    path('change_edit_field', views.change_edit_field,name='change_edit_field'),
    path('delete_data', views.delete_data, name='delete_data'),
    path('upload_files/', views.upload_files, name='upload_files'),
    path('delete_attachment/<int:attachment_id>/', views.delete_attachment, name='delete_attachment'),
    path('showfield/<str:empid>/<str:form_number>/', views.showfield, name='showfield'),
    path('editfield/<str:empid>/<str:form_number>/', views.editfield, name='editfield'),
    path('get_month_data/<int:month>/', views.get_month_data, name='get_month_data'),
    path('graph/<str:month>/', views.graph, name='graph'),
    path('render_people_trained/', views.render_people_trained, name='render_people_trained'),

]

