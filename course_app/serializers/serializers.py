from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.relations import SlugRelatedField

from course_app.models import Course, Lesson


# Это сериализатор \/
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class CourseListSerializer(serializers.ModelSerializer):
    count_of_lessons = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'

    def get_count_of_lessons(self, instance):
        return instance.lessons.all().count()


# class CourseListSerializer(serializers.ModelSerializer):
#     """1.1 Выводит в списке курсов первый по списку урок"""
#     lesson_name = serializers.CharField(source='lesson_set.first')
#     class Meta:
#         model = Course
#         fields = '__all__'


# class CourseListSerializer(serializers.ModelSerializer):
#     """1.2 Выводит в списке курсов первый по списку урок"""
#     lesson_name = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Course
#         fields = '__all__'
#
#     def get_lesson_name(self, instance):
#         if instance.lesson_set.first():
#             return instance.lesson_set.first().name
#         return None


# class CourseListSerializer(serializers.ModelSerializer):
#     """2.1 Выводит в списке курсов спискок уроков"""
#     # lesson_name = serializers.CharField(source='lesson_set.first')
#     lesson = LessonSerializer(source='lesson_set', many=True)
#     # lesson_len = len(lesson)
#
#     class Meta:
#         model = Course
#         fields = '__all__'



