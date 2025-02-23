from django.urls import path
app_name = "newsfeed"

from newsfeed import views
urlpatterns = [
    
    path('create/', views.create_post, name='create_post'),
    path('like-post/<int:post_id>/', views.toggle_post_like, name='post_like'),
    path('add-comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('add-reply/<int:comment_id>/', views.add_reply, name='add_reply'),
    path('', views.news_feed, name='newsfeed'),
    path('edit-post/<int:post_id>/', views.edit_post, name='edit_post'),
    path('delete-post/<int:post_id>/', views.delete_post, name='delete_post'),
]
    

