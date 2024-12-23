from django.contrib import admin
from django.urls import path,include
from . import views
from . models import Quiz
urlpatterns = [
    path('create/' , views.createquiz , name="createquiz"),
    path('login/', views.custom_login, name="custom_login"),
    path('logout/',views.custom_logout, name="custom_logout"),
    path('register/',views.register,name="register"),
    path('questioncreate/<int:quizobject>' , views.questioncreate , name="questioncreate"),
    path('' , views.home , name="home"),
    path('home/' , views.home , name="home"),
    path('staffquiz/',views.show_quiz,name="show_quiz"),
    path('staffquiz/<int:quizobject>'  , views.quizdetails , name="quizdetails"),
    path('staffquiz/takequiz/<int:quizobject>' , views.takequiz,name="takequiz"),
]
