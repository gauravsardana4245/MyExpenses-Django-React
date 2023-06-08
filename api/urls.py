from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("signup/", views.signup),
    path('', views.index),
    path('expenses/', views.getExpenses),
    path('expenses/create/', views.createExpense),
    path("expenses/<str:pk>/update/", views.updateExpense),
    path("expenses/<str:pk>/delete/", views.deleteExpense),
    path("expenses/<str:pk>/", views.getExpense)
]
