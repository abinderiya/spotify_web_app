from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('login/', views.login, name='login'),
	path('callback/', views.callback, name='callback'),
	path('callback/<id>/visualize', views.visualize, name='visualize'),
	path('callback/feature-context', views.feature_context, name='feature_context'),
	path('callback/<id>/plot', views.plot, name='plot'),
]