from django.contrib import admin
from django.urls import path, include

admin.site.site_header = "Тут може бути ваша реклама!"
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('viber_bot.urls')),
]
