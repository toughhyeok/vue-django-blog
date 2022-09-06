from django.urls import path

from api import views


app_name = 'api'
urlpatterns = [
    path('post/list/', views.ApiPostListView.as_view(),
         name='post_list'),
    path('post/<int:pk>/', views.ApiPostDetailView.as_view(),
         name='post_detail'),
    path('catetag/', views.ApiCateTagListView.as_view(),
         name='catetag_list'),
    path('like/<int:pk>/', views.ApiPostLikeDetailView.as_view(),
         name='post_like'),
    path('comment/create/', views.ApiCommentCreateView.as_view(),
         name='comment_create'),
]
