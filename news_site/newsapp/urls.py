from django.urls import path
from . import views

urlpatterns = [
    path('', views.cluster_list, name='cluster_list'),
    path('cluster/<int:cluster_id>/', views.articles_by_cluster, name='articles_by_cluster'),
]
