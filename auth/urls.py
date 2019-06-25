from django.conf.urls import url
from auth import views

urlpatterns = {
    url('^login/$', views.login, name='login'),
    url('^login.html$', views.login, name='login'),
    url('^signup/$', views.sign_up, name='sign_up'),
    url('^signup.html$', views.sign_up, name='sign_up')
}
