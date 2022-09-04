from django.urls import path

from api import views


app_name = 'api'
urlpatterns = [
    path('post/list/', views.ApiPostListView.as_view(), name='post_list'),
    path(
        'post/<int:pk>/',
        views.ApiPostDetailView.as_view(),
        name='post_detail'
    ),
]
