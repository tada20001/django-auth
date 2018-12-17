from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls', )),
    path('', lambda request: redirect('/blog/')),
]
