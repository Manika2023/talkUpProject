from django.urls import path
from meetings_app import views

urlpatterns = [
    path('',views.home,name="home"),
    path('about/',views.about,name="about"),
    path("register/",views.register,name="register"),
    path("login/",views.login_view,name="login"),
    path("dashboard/",views.dashboard,name='dashboard'),
    path("meeting/",views.videocall,name='meeting'),
    path('logout/',views.logout_view,name="logout"),
    path('join/',views.join_room,name="join")
]
