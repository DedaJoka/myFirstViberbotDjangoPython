from django.contrib import admin
from django.urls import path, include
# from myfirstviberbot.views import trx_bot
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = "Тут може бути ваша реклама!"
urlpatterns = [
    path('admin/', admin.site.urls),
]
