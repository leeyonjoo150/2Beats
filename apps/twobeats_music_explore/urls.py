from django.urls import path
from . import views

app_name = 'music_explore'

urlpatterns = [
    # 검색
    path('', views.search_music, name='search'),
    path('autocomplete/', views.search_autocomplete, name='autocomplete'),
    
    # 차트
    path('chart/', views.chart_all, name='chart_all'),
    path('chart/popular/', views.chart_popular, name='chart_popular'),
    path('chart/latest/', views.chart_latest, name='chart_latest'),
    path('chart/liked/', views.chart_liked, name='chart_liked'),
    
    # 상세
    path('detail/<int:music_id>/', views.music_detail, name='detail'),
    path('play/<int:music_id>/', views.increase_play_count, name='play_count'),
    
    # 좋아요
    path('like/<int:music_id>/', views.music_like, name='like'),
    path('like-status/<int:music_id>/', views.get_music_like_status, name='like_status'),
    
    # 댓글
    path('comment/<int:music_id>/', views.music_comment, name='comment'),
    path('comment/delete/<int:comment_id>/', views.comment_delete, name='comment_delete'),
    path('comment/edit/<int:comment_id>/', views.comment_edit, name='comment_edit'),
]