from django.urls import path
from home.views import LoginAPI,SignupAPI,get_csrf_token

urlpatterns=[  
    path('login/',LoginAPI.as_view()),
    path('signup/',SignupAPI.as_view()),
    path('csrf-token/',get_csrf_token)
]