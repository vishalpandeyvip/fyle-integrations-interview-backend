from django.shortcuts import render
from .serializers import TeacherSerializer
from rest_framework.views import APIView
from apps.teachers.models import Teacher
from apps.students.models import Assignment
from apps.students.serializers import StudentAssignmentSerializer
from rest_framework.response import Response
from rest_framework import status
import json

class ListAndGradeAssignment(APIView):
    """
    This View will enlist assignments
    and will grade those assignments.
    """
    def get(self, request, *args, **kwargs):
        principal_header = request.headers.get('X-Principal')
        data = json.loads(principal_header)
        teacher_id = data.get('teacher_id')

        # retrieves teacher with the given id
        # TODO: Should be used get, but test cases doesn't allow
        queryset = Teacher.objects.filter(id = teacher_id) 
        serialiser = TeacherSerializer(queryset, many = True) 
        return Response(data = serialiser.data, status = status.HTTP_200_OK)
    
    def patch(self, request, *args, **kwargs):
        """
        Patch request will be used to manipulate
        the grades assigned to a student's submission.
        """
        principal_header = request.headers.get('X-Principal')
        assignment_id = self.request.data.get('id')
        data = json.loads(principal_header)
        teacher_id = data.get('teacher_id')
        teacher = Teacher.objects.get(id = teacher_id)
        try:
            assignment = Assignment.objects.get(id = assignment_id)
        except Assignment.DoesNotExist:
            return Response({
                'non_field_errors': ['Assignment does not exists.']
            }, status = status.HTTP_404_NOT_FOUND)

        assignment_grade = request.data.get('grade')

        if assignment.state == 'GRADED':
            return Response({
                'non_field_errors': ['GRADED assignments cannot be graded again']
            }, status = status.HTTP_400_BAD_REQUEST)

        if 'content' in request.data:
            return Response({
                'non_field_errors': ['Teacher cannot change the content of the assignment']
            }, status = status.HTTP_400_BAD_REQUEST)

        if 'student' in request.data:
            return Response({
                'non_field_errors': ['Teacher cannot change the student who submitted the assignment']
            }, status = status.HTTP_400_BAD_REQUEST)

        if 'grade' in request.data and assignment.state != 'SUBMITTED':
            return Response({
                'non_field_errors': ['SUBMITTED assignments can only be graded']
            }, status = status.HTTP_400_BAD_REQUEST)

        if assignment.teacher != teacher:
            return Response({
                'non_field_errors': ['Teacher cannot grade for other teacher\'s assignment']
            }, status = status.HTTP_400_BAD_REQUEST)

        if assignment_grade is None or assignment_grade not in list('ABCD'):
            return Response({
                'grade': [f'{assignment_grade} is not a valid choice.']
            }, status = status.HTTP_400_BAD_REQUEST)

        assignment.grade = assignment_grade
        assignment.state = 'GRADED'
        assignment.save()
        serializer = StudentAssignmentSerializer(assignment)
        return Response(serializer.data, status=status.HTTP_200_OK)