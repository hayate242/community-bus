from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginTokenObtaionView.as_view(), name='login'),
    path('user/', views.UserView.as_view(), name='user_regist'),
    path('user/info/', views.UserInfoView.as_view(), name='user_info')
]
