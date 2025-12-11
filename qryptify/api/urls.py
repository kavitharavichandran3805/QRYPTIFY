from django.urls import path
from home.views import LoginAPI,SignupAPI,get_csrf_token,UserDetailsAPI,LogoutAPI,RefreshTokenAPI,EmailAPI,UpdateUserDetailsAPI

urlpatterns=[  
    path('login/',LoginAPI.as_view()),
    path('signup/',SignupAPI.as_view()),
    path('csrf-token/',get_csrf_token),
    path('user-details/',UserDetailsAPI.as_view()),
    path('logout/',LogoutAPI.as_view()),
    path('refresh-token/',RefreshTokenAPI.as_view()),
    path('issue-mail/',EmailAPI.as_view()),
    path('reset-password/',LoginAPI.as_view()),
    path('update-profile/',UpdateUserDetailsAPI.as_view())
]