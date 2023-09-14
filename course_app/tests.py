from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from course_app.models import Course, Lesson, Subscription
from users.models import User


# Create your tests here.

class LessonTestCase(APITestCase):

    # def setUp(self) -> None:
    #     self.user = User.objects.create(email='test@for1.ru', password='0000')
    #
    # def test_create_lesson(self):
    #     """тест соз урока"""
    #     data = {
    #         "name": "nameoflesson",
    #         "description": "descrrr",
    #         'owner': self.user
    #     }
    #     response = self.client.post(
    #         '/lesson/create/',
    #         data=data,
    #     )
    #
    #     print(response.json())
    #
    #     self.assertEqual(
    #         response.status_code,
    #         status.HTTP_201_CREATED
    #     )
    def setUp(self) -> None:
        self.url = '/'
        self.course = Course.objects.create(
            name='test',
            description='desccc'
        )
        self.user = User.objects.create(
            email='test@user.ru',
            password='0000'
        )
        self.data = {
            'name': 'test',
            'description': 'test',
            'course': self.course,
            'owner': self.user
        }

        self.lesson = Lesson.objects.create(**self.data)
        self.client.force_authenticate(user=self.user)

    def test_create_lesson(self):
        data = {
            'name': 'testT',
            'description': 'test',
            'course': self.course.pk,
            'owner': self.user.pk
        }
        lesson_create_url = reverse('course_app:lesson-create')
        response = self.client.post(lesson_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_list_lesson(self):
        lesson_list_url = reverse('course_app:lesson-list')
        response = self.client.get(lesson_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_detail_lesson(self):
        lesson_detail_url = reverse('course_app:lesson-retrieve', kwargs={'pk': self.lesson.pk})
        response = self.client.get(lesson_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.lesson.name)

    def test_update_lesson(self):
        lesson_update_url = reverse('course_app:lesson-update', kwargs={'pk': self.lesson.pk})
        new_name = 'new_name'
        data = {'name': new_name}
        response = self.client.patch(lesson_update_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.name, new_name)

    def test_delete_lesson(self):
        lesson_delete_url = reverse('course_app:lesson-delete', kwargs={'pk': self.lesson.pk})
        response = self.client.delete(lesson_delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Lesson.objects.filter(pk=self.lesson.pk).exists())


class SubscriptionsTestCase(APITestCase):
    def setUp(self) -> None:
        self.course = Course.objects.create(name='test', description='desc')
        self.user = User.objects.create(email='test@user.ru', password='0000')
        self.data = {
            'user': self.user,
            'course': self.course,
        }

        self.subscription = Subscription.objects.create(**self.data)
        self.client.force_authenticate(user=self.user)

    def test_create_subscription(self):
        data = {
            'user': self.user.pk,
            'course': self.course.pk,
        }
        subscription_url = reverse('course_app:course-subscribe')
        print(subscription_url)
        response = self.client.post(subscription_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # self.assertEqual(Subscription.objects.all().count(), 2)


    def test_list_subscriptions(self):
        subscription_url = reverse('course_app:subscription-list')
        print(subscription_url)
        response = self.client.get(subscription_url)
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_subscription(self):
        subscription_detail_url = reverse('course_app:lesson-retrieve', kwargs={'pk': self.subscription.pk})
        response = self.client.get(subscription_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(response.data['user'], self.subscription.user.pk)
        # self.assertFalse(Lesson.objects.filter(pk=self.lesson.pk).exists())

    # def test_delete_lesson(self):
    #     lesson_delete_url = reverse('course_app:lesson-delete', kwargs={'pk': self.lesson.pk})
    #     response = self.client.delete(lesson_delete_url)
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    #     self.assertFalse(Lesson.objects.filter(pk=self.lesson.pk).exists())