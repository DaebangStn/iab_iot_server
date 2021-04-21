from django.urls import path, re_path

from . import views

urlpatterns = [
    path('register/<str:req_mac>', views.register, name='register'),
    path('update/<str:up_mac>', views.update, name='update'),
    re_path(r'^control/(?P<parm_mac>[\s\S])/(?P<parm_mode>[od].+)$', views.mode, name='mode'),
    re_path(r'^control/(?P<parm_mac>[\s\S])/(?:speed-(?P<parm_speed>[0-9]*))$', views.change_speed, name='change_speed'),
]
