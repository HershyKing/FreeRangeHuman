from django.conf.urls import url
from django.contrib import admin
from dashboard import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'tags', views.TagListView.as_view(), name='tags'),
]
