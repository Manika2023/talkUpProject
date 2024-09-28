
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include("meetings_app.urls")),
    path('board/',include("masterBoard.urls")),
]
