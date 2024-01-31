from courses.models import Course,Chapter,Post
from rest_framework import serializers

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id','course_name','courseIcon','createdAt']


class ChapterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chapter
        fields = ['id','title','course']


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id','content_type','object_id','']