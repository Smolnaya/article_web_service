from django.urls import path

from smola import views

urlpatterns = [
    path('', views.index, name='index'),
    path('?<str:title>', views.getArticle, name='getArticle'),
    path('updateArticle/', views.updateArticle, name="updateArticle"),
    path('deleteArticle/', views.deleteArticle, name="deleteArticle"),
    path('searchArticle/', views.searchArticle, name="searchArticle"),
    path('filterArticle/', views.filterArticle, name="filterArticle"),
]
