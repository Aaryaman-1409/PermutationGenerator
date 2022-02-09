from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='qna-home'),
    path('help/', views.help_page, name='help-page')
]
