from django.urls import path

from course_app.apps import CourseAppConfig
from rest_framework.routers import DefaultRouter

# from course_app.views import CourseViewSet, LessonCreateAPIView
from course_app.views import *

app_name = CourseAppConfig.name

router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')

urlpatterns = [
    path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson-create'),
    path('lesson/', LessonListAPIView.as_view(), name='lesson-list'),
    path('lesson/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson-retrieve'),
    path('lesson/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson-update'),
    path('lesson/delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='lesson-delete'),

    path('payment/list/', PaymentListAPIView.as_view(), name='payment-list'),

    path('course/<int:pk>/subscribe/', SubscriptionCreateAPIView.as_view(), name='course-subscribe'),
    path('subscription/list/', SubscriptionListAPIView.as_view(), name='subscription-list'),
    path('subscription/<int:pk>/delete/', SubscriptionDestroyAPIView.as_view(), name='subscription-destroy'),

] + router.urls
