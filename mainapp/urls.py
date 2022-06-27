from django.urls import path

from office import views as office_views
from . import views
from transmitter_log import views as transmitter_views
from office import views as office_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.main, name="main"),
    path('worktab/', views.worktab, name="worktab"),
    path('overview/', views.overview, name="overview"),
    path('department/<str:department_name>', views.department, name="department"),
    path('login/', views.login, name="login"),
    path('log/', views.login_view, name="log"),
    path('register/', views.register, name="register"),
    path('save_profile/', views.save_profile, name="save_profile"),
    path('appoint_to_position/', views.appoint_to_position, name="appoint_to_position"),
    path('logout/', views.logout, name="logout"),
    path('clock_in/', views.clock_in, name="clock_in"),
    path('add_dept/', views.add_department, name="add_dept"),
    path('designate/', views.designate, name="designate"),
    path('designate_oic/', views.designate_oic, name="designate_oic"),
    path('usr_api/<str:username>/', views.usr_api, name="usr_api"),

    path('log_transmitter/', transmitter_views.log_transmitter, name="log_transmitter"),
    path('new_ads/', office_views.new_ads, name="new_ads"),
    path('new_invoice/', office_views.new_invoice, name="new_invoice"),
    path('populate_new_payment/<int:invoice_no>', office_views.populate_new_payment, name="populate_new_payment"),
    path('input_payment/', office_views.input_payment, name="input_payment"),
    path('populate_collections/', office_views.populate_collections, name="populate_collections"),
    path('new_position/', office_views.new_position, name="new_position"),
    path('edit_position/<int:position>', office_views.edit_position, name="edit_position"),
    path('save_position', office_views.save_position, name="save_position"),
    path('api/contract/<str:code>', office_views.contractapi, name="contractapi"),
    path('contract/<str:code>', office_views.contract, name="contract")
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)