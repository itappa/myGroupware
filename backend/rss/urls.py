from django.urls import path
from . import views

app_name = 'rss_reader'

urlpatterns = [
    path('', views.feed_list, name='feed_list'),
    path('add/', views.add_feed, name='add_feed'),
    path('feed/<int:feed_id>/', views.feed_entries, name='feed_entries'),
    path('mark_read/<int:entry_id>/', views.mark_as_read, name='mark_as_read'),
    path('update_feed/<int:feed_id>/', views.update_feed, name='update_feed'),
    path('update_all/', views.update_all_feeds, name='update_all_feeds'),
]