
from django.urls import path
from .views import CourseView,CourseDetailsView,chapterList,api
urlpatterns = [
    path('courses/',CourseView.as_view()),
    path('courses/<int:pk>',CourseDetailsView.as_view()),
    path('chapters/<int:course_id>',chapterList),
    path('my-course/<int:id>',api),
]
