from django.urls import path
from .views import ListAndGradeAssignment

urlpatterns = [
    path('assignments/', ListAndGradeAssignment.as_view(), name = "teachers_assignments")
]
