from django.conf.urls import url
from auth import views

urlpatterns = {
    url('^login/$', views.login, name='login'),
}
