from rest_framework.pagination import PageNumberPagination


class CourseAppPaginator(PageNumberPagination):
    page_size = 10
