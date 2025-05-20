from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet,
    RegisterAPIView,
    LoginAPIView,
    UserListCreateView,
    PricingViewSet,
    UserWithPricingView,
    ScheduleListCreateView,
    RatingCreateView,
    TopWorkersView
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'pricing', PricingViewSet, basename='pricing')

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('users/<int:pk>/with-pricing/', UserWithPricingView.as_view(), name='user-with-pricing'),
    path('employees/', UserListCreateView.as_view(), name='employee-list-create'),
    path('schedules/', ScheduleListCreateView.as_view(), name='schedule-list-create'),
    path('top-workers/', TopWorkersView.as_view(), name='top-workers'),
    path('', include(router.urls)),
    path('users/by_role/', UserViewSet.as_view({'get': 'by_role'}), name='users-by-role'),
    path('ratings/', RatingCreateView.as_view(), name='rating-create'),
]