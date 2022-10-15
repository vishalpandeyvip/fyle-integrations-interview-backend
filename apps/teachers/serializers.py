from rest_framework import serializers
from .models import Teacher


class TeacherSerializer(serializers.ModelSerializer):
    """
    Teacher Serialiser
    """
    class Meta:
        model = Teacher
        fields = '__all__'
