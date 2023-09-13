from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.relations import SlugRelatedField

from course_app.models import Course, Lesson, Payment
from course_app.validators import VideoUrlValidator


# Это сериализатор \/

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [VideoUrlValidator(fields=['video_url'])]


class CourseSerializer(serializers.ModelSerializer):
    count_of_lessons = serializers.SerializerMethodField()  # read_only=True
    lesson = LessonSerializer(source='lessons', many=True, read_only=True)
    # lesson = SerializerMethodField(read_only=True)

    class Meta:
        model = Course
        fields = '__all__'
        validators = [VideoUrlValidator(fields=['name', 'description'])]

    def get_count_of_lessons(self, instance):
        if instance.lessons:
            return instance.lessons.all().count()
        # else:
        #     return 0


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


# class CourseSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Course
#         fields = '__all__'


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
