from django.urls import path
from . import views

urlpatterns=[
    path('',views.mis_dashboard,name='mis_dashboard'), 
    path('employee_data/',views.employee_data,name="employee_data"),  
    path('mis_edit_2/',views.mis_edit_2,name='forms'),
    path('mis_header',views.mis_header,name='forms'),
    path('people_trained/',views.people_trained,name='people_trained'),
    path('manhours/',views.manhours,name='manhours'),

    path('number_of_training_sessions/',views.number_of_training_sessions,name='number_of_training_sessions'),
    path('no_of_safety_alert_card/',views.no_of_safety_alert_card,name='no_of_safety_alert_card'),
    path('near_miss/',views.near_miss,name='near_miss'),
    path('safety_alert_card/',views.safety_alert_card,name='safety_alert_card'),
    path('incidents/',views.incidents,name='incidents'),
    path('road_related_incidents/',views.road_related_incidents,name='road_related_incidents'),
    path('no_of_safety_inspections/',views.no_of_safety_inspections,name='no_of_safety_inspections'),
    path('no_of_observations_for_the_month/',views.no_of_observations_for_the_month,name='no_of_observations_for_the_month'),
    path('no_of_observations_by_walkthrough/',views.no_of_observations_by_walkthrough,name='no_of_observations_by_walkthrough'),
    path('total_no_of_observations_ytd/',views.total_no_of_observations_ytd,name='total_no_of_observations_ytd'),
    path('total_no_of_observations_actiontaken_ytd/',views.total_no_of_observations_actiontaken_ytd,name='total_no_of_observations_actiontaken_ytd'),
    path('total_no_of_observations_pending_ytd/',views.total_no_of_observations_pending_ytd,name='total_no_of_observations_pending_ytd'),
    path('work_permit_issued/',views.work_permit_issued,name='work_permit_issued'),
    path('no_of_moc_approved_and_issued/',views.no_of_moc_approved_and_issued,name='no_of_moc_approved_and_issued'),
    path('no_of_eventmp_approved_and_issued/',views.no_of_eventmp_approved_and_issued,name='no_of_eventmp_approved_and_issued'),
    path('man_power_strength/',views.man_power_strength,name='man_power_strength'),
]