from django.conf.urls import url
from news import views

urlpatterns = {
    url('^$', views.news, name='news'),
}
