from django.urls import path
from .views import GetStudents

urlpatterns = [
    path('get-students/', GetStudents.as_view(), name='get_students'),
]
