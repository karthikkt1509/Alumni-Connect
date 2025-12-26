# users/urls.py
from django.urls import path
from .views import register, user_login, user_logout, user_list, user_detail
from . import views
urlpatterns = [
    path('',views.home, name = 'home'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('users/', user_list, name='user_list'),
    path('users/<int:pk>/', user_detail, name='user_detail'),
   
    path('chat/<str:username>/', views.chat_page, name='chat_page'),
    path("jobs/post/", views.job_posting, name="job_posting"),
    path("jobs/", views.job_list, name="job_list"),
    path('questions/', views.question_list, name='question_list'),
    path('question/<int:pk>/', views.question_detail, name='question_detail'),
    path('ask/', views.ask_question, name='ask_question'),
    path('answer/upvote/<int:answer_id>/', views.upvote_answer, name='upvote_answer'),
]
