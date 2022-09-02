from django.urls import path
from . import views
urlpatterns = [
    path('signup/', views.signup_view, name='sign_up'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('table/', views.table_view, name='table'),


]
