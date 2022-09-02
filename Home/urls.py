from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('', views.main_view, name='main'),
    path('game/<int:num>/', views.game_view, name='game'),
    path('end_game/<int:num>/', views.end_game_view, name='end_game'),
    path('ins/<int:num>/', views.ins_view, name='ins'),
    # path('leave/', views.leave_view, name='leave'),
    path('db', views.test_db),
]
