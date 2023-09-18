from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.relations import SlugRelatedField

from course_app.models import Course, Lesson, Payment, Subscription
from course_app.services import retrieve_session
from course_app.validators import VideoUrlValidator
from users.models import User
from users.serializers import UserSerializer


# Lesson ---------------------------------------------------------------------------------------------------------

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [VideoUrlValidator(fields=['video_url'])]


# Course ---------------------------------------------------------------------------------------------------------


class CourseSerializer(serializers.ModelSerializer):
    count_of_lessons = serializers.SerializerMethodField()  # read_only=True
    lesson = LessonSerializer(source='lessons', many=True, read_only=True)
    # lesson = SerializerMethodField(read_only=True)
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Course
        fields = '__all__'
        validators = [VideoUrlValidator(fields=['name', 'description'])]

    def get_count_of_lessons(self, instance):
        """Считает кол-во уроков"""
        if instance.lessons:
            return instance.lessons.all().count()
        # else:
        #     return 0

    def get_is_subscribed(self, obj):
        """Если пользователь подписан на курс, 'True' """
        user = self.context['request'].user
        return Subscription.objects.filter(user=user, course=obj).exists()


# Payment ---------------------------------------------------------------------------------------------------------


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class PaymentCreateSerializer(serializers.ModelSerializer):
    # course = serializers.SlugRelatedField(
    #     slug_field='name', queryset=Course.objects.all(), allow_null=True, required=False)
    lesson = serializers.SlugRelatedField(
        slug_field='name', queryset=Lesson.objects.all(), allow_null=True, required=False)
    user = serializers.SlugRelatedField(
        slug_field='email', queryset=User.objects.all())
    # date_of_payment

    class Meta:
        model = Payment
        # fields = '__all__'
        fields = ('session', 'course', 'lesson', 'user', 'payment_amount', 'payment_type')


class PaymentRetrieveSerializer(serializers.ModelSerializer):
    """this PaymentRetrieveSerializer"""
    # /////////////////////////////////////////
    course = CourseSerializer(read_only=True)
    lesson = LessonSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    # /////////////////////////////////////////

    url_for_pay = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Payment
        # //////////////////////
        fields = ('is_paid', 'date_of_payment', 'payment_amount',
                  'payment_type', 'url_for_pay', 'session', 'course', 'lesson', 'user' )

    def get_url_for_pay(self, instance) -> None | str | dict:
        """Возвращаем ссылку на оплату, если срок сессии прошел, либо оплачено -> None"""

        if instance.is_paid:
            return None
        session = retrieve_session(instance.session)
        if session.payment_status == 'unpaid' and session.status == 'open':
            return session.url
        elif session.payment_status == 'paid' and session.status == 'complete':
            return None

        status = {
            "session": "Срок сессии вышел! Необходимо заново создать платеж"
        }
        return status


# Subscription -------------------------------------------------------------------------------------------------------


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'


# Черновики для себя -------------------------------------------------------------------------------------------------


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
