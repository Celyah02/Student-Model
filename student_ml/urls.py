from django.contrib import admin
from django.urls import path, include
from performance.views import predict_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', predict_page, name='home'),
    path('api/', include('performance.urls')),
]
